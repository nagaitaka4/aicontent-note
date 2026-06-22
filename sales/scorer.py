"""
40社スコアリングスクリプト
3軸：ブログ運用代行 / HP制作営業 / ロゴ制作営業
A判定時：営業文・フォーム入力ガイド自動生成
"""

import csv
import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# .envファイルがあれば読み込む（python-dotenv不要・手動パース）
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

try:
    import anthropic as _anthropic
    _ANTHROPIC_CLIENT = _anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    _HAIKU_AVAILABLE = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
except Exception:
    _ANTHROPIC_CLIENT = None
    _HAIKU_AVAILABLE = False

INPUT_FILE = os.path.join(os.path.dirname(__file__), "urls-found.csv")
OUTPUT_FILE      = os.path.join(os.path.dirname(__file__), "scored-results.csv")
OUT_BLOG_FILE    = os.path.join(os.path.dirname(__file__), "a-leads-blog.csv")
OUT_HP_FILE      = os.path.join(os.path.dirname(__file__), "a-leads-hp.csv")
OUT_LOGO_FILE    = os.path.join(os.path.dirname(__file__), "a-leads-logo.csv")

# =============================
# 送信者情報（営業文に使用）
# =============================
SENDER_NAME = "永井貴司"
SENDER_MEDIA = "AIコンテンツ運用ノート"
SENDER_EMAIL = "support@aicontent-note.com"
SENDER_SERVICE_URL = "https://aicontent-note.com/service/"
SENDER_MEDIA_URL = "https://aicontent-note.com/"

EXCLUDED_SITE_DOMAINS = [
    "hellowork", "city.", ".go.jp", "kenkyo", "wikipedia",
    "facebook", "instagram", "twitter", "x.com", "linkedin",
    "indeed", "doda", "mynavi", "rikunabi", "hotpepper",
    "townwork", "baitoru", "workin", "aomori.jp",
]

NOW = datetime.now()


# =============================
# サイト品質シグナル判定
# =============================

def site_quality_signals(html, soup, url):
    """サイトの古さ・品質を示すシグナルを収集する"""
    signals = []

    # ① DOCTYPE HTML4/XHTML
    if re.search(r'<!DOCTYPE HTML PUBLIC', html, re.IGNORECASE):
        signals.append("HTML4/XHTMLドキュメント")

    # ② HTTPSなし
    if url.startswith("http://"):
        signals.append("HTTPS未対応")

    # ③ フッター著作権年が古い（2019年以前）
    copyright_match = re.search(r'[©Ⓒ]\s*(\d{4})', html)
    if not copyright_match:
        copyright_match = re.search(r'copyright\s*[\(]?\s*(\d{4})', html, re.IGNORECASE)
    if copyright_match:
        year = int(copyright_match.group(1))
        if year <= 2019:
            signals.append(f"著作権年が古い（{year}年）")

    # ④ テーブルレイアウト（データテーブルを除く）
    tables = soup.find_all("table")
    layout_tables = [t for t in tables if not t.find("th") and not t.find("thead")]
    if len(layout_tables) >= 2:
        signals.append("テーブルレイアウト")

    # ⑤ OGP未設定
    has_ogp = bool(soup.find("meta", attrs={"property": "og:title"}))
    if not has_ogp:
        signals.append("OGP未設定")

    # ⑥ meta description未設定
    has_meta_desc = bool(soup.find("meta", attrs={"name": "description"}))
    if not has_meta_desc:
        signals.append("meta description未設定")

    # ⑦ jQuery旧バージョン（1.x / 2.x）
    jquery_match = re.search(r'jquery[.\-](\d+\.\d+)', html, re.IGNORECASE)
    if jquery_match:
        version = jquery_match.group(1)
        major = int(version.split(".")[0])
        if major <= 2:
            signals.append(f"jQuery {version}（旧バージョン）")

    return signals


