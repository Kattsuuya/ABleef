import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from lib import post_daily_bleeeeeefing


def trigger(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None. The output is written to Cloud Logging.
    """

    post_daily_bleeeeeefing()


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
