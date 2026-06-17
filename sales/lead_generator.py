"""
営業リスト自動生成スクリプト（Playwright版）
- IndeedをPlaywrightで検索 → 会社名・URL取得
- 各社サイトをWordPress/ブログ/採用/連絡先チェック
- A〜Dスコアリング → leads-scored.csvに追記出力
"""

import csv
import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# =============================
# 設定（ここを変更する）
# =============================

SEARCH_QUERIES = [
    "介護",
    "建設",
    "福祉",
]

TARGET_A_COUNT = 30      # A判定をこの件数集めたら終了
MAX_COMPANIES = 500      # 上限（無限ループ防止）
RESULTS_PER_PAGE = 10    # Indeedの1ページあたり件数

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "leads-scored.csv")

EXCLUDED_DOMAINS = [
    "indeed", "hellowork", "doda", "mynavi", "rikunabi",
    "en-japan", "jobcan", "wikipedia", "facebook",
    "instagram", "twitter", "x.com", "linkedin",
    "hotpepper", "townwork", "baitoru", "kaigokensaku",
    "job-gear", "workin", "an-job", "standby", "jopus",
    "kyujinbox", "求人ボックス",
]


# =============================
# Indeed検索（Playwright）
# =============================

def search_indeed(page, query, num_results=30):
    companies = []
    seen = set()
    start = 0

    while len(companies) < num_results:
        url = f"https://jp.indeed.com/jobs?q={query}&start={start}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        name_elems = soup.find_all("span", {"data-testid": "company-name"})
        loc_elems = soup.find_all("div", {"data-testid": "text-location"})

        if not name_elems:
            # 構造が違う場合の代替セレクタ
            name_elems = soup.find_all(class_=re.compile(r"companyName"))
            loc_elems = soup.find_all(class_=re.compile(r"companyLocation"))

        if not name_elems:
            print(f"  [警告] 会社名が取得できませんでした（start={start}）")
            break

        for i, elem in enumerate(name_elems):
            name = elem.get_text(strip=True)
            location = loc_elems[i].get_text(strip=True) if i < len(loc_elems) else ""
            if name and name not in seen:
                seen.add(name)
                companies.append({"name": name, "location": location})

        if len(name_elems) < 10:
            break

        start += 10
        time.sleep(2)

    return companies[:num_results]


# =============================
# 会社URL取得（Yahoo Japan経由）
# =============================

def find_company_url(page, company_name, location=""):
    import urllib.parse
    query = urllib.parse.quote(f"{company_name} {location} 公式サイト")
    url = f"https://search.yahoo.co.jp/search?p={query}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)

        soup = BeautifulSoup(page.content(), "html.parser")

        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if (
                href.startswith("http")
                and not any(exc in href.lower() for exc in EXCLUDED_DOMAINS)
                and "yahoo" not in href.lower()
            ):
                return href

    except Exception as e:
        print(f"  [URL取得エラー] {company_name}: {e}")

    return None


# =============================
# サイト調査（WordPress/ブログ/採用/連絡）
# =============================

def investigate_site(page, url):
    result = {
        "is_wp": False,
        "last_update": None,
        "has_hiring": False,
        "contacts": [],
        "html": "",
    }

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)
        html = page.content()
        result["html"] = html
        soup = BeautifulSoup(html, "html.parser")

        # WordPress判定
        wp_signals = ["wp-content", "wp-includes", "wp-json", 'content="WordPress"']
        result["is_wp"] = any(s in html for s in wp_signals)

        # ブログ最終更新日
        result["last_update"] = extract_date(soup.get_text())

        # 採用ページ有無
        hiring_kw = ["採用情報", "採用募集", "求人情報", "recruit", "career", "採用"]
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href", "")
            if any(kw in text or kw in href for kw in hiring_kw):
                result["has_hiring"] = True
                break

        # 連絡手段
        if soup.find("form"):
            result["contacts"].append("フォーム")
        if re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", html):
            result["contacts"].append("メール")
        if re.search(r"\d{2,4}[\-\s]?\d{2,4}[\-\s]?\d{4}", html):
            result["contacts"].append("電話")

        # ブログ/お知らせページも個別確認
        if not result["last_update"]:
            for path in ["/news", "/blog", "/topics", "/information", "/info"]:
                try:
                    page.goto(url.rstrip("/") + path, wait_until="domcontentloaded", timeout=10000)
                    time.sleep(1)
                    sub_text = BeautifulSoup(page.content(), "html.parser").get_text()
                    date = extract_date(sub_text)
                    if date:
                        result["last_update"] = date
                        break
                except:
                    continue

    except Exception as e:
        print(f"  [サイト調査エラー] {url}: {e}")

    return result


# =============================
# 日付抽出・停止月数計算
# =============================

def extract_date(text):
    patterns = [
        r"\d{4}年\d{1,2}月\d{1,2}日",
        r"\d{4}/\d{1,2}/\d{1,2}",
        r"\d{4}-\d{1,2}-\d{1,2}",
        r"\d{4}\.\d{1,2}\.\d{1,2}",
    ]
    for pattern in patterns:
        found = re.findall(pattern, text)
        if found:
            return found[0]
    return None


def months_since(date_str):
    if not date_str:
        return None
    patterns = [
        r"(\d{4})年(\d{1,2})月(\d{1,2})",
        r"(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})",
    ]
    for pattern in patterns:
        m = re.search(pattern, date_str)
        if m:
            try:
                dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                return (datetime.now() - dt).days / 30
            except:
                pass
    return None


