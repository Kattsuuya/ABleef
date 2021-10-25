# ABleef

Notionデータベースに書いた今日のBleeeeeefingをSlackに投稿する。

## Installation

**1. Notion APIのトークンの取得とデータベースの設定**

1. [Notion Developersのガイド](https://developers.notion.com/docs/getting-started)にしたがってインテグレーションを作成する。
2. `Internal Integration Token` をコピーして.envファイルに記入する。
3. データベースを作成し、URLからDatabase IDをコピーして.envファイルに記入する。
4. Notion APIのバージョン（ `2021-08-16` ）を.envファイルに記入する。

**2. Slack APIのトークンの取得**

1. [slack api](https://api.slack.com/apps)にアクセスする。
2. `Create New App` をクリックし、`App Name` に任意の名前を入力して、`Development Slack Workspace` で導入したい先のワークスペースを選択する。
3. 遷移先ページ左側のメニューから `OAuth & Permissions` をクリックする。
4. `Add an OAuth Scope` をクリックし、 `chat:write` を選択する。
5. ページトップの `Install to Workspace` をクリックする。
6. `許可する` をクリックする。
7. `OAuth Access Token` をコピーして.envファイルに記入する。
8. 投稿したいSlackチャンネル（#から始まる文字列）を.envファイルに記入する。

**3. プロジェクトのインストール**

```bash
git clone https://github.com/KindMaple/ABleef.git
cd ABleef
poetry install
```

## Usage

```bash
poetry shell
python3
>>> from ableef.lib import post_daily_bleeeeeefing
>>> post_daily_bleeeeeefing()
```
