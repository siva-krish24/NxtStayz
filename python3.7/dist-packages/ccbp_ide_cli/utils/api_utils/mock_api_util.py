import json

import pkgutil
from typing import Optional


class MockApiUtil:

    def __init__(self):
        self.base_url = None
        self.user_id = None
        self.access_token = None

    @staticmethod
    def api_request(url_suffix: str, method: Optional[str] = None, body: Optional[dict] = None):  # noqa: ARG004
        data = pkgutil.get_data(__name__, "mock_responses.json")
        mock_responses = json.loads(data)
        return mock_responses.get(url_suffix, {})
