from ccbp_ide_cli.constants.config.config import CCBP_CREDENTIALS_FILE_PATH, \
    CCBP_IDE_TOKEN_KEY_NAME, \
    CCBP_USER_INPUT_OPTIONS, CCBP_TOKEN_EXIST_USER_INPUT_MESSAGE, \
    CCBP_ENV_FILE_PATH
from ccbp_ide_cli.exceptions.exception_messages import IDE_TOKEN_NOT_CONFIGURED
from ccbp_ide_cli.exceptions.exceptions import \
    IDETokenNotConfiguredException
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path, \
    clear_directory_or_file
from ccbp_ide_cli.utils.input_utils import get_input_from_user
from ccbp_ide_cli.utils.output_utils import print_success_message


class CCBPLogout:

    @exception_handling_decorator
    def ccbp_logout(self):
        existing_ide_token = get_value_for_key_from_file_path(
            CCBP_CREDENTIALS_FILE_PATH, CCBP_IDE_TOKEN_KEY_NAME)
        if existing_ide_token:
            user_input = get_input_from_user(
                CCBP_TOKEN_EXIST_USER_INPUT_MESSAGE,
                CCBP_USER_INPUT_OPTIONS)

            if user_input == CCBP_USER_INPUT_OPTIONS[0]:
                clear_directory_or_file(CCBP_CREDENTIALS_FILE_PATH)
                clear_directory_or_file(CCBP_ENV_FILE_PATH)
                print_success_message("\nLogout Success")
        else:
            raise IDETokenNotConfiguredException(
                message=IDE_TOKEN_NOT_CONFIGURED)
