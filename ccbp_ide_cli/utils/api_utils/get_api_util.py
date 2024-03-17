import os

from ccbp_ide_cli.constants.api_end_points import \
    GET_ACCESS_TOKENS_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import CCBP_CREDENTIALS_FILE_PATH, \
    CCBP_IDE_ENV_KEY_NAME, CCBP_IDE_API_CUSTOM_BACKEND_URL_CONFIG, \
    CCBP_IDE_API_DEFAULT_BACKEND_URL, CCBP_IDE_TOKEN_KEY_NAME, \
    CCBP_ENV_FILE_PATH
from ccbp_ide_cli.constants.enums import EnvValueEnum
from ccbp_ide_cli.utils.api_utils.api_util import APIUtil
from ccbp_ide_cli.utils.api_utils.mock_api_util import MockApiUtil
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path, \
    write_key_value_pair_into_file


def get_api_util():
    ide_token = os.environ.get("USER_IDE_TOKEN", "")
    if not ide_token:
        ide_token = get_value_for_key_from_file_path(
                CCBP_CREDENTIALS_FILE_PATH, CCBP_IDE_TOKEN_KEY_NAME)
    if ide_token is None:
        return
    env = os.environ.get("BACKEND_STAGE", "")
    if not env:
        env = get_value_for_key_from_file_path(
            CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)

    base_url = CCBP_IDE_API_CUSTOM_BACKEND_URL_CONFIG.get(
        env, CCBP_IDE_API_DEFAULT_BACKEND_URL,
    )

    if base_url == EnvValueEnum.mock.value:
        return MockApiUtil()

    api_util = APIUtil(base_url=base_url, auth_tokens=None)
    url_suffix = GET_ACCESS_TOKENS_END_POINT_CONFIG["end_point"]
    method = GET_ACCESS_TOKENS_END_POINT_CONFIG["method"]
    body = {"ide_token": ide_token}

    auth_tokens = _get_authtokens(
        api_util, method, url_suffix, body, env)
    if auth_tokens:
        if env is None:
            _set_env(EnvValueEnum.ccbp_prod.value)
        return APIUtil(base_url, auth_tokens=auth_tokens)

    # Requesting to Kossip Prod as token not found in CCBP Prod
    base_url = CCBP_IDE_API_CUSTOM_BACKEND_URL_CONFIG[
        EnvValueEnum.kossip_prod.value]
    api_util.base_url = base_url
    auth_tokens = api_util.api_request(
        method=method, url_suffix=url_suffix, body=body)
    _set_env(EnvValueEnum.kossip_prod.value)
    return APIUtil(base_url, auth_tokens=auth_tokens)


def _get_authtokens(api_util, method, url_suffix, body, env):
    from ccbp_ide_cli.exceptions.exceptions import InvalidApiRequestException
    try:
        on_fail_invoke_callbacks = env is not None
        auth_tokens = api_util.api_request(
            method=method, url_suffix=url_suffix, body=body,
            on_fail_invoke_callbacks=on_fail_invoke_callbacks)

    except InvalidApiRequestException as exception:
        if env is not None:  # Authenticating to specific environment
            raise

        from ccbp_ide_cli.exceptions.exception_messages import \
            INVALID_IDE_TOKEN_RES_STATUS
        if exception.res_status != INVALID_IDE_TOKEN_RES_STATUS:
            # Other than Token not found res status
            raise
    else:
        return auth_tokens


def _set_env(env):
    write_key_value_pair_into_file(
        CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME, env)