# =============================
# スコアリング
# =============================

def score(is_wp, last_update, has_hiring, contacts):
    months = months_since(last_update)
    has_contact = bool(contacts)

    # ブログ運用代行スコア
    if is_wp:
        if months is not None and months >= 6 and has_hiring and has_contact:
            blog = "A"
        elif months is not None and months >= 6:
            blog = "B"
        elif months is not None and months >= 3:
            blog = "C"
        elif months is None:
            blog = "B"  # WordPressあるがブログなし
        else:
            blog = "D"  # 活発更新中
    else:
        blog = "D"

    # HP制作スコア
    if not is_wp:
        if has_hiring and has_contact:
            hp = "A"
        elif has_contact:
            hp = "B"
        elif has_hiring:
            hp = "C"
        else:
            hp = "D"
    else:
        hp = "—"

    return blog, hp


# =============================
# メイン処理
# =============================

def main():
    print("=" * 55)
    print("  営業リスト自動生成スクリプト（Playwright版）")
    print(f"  実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  目標: A判定 {TARGET_A_COUNT}件 が集まるまで継続")
    print("=" * 55)

    all_leads = []
    a_leads = []
    seen_names = set()
    total_checked = 0

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

        query_index = 0
        indeed_start = 0

        while len(a_leads) < TARGET_A_COUNT and total_checked < MAX_COMPANIES:
            query = SEARCH_QUERIES[query_index % len(SEARCH_QUERIES)]

            print(f"\n▼ Indeed検索: {query}（start={indeed_start}）")
            companies = search_indeed(page, query, RESULTS_PER_PAGE * 3)

            # ページオフセット調整
            offset_companies = []
            page_start = indeed_start
            temp_page = context.new_page()
            url_str = f"https://jp.indeed.com/jobs?q={query}&start={page_start}"
            temp_page.goto(url_str, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            soup = BeautifulSoup(temp_page.content(), "html.parser")
            name_elems = soup.find_all("span", {"data-testid": "company-name"})
            loc_elems = soup.find_all("div", {"data-testid": "text-location"})
            for i, elem in enumerate(name_elems):
                name = elem.get_text(strip=True)
                loc = loc_elems[i].get_text(strip=True) if i < len(loc_elems) else ""
                offset_companies.append({"name": name, "location": loc})
            temp_page.close()

            unique = [c for c in offset_companies if c["name"] not in seen_names]
            for c in unique:
                seen_names.add(c["name"])

            if not unique:
                # 次のクエリへ
                query_index += 1
                indeed_start = 0
                continue

            for company in unique:
                if len(a_leads) >= TARGET_A_COUNT or total_checked >= MAX_COMPANIES:
                    break

                name = company["name"]
                location = company["location"]
                total_checked += 1

                print(
                    f"\n  [{total_checked}調査済 / A判定{len(a_leads)}件] "
                    f"{name}（{location}）"
                )

                # URL取得
                url = find_company_url(page, name, location)
                if not url:
                    print(f"    → URL取得失敗。スキップ")
                    continue
                print(f"    → {url}")

                # サイト調査
                site = investigate_site(page, url)
                months = months_since(site["last_update"])
                blog_score, hp_score = score(
                    site["is_wp"],
                    site["last_update"],
                    site["has_hiring"],
                    site["contacts"],
                )

                print(
                    f"    WP:{site['is_wp']} "
                    f"/ 最終更新:{site['last_update']} "
                    f"/ 採用:{site['has_hiring']} "
                    f"/ 連絡:{site['contacts']}"
                )
                print(f"    → ブログ代行:{blog_score} / HP制作:{hp_score}")

                lead = {
                    "取得日": datetime.now().strftime("%Y-%m-%d"),
                    "会社名": name,
                    "所在地": location,
                    "URL": url,
                    "WordPress": "✅" if site["is_wp"] else "×",
                    "ブログ最終更新": site["last_update"] or "不明",
                    "更新停止（月）": round(months, 1) if months else "不明",
                    "採用ページ": "あり" if site["has_hiring"] else "なし",
                    "連絡手段": " / ".join(site["contacts"]) if site["contacts"] else "なし",
                    "ブログ運用代行": blog_score,
                    "HP制作営業": hp_score,
                }
                all_leads.append(lead)

                if blog_score == "A" or hp_score == "A":
                    a_leads.append(lead)
                    print(f"    ★ A判定追加！ 現在 {len(a_leads)}/{TARGET_A_COUNT}件")

                time.sleep(1)

            indeed_start += 10
            if indeed_start > 100:
                query_index += 1
                indeed_start = 0

        browser.close()

    # CSV出力（A判定のみ別ファイルにも出力）
    if all_leads:
        # 全件CSV
        file_exists = os.path.exists(OUTPUT_FILE)
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=all_leads[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(all_leads)

        # A判定のみCSV
        a_output = OUTPUT_FILE.replace(".csv", "_A_only.csv")
        with open(a_output, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=all_leads[0].keys())
            writer.writeheader()
            writer.writerows(a_leads)

        print("\n" + "=" * 55)
        print(f"  完了")
        print(f"  総調査数: {total_checked}社")
        print(f"  A判定（最強リスト）: {len(a_leads)}件 → {a_output}")
        print(f"  全件ログ: {OUTPUT_FILE}")
        print("=" * 55)


if __name__ == "__main__":
    main()
