from ccbp_ide_cli.constants.config.config \
    import CCBP_UPLOAD_ZIP_FILE_SIZE_MAX_LIMIT
from ccbp_ide_cli.utils.call_back_functions import clear_ide_token_config

IDE_TOKEN_NOT_CONFIGURED = \
    ('IDE Token not configured. Use \"ccbp authenticate <IDE TOKEN>.\" '    # noqa: S105
     "Refer: https://learning.ccbp.in/installations/ide-setup-instructions")

API_RESPONSE_FAILED_MESSAGE = ("Server Error, Please try again. "
                               "Contact our support team if the error persists.")
API_REQUEST_FAILED_MESSAGE = ("Unable to connect to the Server, Please check"
                              " that you have a reliable internet connection.")

RESOURCE_NOT_UNLOCKED = "Oops! You don't have access to the session."

DOWNLOAD_ZIP_FILE_FAILED = \
    ("Unable to download the zip file. Please check that you have a reliable "
     "internet connection. Contact our support team if the error persists.")

EXTRACT_ZIP_FILE_FAILED = ("Something went wrong, Please try again."
                           " Contact our support team if the error persists. "
                           "[Error Code 6]")

UNKNOWN_EXCEPTION_OCCURRED = ("Something went wrong, Please try again."
                              " Contact our support team if the error persists. "
                              "[Error Code 7]")

CANNOT_SUBMIT_SESSION = "You can't submit your code for a learning session."

SUBMISSION_FOLDER_IS_EMPTY = ("Your code is empty. "
                              "Please add some files and try again.")

TESTS_RESULTS_NOT_GENERATED = \
    ("Couldn't run tests on your code, Please try again."
     " Contact our support team if the error persists.")

QUESTION_SUBMISSION_FAILED = \
    ("Couldn't submit your code, "
     "Please check that you have a reliable internet connection."
     " Contact our support team if the error persists.")

SUBMISSION_SIZE_EXCEEDED = \
    ("Submission size exceeded, It should be < {} MB. "
        "Please remove any unnecessary files and submit again"
        .format(int(CCBP_UPLOAD_ZIP_FILE_SIZE_MAX_LIMIT / (1024 * 1024))))

IDE_TOKEN_EXPIRED = \
    ("Your IDE token has expired/invalid. "  # noqa: S105
     'Use \"ccbp authenticate <IDE TOKEN>.\" to update it. '
     "Refer: https://learning.ccbp.in/installations/ide-setup-instructions")

QUESTION_NOT_STARTED = \
    ("You haven't started this question. "
    "Please open the question on the advanced learning portal and "
    "follow the instructions.")

TIME_LEFT_TO_UNLOCK_SOLUTIONS = ("The solution is locked for you."
                                 " {} seconds left to unlock.")

SOLUTION_NOT_FOUND = \
    ("You have entered an incorrect solution id. "
     "Please copy the command correctly from the Advanced Learning Portal.")

SESSION_IS_NOT_A_SOLUTION = \
    ("You have entered an incorrect solution id. "
     "Please copy the command correctly from the Advanced Learning Portal.")

CANNOT_START_SESSION = \
    ("You have entered an incorrect command. "
     "Please copy the command correctly from the Advanced Learning Portal.")

INVALID_QUESTION_ID = \
    "Couldn't submit your code. Please contact our support team. [Error Code 8]"

UNABLE_TO_GET_VERSION_DETAILS = \
    "Version details not found. Please contact our support team. [Error Code 9]"

BUILD_FOLDER_IS_EMPTY = ("Couldn't publish your code. "
                         "Please contact our support team. [Error Code 10]")

CANNOT_PUBLISH_SESSION = "You can't publish your code for this session."

SYSTEM_TIME_NOT_UP_TO_DATE = ("Your system time is not upto date with the "
                              "network time. Update your date & time in system "
                              "settings and Restart your system to proceed further.")

NODE_MODULES_INSTALLATION_FAILED = \
    ("Unable to install requirements for this session, please try again. "
        "Contact our support team if the error persists.")

BUILD_COMMAND_FAILED \
    = ("Couldn't build your code. Please try to run 'yarn build' "
        "in your project before publishing the code.")

CANNOT_UPDATE_SESSION = CANNOT_START_SESSION

# Override 4xx messages
API_4XX_EXCEPTION_RES_STATUS_WISE_MESSAGE_CONFIG = {
    # TODO : This will raise when user submit before starting the question.
    #  cant we put message `Please Start the question`
    "USER_QUESTIONS_DOES_NOT_EXIST":
        "Something went wrong, please contact our support team. [Error Code 1]",
    "INVALID_USER_RESPONSE":
        "Something went wrong, please contact our support team. [Error Code 2]",
    "INVALID_QUESTION_IDS":
        "Something went wrong, please contact our support team. [Error Code 3]",
    "INVALID_IDE_BASED_CODING_QUESTIONS":
        "Something went wrong, please contact our support team. [Error Code 4]",
    "INVALID_QUESTION_ID":
        "Something went wrong, please contact our support team. [Error Code 5]",
    "IDE_TOKEN_EXPIRED": IDE_TOKEN_EXPIRED,
    "INVALID_IDE_TOKEN": IDE_TOKEN_EXPIRED,
    "INVALID_DOMAIN_URL":
        "Domain URL format is incorrect."
        " Use <yourdomain>.ccbp.tech as input. Ex: fm.ccbp.tech. "
        "A maximum of 15 characters is allowed.",
    "INVALID_REPOSITORY_URL": "Something went wrong, please try again. "
                              "Contact our support team if the error persists.",
    "DOMAIN_URL_ALREADY_EXISTS": "Given domain URL is already taken. Choose "
                                 "another one.",
    "PUBLISH_REPOSITORY_EXCEPTION": "Something went wrong, please try again. "
                                    "Contact our support team if the error "
                                    "persists. [Error Code 11]",
    "INVALID_IDE_SESSION_ID": CANNOT_START_SESSION,
}

# 4xx Exceptions Callback functions
API_4XX_EXCEPTION_RES_STATUS_WISE_CALLBACK_FUNCTIONS = {
    "IDE_TOKEN_EXPIRED": clear_ide_token_config,
    "INVALID_IDE_TOKEN": clear_ide_token_config,
}

# Exceptions ResStatus
API_REQUEST_FAILED_RES_STATUS = "API_REQUEST_FAILED"
API_REQUEST_TIMEOUT_RES_STATUS = "API_REQUEST_TIMEOUT"
API_CONNECTION_ERROR_RES_STATUS = "API_CONNECTION_ERROR"
EMPTY_API_RESPONSE_RES_STATUS = "EMPTY_API_RESPONSE"
INTERNAL_SERVER_ERROR_RES_STATUS = "INTERNAL_SERVER_ERROR"
UNKNOWN_EXCEPTION_OCCURRED_RES_STATUS = "UNKNOWN_EXCEPTION_OCCURRED"
INVALID_IDE_TOKEN_RES_STATUS = "INVALID_IDE_TOKEN"  # noqa: S105
