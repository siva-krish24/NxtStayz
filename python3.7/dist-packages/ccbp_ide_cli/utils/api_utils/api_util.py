import json
import traceback
from json import JSONDecodeError
from typing import Optional, Dict, Any

import requests
from requests import Response, Timeout, ConnectionError

from ccbp_ide_cli.exceptions.exception_messages import \
    API_RESPONSE_FAILED_MESSAGE, \
    API_4XX_EXCEPTION_RES_STATUS_WISE_MESSAGE_CONFIG, \
    API_4XX_EXCEPTION_RES_STATUS_WISE_CALLBACK_FUNCTIONS, \
    API_REQUEST_FAILED_RES_STATUS, EMPTY_API_RESPONSE_RES_STATUS, \
    INTERNAL_SERVER_ERROR_RES_STATUS, API_CONNECTION_ERROR_RES_STATUS, \
    API_REQUEST_FAILED_MESSAGE, API_REQUEST_TIMEOUT_RES_STATUS
from ccbp_ide_cli.exceptions.exceptions import \
    InvalidApiRequestException


class APIUtil:

    def __init__(self, base_url: str,
                 auth_tokens: Optional[Dict[str, str]]):

        self.base_url = base_url
        self.access_token = ""
        self.user_id = None
        if auth_tokens:
            self.access_token = auth_tokens["access_token"]
            self.user_id = auth_tokens["user_id"]

    def api_request(self, url_suffix: str, method: str,
                    body: Optional[dict] = None,
                    on_fail_invoke_callbacks=True):

        api_url = self.base_url + "api/" + url_suffix
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }
        if body:
            body = self._format_request_body(body)

        try:
            response = self._api_request(
                api_url=api_url, headers=headers, method=method, body=body)
        except Timeout as exception:
            stack_trace = ''.join(traceback.format_tb(exception.__traceback__))
            stack_trace = f"{exception}: \n{stack_trace}"
            raise InvalidApiRequestException(
                message=API_REQUEST_FAILED_MESSAGE, stack_trace=stack_trace,
                res_status=API_REQUEST_TIMEOUT_RES_STATUS)
        except ConnectionError as exception:
            stack_trace = ''.join(traceback.format_tb(exception.__traceback__))
            stack_trace = f"{exception}: \n{stack_trace}"
            raise InvalidApiRequestException(
                message=API_REQUEST_FAILED_MESSAGE, stack_trace=stack_trace,
                res_status=API_CONNECTION_ERROR_RES_STATUS)
        except Exception as exception:
            stack_trace = ''.join(traceback.format_tb(
                exception.__traceback__))
            stack_trace = f"{exception}: \n{stack_trace}"
            failed_message = API_RESPONSE_FAILED_MESSAGE
            raise InvalidApiRequestException(
                message=failed_message,
                res_status=API_REQUEST_FAILED_RES_STATUS,
                stack_trace=stack_trace)
        self._validate_response(response, on_fail_invoke_callbacks)
        try:
            return json.loads(response.content)
        except JSONDecodeError:
            return response.content

    def _validate_response(self, response: Response,
                           on_fail_invoke_callbacks: bool):
        failed_message = API_RESPONSE_FAILED_MESSAGE
        is_failure_response = response is None

        if is_failure_response:
            raise InvalidApiRequestException(
                message=failed_message,
                res_status=EMPTY_API_RESPONSE_RES_STATUS)

        if 400 <= response.status_code < 500:  # noqa: PLR2004
            response_dict = json.loads(response.content)
            message = response_dict["response"]
            res_status = response_dict["res_status"]
            message = API_4XX_EXCEPTION_RES_STATUS_WISE_MESSAGE_CONFIG.get(
                res_status, message)
            if on_fail_invoke_callbacks:
                self._invoke_callback_function(res_status)
            raise InvalidApiRequestException(
                message=message, res_status=res_status)

        if response.status_code >= 500:  # noqa: PLR2004
            raise InvalidApiRequestException(
                message=failed_message,
                res_status=INTERNAL_SERVER_ERROR_RES_STATUS,
                stack_trace=response.content.decode("utf-8"),
            )

    @staticmethod
    def _api_request(
            api_url: str, headers: dict, method: str, body: str):

        from ccbp_ide_cli.constants.constants import \
            CCBP_API_REQUEST_CONNECTION_TIMEOUT_IN_SECONDS
        timeout = CCBP_API_REQUEST_CONNECTION_TIMEOUT_IN_SECONDS
        response = None
        if method == "PUT":
            response = requests.put(headers=headers, data=body, url=api_url,
                                    timeout=timeout)
        elif method == "POST":
            response = requests.post(headers=headers, data=body, url=api_url,
                                     timeout=timeout)
        elif method == "GET":
            response = requests.get(headers=headers, url=api_url,
                                    timeout=timeout)

        return response

    @staticmethod
    def _format_request_body(body: Dict[str, Any]) -> str:
        body = {
            "data": f"'{json.dumps(body)}'",
            "clientKeyDetailsId": 1,
        }
        return json.dumps(body)

    @staticmethod
    def _invoke_callback_function(res_status: str):
        callback_function = \
            API_4XX_EXCEPTION_RES_STATUS_WISE_CALLBACK_FUNCTIONS.get(
                res_status)
        if callback_function:
            callback_function()
