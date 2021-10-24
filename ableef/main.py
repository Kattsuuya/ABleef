import datetime
from typing import Any, Dict, List

from icecream import ic
from lib import fetch_daily_content, fetch_daily_meta_info, setup

if __name__ == "__main__":
    setup()
    page_info: Dict[str, Any] = fetch_daily_meta_info(datetime.date(2021, 10, 23))
    blocks: List[Dict[str, Any]] = fetch_daily_content(page_info["id"])
    ic(blocks)

    # import requests
    # from pathlib import Path
    # from dotenv import load_dotenv
    # import os
    # from typing import List

    # API_BASE_URL = "https://api.notion.com/v1"
    # # .envファイルを読み込み、環境変数として扱う
    # dotenv_path: Path = Path().parent / ".env"
    # if dotenv_path.exists():
    #     # .envがあるときはそっちを読み込む
    #     load_dotenv(dotenv_path)
    # """ 環境変数からトークンなどを取得 """
    # NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
    # NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
    # NOTION_VERSION = os.environ.get("NOTION_VERSION")

    # headers = {
    #     "Authorization": f"Bearer {NOTION_TOKEN}",
    #     "Content-Type": "application/json",
    #     "Notion-Version": NOTION_VERSION,
    # }
    # response: requests.Response = requests.get(
    #     url=f"{API_BASE_URL}/blocks/{block_id}/children",
    #     headers=headers,
    # )
    # blocks: List[Dict[str, Any]] = response.json()["results"]
    # ic(blocks)
