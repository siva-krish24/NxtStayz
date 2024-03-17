from ccbp_ide_cli.constants.enums import FileTypeEnum, EnvValueEnum
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path

CCBP_CREDENTIALS_FILE_PATH = "/home/nxtwave/.ccbp/credentials"
CCBP_ENV_FILE_PATH = "/home/nxtwave/.ccbp/env"
CCBP_AUTOMATE_USER_DIRECTORY_OPEN_IN_IDE_FILE_PATH = "/home/nxtwave/.theia/"
CCBP_VERSION_FILE_PATH = "/home/nxtwave/.ccbp/version-file.json"
CCBP_WORKSPACE_PATH = "/home/nxtwave/"
CCBP_WORKSPACE_TEMP_DIR_PATH = "/home/nxtwave/.tmp/"
CCBP_IDE_V2_TEMP_DIR_PATH = "/tmp/"  # noqa: S108


CCBP_IDE_TOKEN_KEY_NAME = "ide_token"   # noqa: S105
CCBP_IDE_ENV_KEY_NAME = "env"


CCBP_TOKEN_ALREADY_EXIST_USER_INPUT_MESSAGE \
    = ("You are already authenticated. "   # noqa: S105
        "Are you sure you want to re-authenticate? (y/n): ")
CCBP_TOKEN_EXIST_USER_INPUT_MESSAGE \
    = "Are you sure you want to logout? (y/n): "  # noqa: S105
CCBP_USER_DIRECTORY_ALREADY_EXIST_USER_INPUT_MESSAGE \
    = ("There already exists some code for this workspace previously, "
        "\nType(y) to replace your existing code or "
        "Type(n) to open the existing workspace (y/n): ")
CCBP_USER_INPUT_OPTIONS = ["y", "n"]

CCBP_IDE_API_DEFAULT_BACKEND_URL = "https://nkb-backend-ccbp-prod-apis.ccbp.in/"
CCBP_IDE_API_CUSTOM_BACKEND_URL_CONFIG = {
    EnvValueEnum.local.value: "http://localhost:8000/",
    EnvValueEnum.mock.value: EnvValueEnum.mock.value,
    EnvValueEnum.otg_beta.value: "https://nkb-backend-ccbp-beta.earlywave.in/",
    EnvValueEnum.otg_gamma.value: "https://nkb-backend-ccbp-gamma.earlywave.in/",
    EnvValueEnum.otg_prod.value: "https://nkb-backend-ccbp-prod-apis.ccbp.in/",
    EnvValueEnum.ccbp_beta.value: "https://nkb-backend-ccbp-beta.earlywave.in/",
    EnvValueEnum.ccbp_gamma.value: "https://nkb-backend-ccbp-gamma.earlywave.in/",
    EnvValueEnum.ccbp_prod.value: "https://nkb-backend-ccbp-prod-apis.ccbp.in/",
    EnvValueEnum.kossip_beta.value: "https://nkb-backend-beta.apigateway.in/",
    EnvValueEnum.kossip_gamma.value: "https://nkb-backend-10xiitian-gamma-apis.ibhubs.in/",
    EnvValueEnum.kossip_prod.value: "https://nkb-backend-10xiitian-prod-apis.ibhubs.in/",
}

CCBP_IDE_API_DEFAULT_BASE_URL = "https://learning.ccbp.in/"
CCBP_IDE_API_CUSTOM_BASE_URL_CONFIG = {
    EnvValueEnum.local.value: "http://localhost:8000/",
    EnvValueEnum.mock.value: EnvValueEnum.mock.value,
    EnvValueEnum.otg_beta.value: "https://learning-beta.ccbp.in/",
    EnvValueEnum.otg_gamma.value: "https://learning-gamma.ccbp.in/",
    EnvValueEnum.otg_prod.value: "https://learning.ccbp.in/",
    EnvValueEnum.ccbp_beta.value: "https://learning-beta.ccbp.in/",
    EnvValueEnum.ccbp_gamma.value: "https://learning-gamma.ccbp.in/",
    EnvValueEnum.ccbp_prod.value: "https://learning.ccbp.in/",
    EnvValueEnum.kossip_beta.value: "https://10xiitian-beta.ccbp.in/",
    EnvValueEnum.kossip_gamma.value: "https://10xiitian-gamma.ccbp.in/",
    EnvValueEnum.kossip_prod.value: "https://10xiitian.ccbp.in/",
}

env = get_value_for_key_from_file_path(
        CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)
if env == EnvValueEnum.mock.value:
    CCBP_NPM_INSTALL_CMD = "pnpm install --prefer-offline"
    CCBP_NPM_RUN_TEST_CMD = "npm run test"
else:
    CCBP_NPM_INSTALL_CMD = "pnpm install -s --prefer-offline"
    CCBP_NPM_RUN_TEST_CMD = "npm run test -s --no-progress > npm_run_log"

CCBP_NPM_BUILD_CMD = "pnpm run build"


CCBP_TEST_RESULT_FILES = [
    {
        "file_path": ".results",
        "file_type": FileTypeEnum.dir.value,
    },
]
CCBP_TEST_RESULT_JSON_FILE_PATH = ".results/results.json"

CCBP_QUESTION_SUBMISSION_URL_FORMAT \
    = "{base_url}ide-coding-submission/{question_id}/{submission_id}"

CCBP_UPLOAD_ZIP_FILE_SIZE_MAX_LIMIT = 10485760

S3_UPLOAD_END_PATH = "ide_submissions/{}/{}.zip"

# TODO : Need to update value
CCBP_PUBLISH_BUILD_FOLDER_NAME = "build"


# JAVA config
CCBP_JAVA_RUN_TEST_CMD = "mvn test"
CCBP_JAVA_TESTS_FOLDER_NAME = "src/test"
CCBP_JAVA_TESTS_RESULTS_FOLDER_PATH = "target/surefire-reports/"
CCBP_JAVA_TEST_CASE_IDS_FILE_PATH = "src/test/test_case_details.json"


CCBP_IDE_V2_NXTWAVE_USER_ID = 1002

CCBP_IDE_V2_USER_EXAM_CODE_S3_KEY = ("{media_files_location}/ccbp-ide-v2/users/"
                              "{user_id}/{exam_attempt}/{session_id}.zip")
CCBP_IDE_V2_USER_PRACTICE_CODE_S3_KEY = ("{media_files_location}/ccbp-ide-v2/users/"
                                  "{user_id}/{session_id}.zip")
CCBP_IDE_V2_EXAM_ATTEMPT_ID_ENV = "EXAM_ATTEMPT_ID"
