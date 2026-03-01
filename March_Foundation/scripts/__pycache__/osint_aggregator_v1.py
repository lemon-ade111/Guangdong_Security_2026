import csv
import logging
import time
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Target: Industry-standard security news portal for compliance auditing.
# Adhere to ethical scraping guidelines.

SOURCE_URL = "https://www.sec-wiki.com/news"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 10
DELAY_SECONDS = 2
OUTPUT_FILE = "intelligence.csv"


@dataclass
class Article:
    title: str
    url: str


def fetch_html(url: str) -> str:
    time.sleep(DELAY_SECONDS)
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def parse_titles(html: str, base_url: str) -> List[Article]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    results: List[Article] = []
    if not table:
        return results

    for row in table.find_all("tr"):
        link = row.find("a", href=True)
        if not link:
            continue
        title = " ".join(link.get_text(strip=True).split())
        if not title:
            continue
        href = link.get("href", "").strip()
        if not href:
            continue
        full_url = urljoin(base_url, href)
        results.append(Article(title=title, url=full_url))

    seen = set()
    unique_results: List[Article] = []
    for item in results:
        key = (item.title, item.url)
        if key in seen:
            continue
        seen.add(key)
        unique_results.append(item)
    return unique_results


def save_to_csv(records: List[Article], file_path: str) -> None:
    with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "url"])
        writer.writeheader()
        for record in records:
            writer.writerow({"title": record.title, "url": record.url})


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    try:
        logging.info("开始抓取 Sec-Wiki 新闻列表")
        html = fetch_html(SOURCE_URL)
        records = parse_titles(html, SOURCE_URL)
        if not records:
            logging.warning("未解析到任何文章标题，请检查页面结构或 URL")
        save_to_csv(records, OUTPUT_FILE)
        logging.info("已保存 %s 条记录到 %s", len(records), OUTPUT_FILE)
        if records:
            print(f"成功捕获安全情报：{records[0].title}")
        return 0
    except requests.exceptions.RequestException as exc:
        logging.error("网络请求失败，请检查连接或目标地址。错误信息：%s", exc)
        return 1
    except Exception as exc:
        logging.exception("程序运行出现异常：%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
