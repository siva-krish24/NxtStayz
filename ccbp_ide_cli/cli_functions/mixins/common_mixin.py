import json
import os
import uuid
from pathlib import Path
from typing import Dict, Union

from ccbp_ide_cli.constants.api_end_points import \
    GET_SESSION_DETAILS_END_POINT_CONFIG, \
    GET_USER_RESOURCE_COMPLETION_DETAILS_END_POINT_CONFIG, \
    GET_S3_CREDENTIALS_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import CCBP_IDE_TOKEN_KEY_NAME, \
    CCBP_CREDENTIALS_FILE_PATH, CCBP_WORKSPACE_PATH, \
    CCBP_WORKSPACE_TEMP_DIR_PATH, CCBP_IDE_V2_TEMP_DIR_PATH, \
    CCBP_IDE_V2_EXAM_ATTEMPT_ID_ENV, CCBP_IDE_V2_USER_EXAM_CODE_S3_KEY, \
    CCBP_IDE_V2_USER_PRACTICE_CODE_S3_KEY
from ccbp_ide_cli.exceptions.exception_messages import \
    IDE_TOKEN_NOT_CONFIGURED, RESOURCE_NOT_UNLOCKED
from ccbp_ide_cli.exceptions.exceptions import \
    IDETokenNotConfiguredException, UserResourceNotUnlockedException
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path, \
    clear_directory_or_file


class CommonMixin:
    api_util = None

    @staticmethod
    def validate_ide_token():

        ide_token = os.environ.get("USER_IDE_TOKEN", "")
        if ide_token:
            return

        existing_ide_token = get_value_for_key_from_file_path(
            CCBP_CREDENTIALS_FILE_PATH, CCBP_IDE_TOKEN_KEY_NAME)
        if existing_ide_token is None:
            raise IDETokenNotConfiguredException(
                message=IDE_TOKEN_NOT_CONFIGURED)

    def get_session_details(self, session_display_id: str) \
            -> Dict[str, Union[str, bool]]:

        drop_instance_id = os.environ.get("DROP_INSTANCE_ID")

        end_point_details = GET_SESSION_DETAILS_END_POINT_CONFIG
        body = {"ide_session_display_id": session_display_id,
                "drop_id": drop_instance_id}
        session_details = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=body)
        return session_details

    def validate_user_resource(self, resource_id: str):
        if not resource_id:
            return

        user_id = self.api_util.user_id
        body = {
            "user_id": user_id,
            "resource_ids": [resource_id],
        }
        end_point_details \
            = GET_USER_RESOURCE_COMPLETION_DETAILS_END_POINT_CONFIG
        user_resource_details = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=body)
        user_resource_details = user_resource_details[0]
        if user_resource_details["is_locked"] is True:
            raise UserResourceNotUnlockedException(
                message=RESOURCE_NOT_UNLOCKED)

    @staticmethod
    def get_metadata_details(metadata: str):
        try:
            metadata = json.loads(metadata)
        except Exception:
            return None

        return metadata

    @staticmethod
    def get_question_specific_temp_folder(user_directory_path: str) -> str:
        return user_directory_path.replace(CCBP_WORKSPACE_PATH, "")

    @staticmethod
    def is_command_execution_status_failed(status: int) -> bool:
        return os.WEXITSTATUS(status) != 0

    def clear_existing_node_modules(self, user_directory_path: str):

        session_tmp_path = self.get_question_specific_temp_folder(
            user_directory_path)
        node_modules_path = str(Path(
            CCBP_WORKSPACE_TEMP_DIR_PATH) / session_tmp_path / "node_modules")
        clear_directory_or_file(node_modules_path)

    def get_cognito_credentials(self):
        end_point_details = GET_S3_CREDENTIALS_END_POINT_CONFIG
        s3_credentials = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=None)
        return s3_credentials

    @staticmethod
    def backup_current_code(
            s3_credentials: Dict[str, str], user_directory_path: str,
            backup_s3_key: str, ide_session_id: str):

        temp_folder_path = str(Path(
            CCBP_IDE_V2_TEMP_DIR_PATH) / str(uuid.uuid4()))
        Path(temp_folder_path).mkdir(parents=True, exist_ok=True)

        from ccbp_ide_cli.utils.s3_utils import UploadFileToS3Util
        upload_util = UploadFileToS3Util(s3_credentials, ide_session_id)
        print("Zipping ...")
        zip_file_path = upload_util.create_zip_file(
            user_directory_path, temp_folder_path)
        print("Uploading ...")
        upload_util.upload_zip_file_to_private_s3(
            zip_file_path, str(uuid.uuid4()), temp_folder_path,
            s3_key=backup_s3_key)

    @staticmethod
    def get_user_session_code_s3_key(
            user_id: str, media_files_location, session_id: str) -> str:
        media_files_location = media_files_location.strip("/")
        exam_attempt_id = os.environ.get(CCBP_IDE_V2_EXAM_ATTEMPT_ID_ENV)
        if exam_attempt_id:
            return CCBP_IDE_V2_USER_EXAM_CODE_S3_KEY.format(
                media_files_location=media_files_location, user_id=user_id,
                exam_attempt=exam_attempt_id, session_id=session_id)

        return CCBP_IDE_V2_USER_PRACTICE_CODE_S3_KEY.format(
            media_files_location=media_files_location, user_id=user_id,
            session_id=session_id)
