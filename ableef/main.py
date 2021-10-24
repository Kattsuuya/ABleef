import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv


def main():
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

    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


if __name__ == "__main__":
    main()
