import logging
import os

from logentries import LogentriesHandler

from ccbp_ide_cli.constants.config.config import CCBP_ENV_FILE_PATH, \
    CCBP_IDE_ENV_KEY_NAME
from ccbp_ide_cli.constants.enums import EnvValueEnum
from ccbp_ide_cli.exceptions.exception_messages import \
    API_REQUEST_FAILED_RES_STATUS, EMPTY_API_RESPONSE_RES_STATUS, \
    INTERNAL_SERVER_ERROR_RES_STATUS, UNKNOWN_EXCEPTION_OCCURRED_RES_STATUS
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path


# Stage wise Logentries Token Config
env = get_value_for_key_from_file_path(
        CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)
if env == EnvValueEnum.mock.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_MOCK",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.local.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_LOCAL",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.otg_beta.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_OTG_BETA",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.otg_gamma.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_OTG_GAMMA",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.ccbp_beta.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_OTG_BETA",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.ccbp_gamma.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_OTG_GAMMA",
        "718b0b28-5b46-493c-bfae-0d2567bcfc5a")
elif env == EnvValueEnum.kossip_beta.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_KOSSIP_BETA",
        "91454b02-0bb4-4c2f-8e76-59e63ed86516")
elif env == EnvValueEnum.kossip_gamma.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_KOSSIP_GAMMA",
        "91454b02-0bb4-4c2f-8e76-59e63ed86516")
elif env == EnvValueEnum.kossip_prod.value:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_KOSSIP_PROD",
        "53362bd0-9cdc-4137-82af-6fd6fdff89ad")
else:
    CCBP_CLI_LOGENTRIES_TOKEN = os.environ.get(
        "CCBP_CLI_LOGENTRIES_TOKEN_OTG_PROD",
        "d3e8e66b-9a36-4001-9fad-344ec03bd608")

# Critical Exception Config
CRITICAL_LOG_CONFIG = [
    API_REQUEST_FAILED_RES_STATUS,
    EMPTY_API_RESPONSE_RES_STATUS,
    INTERNAL_SERVER_ERROR_RES_STATUS,
    UNKNOWN_EXCEPTION_OCCURRED_RES_STATUS,
    "CannotDownloadFileException",
    "CannotExtractZipFileException",
    "SubmissionUploadFailedException",
    "INVALID_USER_RESPONSE",
    "INVALID_QUESTION_IDS",
    "INVALID_IDE_BASED_CODING_QUESTIONS",
    "INVALID_QUESTION_ID",
]

# Logentries Configuration
LOGGER = logging.getLogger("logentries")
LOGGER.propagate = False
LOGGER.setLevel(logging.INFO)

logentries_handler = LogentriesHandler(
    CCBP_CLI_LOGENTRIES_TOKEN, verbose=False)
logentries_handler.setLevel(logging.INFO)
le_format = '{"timestamp":"%(asctime)s", \
    "level": "%(levelname)s", "message": %(message)s}'
logentries_handler.setFormatter(
    fmt=logging.Formatter(fmt=le_format))

LOGGER.addHandler(logentries_handler)
