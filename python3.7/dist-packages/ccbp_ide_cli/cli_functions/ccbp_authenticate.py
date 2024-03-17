from ccbp_ide_cli.constants.config.config import CCBP_CREDENTIALS_FILE_PATH, \
    CCBP_IDE_TOKEN_KEY_NAME, CCBP_TOKEN_ALREADY_EXIST_USER_INPUT_MESSAGE, \
    CCBP_USER_INPUT_OPTIONS
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path, \
    write_key_value_pair_into_file
from ccbp_ide_cli.utils.input_utils import get_input_from_user
from ccbp_ide_cli.utils.output_utils import print_success_message


class CCBPAuthenticate:

    api_util = None

    @exception_handling_decorator
    def ccbp_authenticate(self, ide_token: str):
        existing_ide_token = get_value_for_key_from_file_path(
            CCBP_CREDENTIALS_FILE_PATH, CCBP_IDE_TOKEN_KEY_NAME)
        if existing_ide_token:
            user_input = get_input_from_user(
                CCBP_TOKEN_ALREADY_EXIST_USER_INPUT_MESSAGE,
                CCBP_USER_INPUT_OPTIONS)

            if user_input == CCBP_USER_INPUT_OPTIONS[0]:
                self._authenticate_ide_token(ide_token)
        else:
            self._authenticate_ide_token(ide_token)

    def _authenticate_ide_token(self, ide_token: str):
        write_key_value_pair_into_file(
            CCBP_CREDENTIALS_FILE_PATH, CCBP_IDE_TOKEN_KEY_NAME, ide_token)

        self.api_util = get_api_util()
        print_success_message("\nAuthenticate Success")
