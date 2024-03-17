import os

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.config.config import CCBP_IDE_V2_NXTWAVE_USER_ID, \
    CCBP_WORKSPACE_PATH
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import \
    download_file_and_extract_file, clear_dir_recursively
from ccbp_ide_cli.utils.output_utils import print_success_message


class CCBPReset(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_reset(self, session_display_id: str):

        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(session_display_id)

        metadata = self.get_metadata_details(session_details["metadata"])
        if metadata:
            resource_id = metadata.get("resource_id")
            self.validate_user_resource(resource_id)

        user_directory_path = session_details["user_directory_path"]
        boilerplate_code_s3_url = session_details["boilerplate_code_s3_url"]

        if session_details.get("is_reusable_session"):
            active_session_id = session_details.get(
                "active_session_display_id")
            if active_session_id:
                active_session_details = self.get_session_details(
                    active_session_id)
                boilerplate_code_s3_url = active_session_details[
                    "boilerplate_code_s3_url"]
            else:
                print("No active session")
                return

        self._extract_boiler_plate_with_out_user_consent(
            boilerplate_code_s3_url, user_directory_path)
        print_success_message("Reset Success")

    @staticmethod
    def _extract_boiler_plate_with_out_user_consent(
            boiler_plate_url: str, user_director_path):

        clear_dir_recursively(user_director_path)
        download_file_and_extract_file(
            dir_path=user_director_path, zip_file_url=boiler_plate_url)
        os.system(f"sudo chown -R {CCBP_IDE_V2_NXTWAVE_USER_ID}:{CCBP_IDE_V2_NXTWAVE_USER_ID} {CCBP_WORKSPACE_PATH}")  # noqa: S605
