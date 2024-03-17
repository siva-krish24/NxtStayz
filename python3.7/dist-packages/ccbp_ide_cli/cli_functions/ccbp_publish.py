import uuid
import os
from pathlib import Path

from typing import Dict

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.config.config import CCBP_NPM_INSTALL_CMD, \
    CCBP_NPM_BUILD_CMD, CCBP_WORKSPACE_TEMP_DIR_PATH, \
    CCBP_PUBLISH_BUILD_FOLDER_NAME
from ccbp_ide_cli.constants.enums import SpinnerStatusEnum
from ccbp_ide_cli.exceptions.exception_messages import \
    SUBMISSION_FOLDER_IS_EMPTY, BUILD_FOLDER_IS_EMPTY, CANNOT_PUBLISH_SESSION, \
    NODE_MODULES_INSTALLATION_FAILED, BUILD_COMMAND_FAILED
from ccbp_ide_cli.exceptions.exceptions import CannotPublishException, \
    NodeModulesInstallationFailedException
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import is_empty_folder, clear_directory_or_file, remove_all_files_in_directory_except_node_modules,\
    extract_zip_file_to_dir


class CCBPPublish(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_publish(self, session_display_id: str, domain_url: str):
        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(session_display_id)
        user_directory_path = session_details["user_directory_path"]

        if not session_details["is_deploy_enabled"]:
            raise CannotPublishException(CANNOT_PUBLISH_SESSION)

        if is_empty_folder(session_details["user_directory_path"]):
            raise CannotPublishException(SUBMISSION_FOLDER_IS_EMPTY)

        s3_credentials = self._get_cognito_credentials()
        directory_url = self._zip_user_directory(
            s3_credentials, user_directory_path, session_display_id)

        self._ccbp_publish(directory_url, domain_url, session_display_id)

    def _get_cognito_credentials(self):
        from ccbp_ide_cli.constants.api_end_points import \
            GET_S3_CREDENTIALS_END_POINT_CONFIG
        end_point_details = GET_S3_CREDENTIALS_END_POINT_CONFIG
        s3_credentials = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=None)
        return s3_credentials

    def _zip_user_directory(
            self, s3_credentials: Dict[str, str],
            user_directory_path: str, ide_session_id: str) -> str:

        temp_folder_path = self._build_user_directory_code(
            user_directory_path)
        build_folder_path = str(
            Path(temp_folder_path) / CCBP_PUBLISH_BUILD_FOLDER_NAME)
        if is_empty_folder(build_folder_path):
            raise CannotPublishException(BUILD_FOLDER_IS_EMPTY)

        from ccbp_ide_cli.utils.s3_utils import UploadFileToS3Util
        upload_util = UploadFileToS3Util(s3_credentials, ide_session_id)
        print("Zipping ...")
        zip_file_path = upload_util.create_zip_file(
            build_folder_path, temp_folder_path)
        print("Publishing ...")
        s3_url = upload_util.upload_zip_file_to_private_s3(
            zip_file_path, str(uuid.uuid4()), temp_folder_path, True)

        return s3_url

    def _ccbp_publish(self, directory_url: str, domain_url: str,
                      session_display_id: str):
        body = {
            "repository_url": directory_url,
            "domain_url": domain_url,
            "session_display_id": session_display_id,
        }

        from ccbp_ide_cli.constants.api_end_points import \
            PUBLISH_REPOSITORY_END_POINT_CONFIG
        end_point_details = PUBLISH_REPOSITORY_END_POINT_CONFIG

        self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=body)

        from ccbp_ide_cli.utils.output_utils import print_success_message
        print_success_message(
            f"Published Successfully!. Check at https://{domain_url}")

    def _build_user_directory_code(self, user_directory_path: str) -> str:

        from ccbp_ide_cli.utils.progressbar_util import ProgressBarInFiniteUtil
        from ccbp_ide_cli.utils.s3_utils import UploadFileToS3Util

        temp_folder = self.get_question_specific_temp_folder(
            user_directory_path)
        temp_folder_path = str(Path(
            CCBP_WORKSPACE_TEMP_DIR_PATH) / temp_folder)
        Path(temp_folder_path).mkdir(parents=True, exist_ok=True)
        remove_all_files_in_directory_except_node_modules(temp_folder_path)
        zip_file_path = str(Path(temp_folder_path) / "temp_user_code.zip")

        spinner = ProgressBarInFiniteUtil("Preparing files to publish ...")
        UploadFileToS3Util.prepare_zip_file(zip_file_path, user_directory_path,
                                            show_progress_bar=False)
        extract_zip_file_to_dir(temp_folder_path, zip_file_path)
        clear_directory_or_file(zip_file_path)

        os.chdir(temp_folder_path)
        exec_status = os.system(CCBP_NPM_INSTALL_CMD)  # noqa: S605
        if self.is_command_execution_status_failed(exec_status):
            self.clear_existing_node_modules(user_directory_path)
            spinner.stop(SpinnerStatusEnum.failure.value)
            raise NodeModulesInstallationFailedException(
                message=NODE_MODULES_INSTALLATION_FAILED)
        exec_status = os.system(CCBP_NPM_BUILD_CMD)  # noqa: S605
        if self.is_command_execution_status_failed(exec_status):
            spinner.stop(SpinnerStatusEnum.failure.value)
            raise CannotPublishException(BUILD_COMMAND_FAILED)
        os.chdir(user_directory_path)

        spinner.stop()

        return temp_folder_path