def logo_signals(html, soup):
    """ロゴの品質シグナルを収集する"""
    result = {
        "has_favicon": False,
        "logo_type": "不明",
        "logo_detail": "",
    }

    # ファビコン
    favicon = soup.find("link", rel=re.compile(r"(shortcut )?icon", re.I))
    result["has_favicon"] = bool(favicon)

    # ロゴ検出
    header = (
        soup.find("header")
        or soup.find(id=re.compile(r"header", re.I))
        or soup.find(class_=re.compile(r"header", re.I))
    )
    search_area = header if header else soup

    # SVGロゴ
    svg_logo = search_area.find("svg")
    if svg_logo:
        result["logo_type"] = "SVG（モダン）"
        result["logo_detail"] = "SVGロゴ"
        return result

    # 画像ロゴ
    logo_img = (
        search_area.find("img", src=re.compile(r"logo", re.I))
        or search_area.find("img", alt=re.compile(r"logo|ロゴ", re.I))
        or (search_area.find("img") if header else None)
    )

    if logo_img:
        src = logo_img.get("src", "")
        w = logo_img.get("width", "")
        h = logo_img.get("height", "")
        # SVG埋め込み
        if src.endswith(".svg"):
            result["logo_type"] = "SVG（モダン）"
        # 極小ロゴ（32px以下）
        elif w and h and int(re.sub(r"\D", "", w) or "999") <= 32:
            result["logo_type"] = "極小画像（低品質の可能性）"
        else:
            result["logo_type"] = "画像ロゴ"
        result["logo_detail"] = src[:50]
    else:
        result["logo_type"] = "テキストのみ（画像ロゴなし）"

    return result


# =============================
# サイト調査
# =============================

