"""
会社名リストからURLを一括取得（Yahoo Japan経由）
"""

import csv
import time
import urllib.parse
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

EXCLUDED_DOMAINS = [
    "indeed", "hellowork", "doda", "mynavi", "rikunabi",
    "en-japan", "jobcan", "wikipedia", "facebook",
    "instagram", "twitter", "x.com", "linkedin",
    "hotpepper", "townwork", "baitoru", "kaigokensaku",
    "job-gear", "workin", "an-job", "standby", "jopus",
    "kyujinbox", "yahoo", "google", "bing", "recruit",
    "wantedly", "glassdoor", "careercross", "jobsinjapan",
]

COMPANIES = [
    ("橘建設 株式会社", "石川県金沢市"),
    ("東洋測量設計 株式会社", "栃木県宇都宮市"),
    ("三品造園土木 株式会社", "栃木県鹿沼市"),
    ("株式会社 水戸建設", "埼玉県さいたま市"),
    ("株式会社 荒川瀧石", "埼玉県秩父市"),
    ("秩父測量設計 株式会社", "埼玉県秩父市"),
    ("株式会社 八楠", "神奈川県横浜市"),
    ("鳥越工業 株式会社", "岡山県真庭市"),
    ("株式会社 水光エンジニア", "広島県広島市"),
    ("ロードライン 株式会社", "佐賀県小城市"),
    ("梅村建工 株式会社", "岐阜県岐阜市"),
    ("駿河技建 株式会社", "静岡県静岡市"),
    ("株式会社 東海維持管理工業", "愛知県名古屋市"),
    ("斉藤井出建設 株式会社", "北海道足寄郡"),
    ("中村建設 株式会社", "北海道余市郡"),
    ("株式会社 アルク", "茨城県水戸市"),
    ("株式会社 中村鐵工所", "茨城県取手市"),
    ("株式会社 山中設備工業", "栃木県栃木市"),
    ("株式会社シンコウ", "埼玉県さいたま市"),
    ("株式会社 ロックシステム", "神奈川県横浜市"),
    ("株式会社 笹山植木", "神奈川県横浜市"),
    ("三興電機 株式会社", "神奈川県横浜市"),
    ("株式会社 山木組", "新潟県村上市"),
    ("中谷商事 株式会社", "石川県金沢市"),
    ("新井電気工事株式会社", "長野県飯田市"),
    ("株式会社 桐山組", "岐阜県大垣市"),
    ("丸満産業 株式会社", "愛知県海部郡"),
    ("株式会社 水研設備", "滋賀県東近江市"),
    ("株式会社楠工務店", "大阪府大阪市"),
    ("出水断熱", "大阪府八尾市"),
    ("株式会社 ever", "兵庫県姫路市"),
    ("株式会社 シカタ", "兵庫県高砂市"),
    ("株式会社 富田工務店", "香川県高松市"),
    ("株式会社 久保造園", "佐賀県佐賀市"),
    ("株式会社 紅葉建設", "滋賀県東近江市"),
    ("株式会社 立花建設", "青森県八戸市"),
    ("有限会社 桐生建設", "山形県米沢市"),
    ("神室工業 株式会社", "山形県最上郡"),
    ("株式会社 ハトリ", "埼玉県羽生市"),
    ("古谷建設 株式会社", "千葉県山武郡"),
]

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "urls-found.csv")


def find_url(page, company_name, location):
    query = urllib.parse.quote(f"{company_name} {location} 公式サイト")
    search_url = f"https://search.yahoo.co.jp/search?p={query}"

    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)

        soup = BeautifulSoup(page.content(), "html.parser")

        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if (
                href.startswith("http")
                and not any(exc in href.lower() for exc in EXCLUDED_DOMAINS)
            ):
                return href

    except Exception as e:
        print(f"  [エラー] {company_name}: {e}")

    return "取得失敗"


def main():
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

        for i, (name, location) in enumerate(COMPANIES, 1):
            print(f"[{i:02d}/{len(COMPANIES)}] {name}（{location}）")
            url = find_url(page, name, location)
            print(f"  → {url}")
            results.append({"会社名": name, "所在地": location, "URL": url})
            time.sleep(1)

        browser.close()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["会社名", "所在地", "URL"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n完了：{OUTPUT_FILE} に保存しました")
    found = sum(1 for r in results if r["URL"] != "取得失敗")
    print(f"取得成功：{found}/{len(COMPANIES)}件")


if __name__ == "__main__":
    main()
