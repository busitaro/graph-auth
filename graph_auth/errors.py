import requests
import json


class ApiError(Exception):
    def __init__(self, response: requests.models.Response):
        self.status_code = response.status_code
        self.reason = response.reason
        self.message = json.loads(response._content.decode("utf-8"))["error"]["message"]
        self.raw_response = response


class NotAuthorizedError(Exception):
    pass