def investigate(page, url):
    result = {
        "is_wp": False,
        "has_blog": False,
        "last_update": None,
        "months_stopped": None,
        "article_count": 0,
        "is_responsive": False,
        "has_form": False,
        "form_url": None,
        "email": None,
        "quality_signals": [],
        "logo": {},
        "error": None,
        "is_wrong_site": False,
    }

    if any(exc in url.lower() for exc in EXCLUDED_SITE_DOMAINS):
        result["is_wrong_site"] = True
        result["error"] = "公式サイトではない可能性あり"
        return result

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        # WordPress判定
        wp_signals = ["wp-content", "wp-includes", "wp-json", 'content="WordPress"']
        result["is_wp"] = any(s in html for s in wp_signals)

        # スマホ対応
        result["is_responsive"] = bool(soup.find("meta", attrs={"name": "viewport"}))

        # 品質シグナル
        result["quality_signals"] = site_quality_signals(html, soup, url)

        # ロゴ
        result["logo"] = logo_signals(html, soup)

        # メール
        email_match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", html)
        if email_match:
            email = email_match.group(0)
            if not any(x in email for x in ["example", "your@", "test@", ".png", ".jpg", "sentry", "wpcf7"]):
                result["email"] = email

        # フォーム
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            link_text = a.get_text(strip=True)
            if any(kw in link_text + href for kw in ["contact", "お問い合わせ", "問合せ", "inquiry"]):
                full_url = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                result["has_form"] = True
                result["form_url"] = full_url
                break
        if not result["has_form"] and soup.find("form"):
            result["has_form"] = True
            result["form_url"] = url

        # ブログ調査
        blog_urls_to_check = []
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            link_text = a.get_text(strip=True)
            if any(kw in link_text + href for kw in ["お知らせ", "ニュース", "ブログ", "news", "blog", "topics", "information", "新着", "column"]):
                full = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                if url.split("/")[2] in full:
                    blog_urls_to_check.append(full)

        for path in ["/news", "/blog", "/topics", "/information", "/info", "/column"]:
            blog_urls_to_check.append(url.rstrip("/") + path)

        blog_urls_to_check = list(dict.fromkeys(blog_urls_to_check))[:5]

        for blog_url in blog_urls_to_check:
            try:
                page.goto(blog_url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(1)
                blog_soup = BeautifulSoup(page.content(), "html.parser")
                dates = extract_dates(blog_soup.get_text())
                if dates:
                    result["has_blog"] = True
                    latest = max(dates, key=lambda d: d[1])
                    result["last_update"] = latest[0]
                    result["months_stopped"] = round((NOW - latest[1]).days / 30, 1)
                    items = blog_soup.find_all(
                        ["article", "li", "div"],
                        class_=re.compile(r"(post|entry|item|news|blog)", re.I)
                    )
                    result["article_count"] = len(items) if items else len(dates)
                    break
            except:
                continue

        if not result["has_blog"]:
            dates = extract_dates(text)
            if dates:
                latest = max(dates, key=lambda d: d[1])
                result["last_update"] = latest[0]
                result["months_stopped"] = round((NOW - latest[1]).days / 30, 1)

    except Exception as e:
        result["error"] = str(e)[:100]

    return result


def extract_dates(text):
    patterns = [
        (r"(\d{4})年(\d{1,2})月(\d{1,2})日", lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (r"(\d{4})/(\d{1,2})/(\d{1,2})", lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (r"(\d{4})-(\d{1,2})-(\d{1,2})", lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (r"(\d{4})\.(\d{1,2})\.(\d{1,2})", lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
    ]
    results = []
    for pattern, parser in patterns:
        for m in re.finditer(pattern, text):
            try:
                dt = parser(m)
                if 2010 <= dt.year <= NOW.year:
                    results.append((m.group(0), dt))
            except:
                pass
    return results


# =============================
# 日付フォーマット変換
# =============================

def format_date_jp(date_str):
    """各種日付文字列をYYYY年M月D日形式に変換。変換できなければそのまま返す"""
    if not date_str:
        return "不明"
    patterns = [
        r"(\d{4})[年./\-](\d{1,2})[月./\-](\d{1,2})",
    ]
    for pat in patterns:
        m = re.search(pat, date_str)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return f"{y}年{mo}月{d}日"
    return date_str


# =============================
# Haiku APIによるテーマ生成
# =============================

def generate_themes(company_name, location, site_text):
    """Claude Haiku APIで会社ごとの記事テーマ3本を生成する"""
    if not _HAIKU_AVAILABLE or not _ANTHROPIC_CLIENT:
        return "（テーマ自動生成：ANTHROPIC_API_KEY未設定）", "", ""

    prompt = f"""あなたはブログ運用代行の営業担当者です。
以下の会社情報とホームページの内容を参考に、この会社が情報発信できそうなブログ記事タイトルを3本提案してください。

会社名：{company_name}
所在地：{location}
HPの内容（抜粋）：
{site_text[:1500]}

条件：
・建設・土木・電気工事などの業種に合わせた実務的なテーマにする
・採用・企業PR・技術紹介など、読まれやすいテーマを選ぶ
・タイトルは20〜35文字程度
・「〜の方法」「〜のポイント」などの具体的な形式で
・必ず3本、番号なし・箇条書きなしでタイトルのみを1行ずつ出力する

出力形式（この形式のみ。前置き・説明・記号は不要）：
タイトル1
タイトル2
タイトル3"""

    try:
        response = _ANTHROPIC_CLIENT.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        lines = [l.strip() for l in response.content[0].text.strip().split("\n") if l.strip()]
        t1 = lines[0] if len(lines) > 0 else ""
        t2 = lines[1] if len(lines) > 1 else ""
        t3 = lines[2] if len(lines) > 2 else ""
        return t1, t2, t3
    except Exception as e:
        return f"（テーマ生成エラー：{str(e)[:50]}）", "", ""


# =============================
# 営業文生成（メール版・フォーム版）
# =============================

def generate_sales_message(company_name, last_update, months_stopped, theme_1="", theme_2="", theme_3=""):
    """メール送信用営業文"""
    update_text = format_date_jp(last_update)
    months_int = int(months_stopped) if months_stopped else 0

    subject = f"【{company_name}様】ホームページ更新についてのご提案"

    body = f"""{company_name}
ご担当者　様

はじめまして。

AIコンテンツ運用ノートというメディアを運営しております、永井と申します。

貴社HPを拝見したところ、ブログ・お知らせの最終更新が、
「{update_text}」となっており、約{months_int}か月ほど
定期的な情報発信が停止しているご状況とお見受けしました。

採用活動においては、求職者のほとんどはHPもあわせて確認することが一般的です。

そのため、

「今も活動している会社なのか分からない」
「どのような事業を行っているか伝わりにくい」
「会社の雰囲気や日々の活動が見えにくい」

といった印象につながってしまうことがあり、少しもったいないと感じました。

一方で、情報発信の重要性は理解されていても、

・更新担当者がいない
・本業が忙しく後回しになってしまう
・記事の内容を考える時間がない

といった理由で、情報発信が止まってしまう企業様も少なくありません。

HPの情報発信は、求職者だけでなく、お客様や取引先などが会社を知るための情報源にもなります。

弊サービスのブログ運用代行では、
記事テーマの企画・設計から執筆、WordPressへの入稿・公開まで、
まるごと対応しております。

ご担当者様に行っていただく作業は、

・初回ヒアリング
・月初の記事テーマ確認
・記事内容確認

のみです。

※担当者を増やしたり、構成や記事内容を毎回考えたりする必要はありません。
※メール・フォームのみで完結するため、打ち合わせ日程の調整などは不要です。

参考までに、現在のHPを拝見し、情報発信の題材になりそうな記事テーマを3つ考えてみました。

・{theme_1}
・{theme_2}
・{theme_3}

このような内容を継続的に発信できるよう、
まずは1ヶ月のお試しプラン（5万円）もご用意しております。

■サービス詳細
{SENDER_SERVICE_URL}

ご興味がございましたら、お気軽にご返信いただけますと幸いです。



━━━━━━━━━━━━━━━━━━

{SENDER_MEDIA} / {SENDER_NAME}

HP：{SENDER_MEDIA_URL}
Mail：{SENDER_EMAIL}

━━━━━━━━━━━━━━━━━━"""

    return subject, body


def generate_form_message(company_name, last_update, months_stopped, theme_1="", theme_2="", theme_3=""):
    """お問い合わせフォーム用営業文"""
    update_text = format_date_jp(last_update)
    months_int = int(months_stopped) if months_stopped else 0

    subject = "ホームページ更新についてのご提案"

    body = f"""{company_name}
ご担当者様

はじめまして。

AIコンテンツ運用ノートというメディアを運営しております、永井と申します。

貴社HPを拝見したところ、ブログ・お知らせの最終更新が
「{update_text}」となっており、約{months_int}か月ほど
情報発信が停止しているご状況とお見受けしました。

採用活動においては、求職者のほとんどはHPも確認することが一般的です。

そのため、

・今も活動している会社なのか分からない
・どのような事業を行っているか伝わりにくい
・会社の雰囲気や日々の活動が見えにくい

といった印象につながってしまうことがあり、少しもったいないと感じました。

弊サービスでは、記事テーマの企画・設計から執筆、WordPressへの入稿・公開まで対応しております。

参考までに、現在のHPを拝見し、情報発信の題材になりそうな記事テーマを考えてみました。

・{theme_1}
・{theme_2}
・{theme_3}

サービスの詳細はこちらをご覧ください。
{SENDER_SERVICE_URL}

ご興味がございましたら、
お気軽にご返信いただけますと幸いです。


永井

{SENDER_MEDIA_URL}
{SENDER_EMAIL}"""

    return subject, body


def extract_form_fields(page, form_url):
    """フォームの項目名を取得し、入力ガイドを生成する"""
    try:
        page.goto(form_url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(1.5)
        soup = BeautifulSoup(page.content(), "html.parser")

        form = soup.find("form")
        if not form:
            return None

        field_map = []

        # label → input の対応を取得
        for label in form.find_all("label"):
            label_text = label.get_text(strip=True)
            if not label_text:
                continue
            for_id = label.get("for", "")
            input_el = (
                form.find(id=for_id)
                if for_id
                else label.find_next(["input", "textarea", "select"])
            )
            if not input_el:
                continue
            field_type = input_el.name
            input_type = input_el.get("type", "text")
            if input_type in ["submit", "button", "hidden", "reset"]:
                continue

            # 入力内容をラベルから推定
            kw = label_text.lower()
            if any(k in kw for k in ["名前", "氏名", "お名前", "name"]):
                value = SENDER_NAME
            elif any(k in kw for k in ["会社", "法人", "事業所", "company"]):
                value = SENDER_MEDIA
            elif any(k in kw for k in ["メール", "mail", "email"]):
                value = SENDER_EMAIL
            elif any(k in kw for k in ["電話", "tel", "phone"]):
                value = "（省略可能な場合は空欄）"
            elif any(k in kw for k in ["件名", "タイトル", "subject"]):
                value = "【ご提案】ブログ記事更新についてのご相談"
            elif any(k in kw for k in ["内容", "本文", "メッセージ", "コメント", "お問", "相談", "message", "body", "content"]):
                value = "【営業文本文をここに入力】"
            else:
                value = f"（{label_text}：内容確認の上入力）"

            field_map.append(f"・{label_text}：{value}")

        return "\n".join(field_map) if field_map else None

    except Exception as e:
        return f"（フォーム取得エラー：{str(e)[:50]}）"


# =============================
# スコアリング
# =============================

def score(r, url):
    months = r["months_stopped"]
    has_form_or_email = r["has_form"] or bool(r["email"])
    quality = r["quality_signals"]
    logo = r["logo"]
    is_old_site = len(quality) >= 2  # シグナル2つ以上 = 古いサイトと判断

    # ---- ブログ運用代行 ----
    if r["is_wp"] and has_form_or_email:
        if months is not None and months >= 6 and r["article_count"] >= 5:
            blog = "A"
        elif months is not None and months >= 6:
            blog = "B"
        elif months is not None and months >= 3:
            blog = "B"
        else:
            blog = "C"
    elif r["is_wp"]:
        blog = "D"
    else:
        blog = "D"

    # ---- HP制作営業 ----
    if r["is_wrong_site"]:
        hp = "D（公式サイト未確認）"
    elif r["is_wp"]:
        hp = "—"
    else:
        if has_form_or_email:
            if not r["is_responsive"]:
                hp = "A（スマホ非対応）"
            elif is_old_site:
                hp = "A（古いサイト）"
            else:
                hp = "B"
        else:
            hp = "C（連絡手段なし）"

    # HPなし＋メールあり
    if r["is_wrong_site"] and r["email"]:
        hp = "A（HPなし・メール有）"

    # ---- ロゴ制作 ----
    logo_type = logo.get("logo_type", "不明")
    has_favicon = logo.get("has_favicon", True)

    if r["is_wrong_site"]:
        logo_score = "D（公式サイト未確認）"
    elif "テキストのみ" in logo_type:
        logo_score = "A（テキストロゴのみ）" if has_form_or_email else "B"
    elif not has_favicon and is_old_site and has_form_or_email:
        logo_score = "A（ファビコンなし＋古いサイト）"
    elif "SVG" in logo_type:
        logo_score = "D（SVGロゴ・モダン）"
    elif "極小" in logo_type and has_form_or_email:
        logo_score = "B（極小ロゴ）"
    elif is_old_site and has_form_or_email:
        logo_score = "B（古いサイト・要目視）"
    else:
        logo_score = "C（要目視確認）"

    return blog, hp, logo_score


# =============================
# メイン
# =============================

def main():
    companies = []
    with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="ja-JP",
        )
        page = context.new_page()

        for i, company in enumerate(companies, 1):
            name = company["会社名"]
            location = company["所在地"]
            url = company["URL"]

            print(f"\n[{i:02d}/{len(companies)}] {name}")
            print(f"  URL: {url}")

            r = investigate(page, url)
            blog, hp, logo_score = score(r, url)

            contact_parts = []
            if r["form_url"]:
                contact_parts.append(f"フォーム：{r['form_url']}")
            if r["email"]:
                contact_parts.append(f"メール：{r['email']}")
            if not contact_parts:
                contact_parts.append("なし")

            quality_str = " / ".join(r["quality_signals"]) if r["quality_signals"] else "なし"
            logo_type = r["logo"].get("logo_type", "不明")
            has_fav = "あり" if r["logo"].get("has_favicon") else "なし"

            print(f"  WP:{r['is_wp']} スマホ:{r['is_responsive']} ブログ:{r['has_blog']} 最終更新:{r['last_update']} 記事:{r['article_count']}")
            print(f"  品質シグナル：{quality_str}")
            print(f"  ロゴ：{logo_type} / ファビコン：{has_fav}")
            print(f"  → ブログ代行:{blog} / HP制作:{hp} / ロゴ:{logo_score}")
            if r["error"]:
                print(f"  ⚠ {r['error']}")

            # A判定時：テーマ生成・営業文・フォーム入力ガイド生成
            sales_subject = ""
            sales_body = ""
            form_subject = ""
            form_body = ""
            form_guide = ""
            theme_1 = theme_2 = theme_3 = ""

            if blog == "A":
                # サイトテキスト取得（テーマ生成用）
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(1)
                    site_text = BeautifulSoup(page.content(), "html.parser").get_text()
                except Exception:
                    site_text = ""

                theme_1, theme_2, theme_3 = generate_themes(name, location, site_text)
                print(f"  テーマ生成：{theme_1} / {theme_2} / {theme_3}")

                sales_subject, sales_body = generate_sales_message(
                    name, r["last_update"], r["months_stopped"],
                    theme_1, theme_2, theme_3
                )
                form_subject, form_body = generate_form_message(
                    name, r["last_update"], r["months_stopped"],
                    theme_1, theme_2, theme_3
                )

                if r["form_url"]:
                    guide = extract_form_fields(page, r["form_url"])
                    if guide:
                        form_guide = guide + "\n・お問い合わせ内容：【フォーム版営業文本文を入力】"
                    else:
                        form_guide = "（フォーム項目を自動取得できませんでした）"

            results.append({
                "会社名": name,
                "所在地": location,
                "URL": url,
                "WordPress": "あり" if r["is_wp"] else "なし",
                "スマホ対応": "あり" if r["is_responsive"] else "なし",
                "ブログ有無": "あり" if r["has_blog"] else "なし",
                "最終更新日": r["last_update"] or "不明",
                "更新停止（月）": r["months_stopped"] or "不明",
                "記事数目安": r["article_count"],
                "品質シグナル": quality_str,
                "ロゴ評価": logo_type,
                "ファビコン": has_fav,
                "連絡手段": " / ".join(contact_parts),
                "ブログ運用代行": blog,
                "HP制作営業": hp,
                "ロゴ制作": logo_score,
                "テーマ1": theme_1,
                "テーマ2": theme_2,
                "テーマ3": theme_3,
                "営業文（件名）": sales_subject,
                "営業文（本文）": sales_body,
                "フォーム版（件名）": form_subject,
                "フォーム版（本文）": form_body,
                "フォーム入力ガイド": form_guide,
                "備考": r["error"] or "",
            })

            time.sleep(1)

        browser.close()

    # 既存CSVを読み込んで重複チェック（会社名＋URLで判定）
    existing_keys = set()
    fieldnames = list(results[0].keys())
    file_exists = os.path.exists(OUTPUT_FILE)

    if file_exists:
        with open(OUTPUT_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_keys.add((row["会社名"], row["URL"]))

    new_results = [r for r in results if (r["会社名"], r["URL"]) not in existing_keys]
    skipped = len(results) - len(new_results)

    mode = "a" if file_exists else "w"
    with open(OUTPUT_FILE, mode, newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_results)

    print("\n" + "=" * 55)
    print(f"完了：{OUTPUT_FILE}")
    print(f"追記：{len(new_results)}件 / スキップ（重複）：{skipped}件")

    # 累計集計
    all_results = []
    with open(OUTPUT_FILE, newline="", encoding="utf-8-sig") as f:
        all_results = list(csv.DictReader(f))
    a_blog  = sum(1 for r in all_results if r["ブログ運用代行"] == "A")
    a_hp    = sum(1 for r in all_results if str(r["HP制作営業"]).startswith("A"))
    a_logo  = sum(1 for r in all_results if str(r["ロゴ制作"]).startswith("A"))
    print(f"【累計 {len(all_results)}社】A判定：ブログ代行 {a_blog}件 / HP制作 {a_hp}件 / ロゴ制作 {a_logo}件")
    print("=" * 55)

    # A判定リストをサービス別ファイルに書き出し（全件を上書き再生成）
    blog_leads = [r for r in all_results if r["ブログ運用代行"] == "A"]
    hp_leads   = [r for r in all_results if str(r["HP制作営業"]).startswith("A")]
    logo_leads = [r for r in all_results if str(r["ロゴ制作"]).startswith("A")]

    blog_fields = ["会社名", "所在地", "URL", "連絡手段", "最終更新日", "更新停止（月）",
                   "テーマ1", "テーマ2", "テーマ3",
                   "営業文（件名）", "営業文（本文）", "フォーム版（件名）", "フォーム版（本文）",
                   "フォーム入力ガイド", "備考"]
    simple_fields = ["会社名", "所在地", "URL", "連絡手段", "HP制作営業", "備考"]
    logo_fields   = ["会社名", "所在地", "URL", "連絡手段", "ロゴ制作", "備考"]

    def write_leads(path, leads, fields):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leads)

    write_leads(OUT_BLOG_FILE, blog_leads, blog_fields)
    write_leads(OUT_HP_FILE,   hp_leads,   simple_fields)
    write_leads(OUT_LOGO_FILE, logo_leads, logo_fields)

    print(f"  → ブログ代行A：{OUT_BLOG_FILE}（{len(blog_leads)}件）")
    print(f"  → HP制作A  ：{OUT_HP_FILE}（{len(hp_leads)}件）")
    print(f"  → ロゴ制作A：{OUT_LOGO_FILE}（{len(logo_leads)}件）")


if __name__ == "__main__":
    main()
