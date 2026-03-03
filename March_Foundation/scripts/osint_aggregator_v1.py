import sqlite3
import hashlib
import logging
import time
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# 目标：符合银行安全合规标准的OSINT情报聚合器
# 数据存储从CSV升级为SQLite，满足PIPL数据防篡改审计要求

SOURCE_URL = "https://www.sec-wiki.com/news"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 10
DELAY_SECONDS = 2
DATABASE_PATH = "/home/lemon/Guangdong_Security_2026/March_Foundation/scripts/audit_assets.db"


@dataclass
class Article:
    title: str
    url: str


def initialize_database() -> None:
    """初始化数据库表结构，确保满足合规审计要求"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            # 检查表是否存在，如果不存在则创建
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intel_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,  -- 唯一约束确保数据去重
                    risk_level TEXT DEFAULT 'PENDING',
                    audit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_integrity_hash TEXT NOT NULL  -- 数据完整性哈希，满足PIPL防篡改要求
                )
            """)
            # 确保url字段有唯一索引（如果不存在）
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_url_unique 
                ON intel_table(url)
            """)
            conn.commit()
            logging.info("数据库初始化完成，已配置UNIQUE约束和完整性哈希字段")
    except sqlite3.Error as e:
        logging.error("数据库初始化失败：%s", e)
        raise


def calculate_data_integrity_hash(title: str, url: str) -> str:
    """
    计算数据完整性哈希值，满足PIPL数据防篡改审计要求
    
    合规意义：通过SHA-256哈希算法，确保存储数据的完整性和不可篡改性
    任何对title或url的修改都会导致哈希值变化，便于审计追踪
    """
    data_string = f"{title}|{url}".encode('utf-8')
    integrity_hash = hashlib.sha256(data_string).hexdigest()
    return integrity_hash


def fetch_html(url: str) -> str:
    """
    获取网页HTML内容，包含合规的请求延迟控制
    
    合规意义：避免对目标网站造成过大访问压力，符合网络爬虫伦理规范
    """
    time.sleep(DELAY_SECONDS)
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def parse_titles(html: str, base_url: str) -> List[Article]:
    """
    解析HTML内容，提取文章标题和URL
    
    合规意义：仅提取公开信息，不涉及个人隐私数据采集
    """
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

    # 内存级去重，提高处理效率
    seen = set()
    unique_results: List[Article] = []
    for item in results:
        key = (item.title, item.url)
        if key in seen:
            continue
        seen.add(key)
        unique_results.append(item)
    return unique_results


def save_to_database(records: List[Article]) -> int:
    """
    将记录保存到SQLite数据库，实现ACID事务保障
    
    合规意义：
    1. 使用INSERT OR IGNORE实现数据库级去重，避免重复数据浪费审计资源
    2. 计算并存储数据完整性哈希，满足PIPL防篡改要求
    3. 事务处理确保数据一致性
    """
    inserted_count = 0
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            for record in records:
                # 计算数据完整性哈希
                integrity_hash = calculate_data_integrity_hash(record.title, record.url)
                
                # 使用INSERT OR IGNORE实现去重插入
                cursor.execute("""
                    INSERT OR IGNORE INTO intel_table (title, url, data_integrity_hash)
                    VALUES (?, ?, ?)
                """, (record.title, record.url, integrity_hash))
                
                if cursor.rowcount > 0:
                    inserted_count += 1
            
            conn.commit()
            logging.info("成功插入 %s 条新记录到数据库，跳过 %s 条重复记录", 
                        inserted_count, len(records) - inserted_count)
            
    except sqlite3.Error as e:
        logging.error("数据库操作失败：%s", e)
        # 事务自动回滚，确保数据一致性
        raise
    
    return inserted_count


def main() -> int:
    """
    主函数：执行完整的OSINT情报收集流程
    
    合规审计要点：
    1. 完整的异常处理机制，确保系统稳定性
    2. 数据完整性保障，满足监管要求
    3. 资源有效利用，避免重复数据存储
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    try:
        # 初始化数据库，确保表结构符合合规要求
        initialize_database()
        
        logging.info("开始抓取 Sec-Wiki 新闻列表")
        html = fetch_html(SOURCE_URL)
        records = parse_titles(html, SOURCE_URL)
        
        if not records:
            logging.warning("未解析到任何文章标题，请检查页面结构或 URL")
            return 0
        
        # 保存到数据库并获取实际插入数量
        inserted_count = save_to_database(records)
        
        logging.info("OSINT情报收集完成。共解析 %s 条记录，成功插入 %s 条新记录", 
                    len(records), inserted_count)
        
        if inserted_count > 0:
            print(f"成功捕获 {inserted_count} 条新的安全情报")
        else:
            print("未发现新的安全情报，所有记录均已存在")
            
        return 0
        
    except requests.exceptions.RequestException as exc:
        logging.error("网络请求失败，请检查连接或目标地址。错误信息：%s", exc)
        return 1
    except sqlite3.Error as exc:
        logging.error("数据库操作异常，请检查数据库文件权限或磁盘空间。错误信息：%s", exc)
        return 1
    except Exception as exc:
        logging.exception("程序运行出现未预期异常：%s", exc)
        return 1


if __name__ == "__main__":
    exit(main())