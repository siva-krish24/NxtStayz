import os

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.api_end_points import \
    UPDATE_CCBP_IDE_ACTIVE_SESSION, DOWNLOAD_USER_BACKUP_CODE_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import \
    (CCBP_IDE_V2_NXTWAVE_USER_ID, \
     CCBP_WORKSPACE_PATH)
from ccbp_ide_cli.exceptions.exception_messages import CANNOT_UPDATE_SESSION
from ccbp_ide_cli.exceptions.exceptions import \
    CannotUpdateSessionException
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import \
    download_file_and_extract_file, \
    remove_all_files_in_directory_except_node_modules


class CCBPUpdate(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_update(self, reusable_session_id: str, current_session_id: str):
        print("Updating started", reusable_session_id)
        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        reusable_session_details = self.get_session_details(reusable_session_id)

        if not reusable_session_details.get("is_reusable_session"):
            raise CannotUpdateSessionException(CANNOT_UPDATE_SESSION)

        metadata = self.get_metadata_details(
            reusable_session_details["metadata"])
        if metadata:
            resource_id = metadata.get("resource_id")
            self.validate_user_resource(resource_id)

        user_directory_path = reusable_session_details["user_directory_path"]

        active_session_id = reusable_session_details.get(
            "active_session_display_id")
        if active_session_id and active_session_id == current_session_id:
            print(f"Current session {current_session_id} is already active")
            return

        s3_credentials = self.get_cognito_credentials()
        user_id = self.api_util.user_id

        if active_session_id:
            print("Backup current code started")
            backup_s3_key = self.get_user_session_code_s3_key(
                user_id, s3_credentials["folder_name"], active_session_id)
            self.backup_current_code(
                s3_credentials, user_directory_path, backup_s3_key,
                active_session_id)
            remove_all_files_in_directory_except_node_modules(
                user_directory_path)
            print("Backup current code completed")

        s3_key = self.get_user_session_code_s3_key(
            user_id, s3_credentials["folder_name"], current_session_id)
        try:
            current_session_code_url = self._get_presigned_code_url(s3_key)
            self._extract_boiler_plate_with_out_user_consent(
                current_session_code_url, user_directory_path)
            print(f"Updated user existing code for session "
                  f"{current_session_id}")
        except Exception:
            current_session_details = self.get_session_details(
                current_session_id)
            current_session_code_url = \
                current_session_details["boilerplate_code_s3_url"]
            self._extract_boiler_plate_with_out_user_consent(
                current_session_code_url, user_directory_path)
            print(f"Updated boilerplate code for session "
                  f"{current_session_id}")

        self._update_active_session_id(current_session_id)
        print("Updated")

    def _update_active_session_id(self, current_session_id: str):

        drop_instance_id = os.environ.get("DROP_INSTANCE_ID")
        self.api_util.api_request(
            url_suffix=UPDATE_CCBP_IDE_ACTIVE_SESSION["end_point"],
            method=UPDATE_CCBP_IDE_ACTIVE_SESSION["method"], body={
                "drop_id": drop_instance_id,
                "active_session_display_id": current_session_id,
            })

    @staticmethod
    def _extract_boiler_plate_with_out_user_consent(
            boiler_plate_url: str, user_director_path: str):

        download_file_and_extract_file(
            dir_path=user_director_path, zip_file_url=boiler_plate_url)
        os.system(
            f"sudo chown -R {CCBP_IDE_V2_NXTWAVE_USER_ID}:"  # noqa: S605
            f"{CCBP_IDE_V2_NXTWAVE_USER_ID} {CCBP_WORKSPACE_PATH}")

    def _get_presigned_code_url(self, s3_key: str) -> str:

        response = self.api_util.api_request(
            url_suffix=DOWNLOAD_USER_BACKUP_CODE_END_POINT_CONFIG["end_point"],
            method=DOWNLOAD_USER_BACKUP_CODE_END_POINT_CONFIG["method"], body={
                "s3_key": s3_key,
            })
        return response["download_code_url"]
