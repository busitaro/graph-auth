import json
import requests
import os

from .errors import ApiError

output_json = "auth.json"


def auth(client_id: str, client_secret: str, tenant_id: str):
    """
    Params
    -------
    client_id: str
        認証に使用するクライアントID
    client_secret: str
        認証に使用するクライアントシークレット
    tenant_id: str
        認証対象のテナントID
    """
    # 認証リクエスト
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    res = requests.post(url, data=data, headers=headers)

    # 認証失敗の場合
    if res.status_code != 200:
        raise ApiError(res)

    # ファイル出力
    with open(f"./{output_json}", "w", encoding="utf-8") as f:
        f.write(res._content.decode("utf-8"))

    return res


def read_token() -> str:
    """
    Returns
    -------
    0: str
        取得済みのトークン
    """
    # 認証ファイルのチェック
    if not os.path.exists(f"./{output_json}"):
        raise ValueError("not authenticated yet")

    # jsonとして読み込んで、トークンを読出し
    with open(f"./{output_json}", "r", encoding="utf-8") as f:
        auth_dict = json.load(f)

    return auth_dict["access_token"]
