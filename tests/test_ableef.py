"""
TODO
fetch_daily_meta_info()
- [x] 1日分のBleeeeeefingページのメタ情報をJSONで取得する
    - [x] 2021-10-23のBleeeeeefingページのメタ情報をDictで返す
    - [x] 2021-10-24のBleeeeeefingページのメタ情報をDictで返す
fetch_daily_content()
- [ ] 1日分のBleeeeeefingページの内容をJSONで取得する
    - [x] 2021-10-23のBleeeeeefingページのメタ情報をDictで返す
    - [ ] 2021-10-24のBleeeeeefingページのメタ情報をDictで返す
"""
import datetime
from typing import Any, Dict, List

from ableef.lib import fetch_daily_content, fetch_daily_meta_info


class Test_fetch_meta_info:
    def test_2021_10_23のBleeeeeefingページのメタ情報をDictで返す(self):
        today: datetime.date = datetime.date(2021, 10, 23)
        result: Dict[str, Any] = fetch_daily_meta_info(today)
        assert result["properties"]["名前"]["title"][0]["plain_text"] == "2021-10-23"
        assert result["properties"]["日付"]["date"]["start"] == "2021-10-23"

    def test_2021_10_24のBleeeeeefingページのメタ情報をDictで返す(self):
        today: datetime.date = datetime.date(2021, 10, 24)
        result: Dict[str, Any] = fetch_daily_meta_info(today)
        assert result["properties"]["名前"]["title"][0]["plain_text"] == "2021-10-24"
        assert result["properties"]["日付"]["date"]["start"] == "2021-10-24"


class Test_fetch_daily_content:
    def test_2021_10_23のBleeeeeefingページのメタ情報をDictで返す(self):
        block_id: str = "43ca1c50-e2a3-4c8e-b936-4693e6e202c8"
        result: List[Dict[str, Any]] = fetch_daily_content(block_id)
        assert result[1]["type"] == "bulleted_list_item"
        assert result[1]["bulleted_list_item"]["text"][0]["plain_text"] == "hoge"

    def test_2021_10_24のBleeeeeefingページのメタ情報をDictで返す(self):
        block_id: str = "76659722-c2fc-4de4-ae72-92b4c2b306a9"
        result: List[Dict[str, Any]] = fetch_daily_content(block_id)
        assert result[1]["type"] == "bulleted_list_item"
        assert result[1]["bulleted_list_item"]["text"][0]["plain_text"] == "テスト駆動開発の練習"
