import datetime
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv


def fetch_daily_content(block_id: str) -> List[Dict[str, Any]]:
    setup()
    response: requests.Response = requests.get(
        url=f"{API_BASE_URL}/blocks/{block_id}/children",
        headers=headers,
    )
    result: List[Dict[str, Any]] = response.json()["results"]
    return result


def fetch_daily_meta_info(date_: datetime.date) -> Dict[str, Any]:
    setup()
    # 特定の日付のみ取り出すためのフィルタクエリ
    query: Dict[str, Any] = {
        "filter": {
            "property": "日付",
            "date": {
                "equals": date_.strftime("%Y-%m-%d"),
            },
        },
    }
    response: requests.Response = requests.post(
        url=f"{API_BASE_URL}/databases/{NOTION_DATABASE_ID}/query",
        headers=headers,
        json=query,
    )
    # ステータスが200ではない場合のみレスポンスの詳細を標準エラー出力に表示する
    if response.status_code != 200:
        print(response.json(), file=sys.stderr)
    results: List[Dict[str, Any]] = response.json()["results"]
    return results[0]


def setup():
    global API_BASE_URL, NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_VERSION, headers
    API_BASE_URL = "https://api.notion.com/v1"
    # .envファイルを読み込み、環境変数として扱う
    dotenv_path: Path = Path().parent / ".env"
    if dotenv_path.exists():
        # .envがあるときはそっちを読み込む
        load_dotenv(dotenv_path)
    """ 環境変数からトークンなどを取得 """
    NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
    NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
    NOTION_VERSION = os.environ.get("NOTION_VERSION")

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
