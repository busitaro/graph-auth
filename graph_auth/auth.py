import json
import requests
import os
from functools import wraps

from .errors import ApiError
from .errors import NotAuthorizedError


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
        raise NotAuthorizedError("not authenticated yet")

    # jsonとして読み込んで、トークンを読出し
    with open(f"./{output_json}", "r", encoding="utf-8") as f:
        auth_dict = json.load(f)

    return auth_dict["access_token"]


def reauth(client_id: str, client_secret: str, tenant_id: str):
    """
    APIが認証切れで失敗した場合に、再認証を行うデコレータ

    Params
    -------
    client_id: str
        認証に使用するクライアントID
    client_secret: str
        認証に使用するクライアントシークレット
    tenant_id: str
        認証対象のテナントID
    """

    def reauth_decorator(func):
        """
        Params
        -------
        func:
            APIを実行する関数
        """

        @wraps(func)
        def reauth_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiError as ex:
                if ex.status_code == 401 and ex.reason == "Unauthorized":
                    # 認証を実行し、処理を再実行
                    auth(client_id, client_secret, tenant_id)
                    return func(*args, **kwargs)
                else:
                    raise ex
            except NotAuthorizedError as ex:
                auth(client_id, client_secret, tenant_id)
                return func(*args, **kwargs)

        return reauth_wrapper

    return reauth_decorator
