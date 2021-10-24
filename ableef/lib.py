import datetime
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def setup():
    global API_BASE_URL, NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_VERSION, SLACK_TOKEN, headers, slack_client
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
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    slack_client = WebClient(token=SLACK_TOKEN)


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


def fetch_daily_content(block_id: str) -> List[Dict[str, Any]]:
    setup()
    response: requests.Response = requests.get(
        url=f"{API_BASE_URL}/blocks/{block_id}/children",
        headers=headers,
    )
    result: List[Dict[str, Any]] = response.json()["results"]
    return result


def to_slack_format(contents: List[Dict[str, Any]]) -> str:
    if contents == []:
        return ""
    result: List[str] = []
    for content in contents:
        if content["type"] == "heading_2":
            result.append(f'*{content[content["type"]]["text"][0]["plain_text"]}*')
        elif content["type"] == "bulleted_list_item":
            result.append(f'・{content[content["type"]]["text"][0]["plain_text"]}')
        else:
            result.append(content[content["type"]]["text"][0]["plain_text"])
    return "\n".join(result)


class SlackResponseError(Exception):
    def __init__(self, status_code: int, data):
        self.status_code = status_code
        self.data = data

    def __str__(self):
        return f"{self.status_code=}\n{self.data=}"


def post_to_slack(message: str, channel: str) -> None:
    """
    Slackのbleeeeeefingチャンネルに投稿する
    Copied from https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
    """
    try:
        response = slack_client.chat_postMessage(channel=channel, text=message)
        if response.status_code != 200:
            raise SlackResponseError(response.status_code, response.data)
    except SlackResponseError as e:
        print(e)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
