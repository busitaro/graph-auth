import requests
import json


class ApiError(Exception):
    def __init__(self, response: requests.models.Response):
        self.status_code = response.status_code
        self.reason = response.reason
        _content = json.loads(response._content.decode("utf-8"))
        if "error_description" in _content:
            self.message = _content["error_description"]
        else:
            self.message = _content["error"]["message"]
        self.raw_response = response


class NotAuthorizedError(Exception):
    pass
