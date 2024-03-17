import os

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.output_utils import print_success_message


class CCBPBackup(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_backup(self):
        print("Backup started")
        session_id = os.environ.get("DROP_SESSION_ID")
        if not session_id:
            return
        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(
            session_id)
        if session_details.get("is_reusable_session"):
            active_session_id = session_details.get(
                "active_session_display_id")
        else:
            active_session_id = session_id

        if not active_session_id:
            return
        print("Active session id: ", active_session_id)

        user_directory_path = session_details["user_directory_path"]
        s3_credentials = self.get_cognito_credentials()
        user_id = self.api_util.user_id

        backup_s3_key = self.get_user_session_code_s3_key(
            user_id, s3_credentials["folder_name"], active_session_id)
        self.backup_current_code(
            s3_credentials, user_directory_path, backup_s3_key,
            active_session_id)
        print_success_message("Backup Success")
