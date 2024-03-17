import json

import sentry_sdk

from ccbp_ide_cli.constants.config.logging_config import LOGGER, \
    CCBP_CLI_LOGENTRIES_TOKEN
from ccbp_ide_cli.constants.constants import DEFAULT_DATETIME_FORMAT
from ccbp_ide_cli.constants.enums import UserActionStatus
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util


def log_data(**logging_data):

    if not CCBP_CLI_LOGENTRIES_TOKEN:
        return

    try:
        api_util = get_api_util()
        user_id = api_util.user_id if api_util.user_id else ""
    except Exception:
        user_id = ""

    from ccbp_ide_cli.cli_functions.ccbp_version import CCBPVersion
    ccbp_version = CCBPVersion()
    version = ccbp_version.get_version()
    version = "" if version is None else version

    start_timestamp = logging_data["start_timestamp"]
    end_timestamp = logging_data["end_timestamp"]

    logging_data.update(
        {
            "start_timestamp": start_timestamp.strftime(
                DEFAULT_DATETIME_FORMAT),
            "end_timestamp": end_timestamp.strftime(
                DEFAULT_DATETIME_FORMAT),
            "user_id": user_id,
            "version": version,
        },
    )

    status = logging_data["status"]
    log_message = json.dumps(logging_data)

    with sentry_sdk.push_scope() as scope:
        scope.user = {"id": user_id}
        if status == UserActionStatus.failure.value:
            is_critical = _is_critical(logging_data["failure_reason"])
            if is_critical:
                LOGGER.critical(msg=log_message)
            else:
                LOGGER.error(msg=log_message)
        else:
            LOGGER.info(msg=log_message)
        sentry_sdk.flush()


def _is_critical(failure_reason: str) -> bool:

    from ccbp_ide_cli.constants.config.logging_config \
        import CRITICAL_LOG_CONFIG
    return failure_reason in CRITICAL_LOG_CONFIG
