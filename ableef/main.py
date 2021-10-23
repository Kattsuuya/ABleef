import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from icecream import ic

API_BASE_URL = "https://api.notion.com/v1"

if __name__ == "__main__":
    # .envファイルを読み込み、環境変数として扱う
    dotenv_path: Path = Path().parent / ".env"
    if dotenv_path.exists():
        # .envがあるときはそっちを読み込む
        load_dotenv(dotenv_path)
    NOTION_TOKEN: str = os.environ.get("NOTION_TOKEN")
    NOTION_DATABASE_ID: str = os.environ.get("NOTION_DATABASE_ID")
    NOTION_VERSION: str = os.environ.get("NOTION_VERSION")

    """ ページ一覧を取得する """
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    response: requests.Response = requests.post(
        url=f"{API_BASE_URL}/databases/{NOTION_DATABASE_ID}/query",
        headers=headers,
    )
    assert response.status_code == 200
    pages: List[Dict[str, Any]] = response.json()["results"]
    for page in pages:
        ic(page["properties"]["名前"]["title"][0]["plain_text"])
        ic(page["url"])

    """ 特定のページの情報を取得する """
    page_id: str = pages[2]["id"]
    ic(page_id)
    response = requests.get(
        url=f"{API_BASE_URL}/pages/{page_id}",
        headers=headers,
    )
    assert response.status_code == 200
    ic(response.json())

    """ ページの内容を取得する """
    response = requests.get(
        url=f"{API_BASE_URL}/blocks/{page_id}/children",
        headers=headers,
    )
    assert response.status_code == 200
    ic(response.json())
