import os
import re
import traceback
import zipfile
import logging
from pathlib import Path
from typing import Dict, List

from ccbp_ide_cli.constants.config.config \
    import CCBP_UPLOAD_ZIP_FILE_SIZE_MAX_LIMIT, \
    CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME, S3_UPLOAD_END_PATH
from ccbp_ide_cli.constants.enums import EnvValueEnum

from ccbp_ide_cli.utils.file_utils import get_file_size, \
    clear_directory_or_file, is_file_path_exist, \
    get_value_for_key_from_file_path, is_dir_path_exist

from ccbp_ide_cli.exceptions.exception_messages import \
    QUESTION_SUBMISSION_FAILED, SUBMISSION_SIZE_EXCEEDED, \
    SYSTEM_TIME_NOT_UP_TO_DATE
from ccbp_ide_cli.exceptions.exceptions import SubmissionUploadFailedException, \
    CannotSubmitQuestionException, SystemTimeNotUpToDateException
from ccbp_ide_cli.utils.progressbar_util import ProgressBarFiniteUtil

logger = logging.getLogger(__name__)


class UploadFileToS3Util:

    def __init__(self, s3_credentials: Dict[str, str], ide_session_id: str):
        self.AWS_STORAGE_BUCKET_NAME = s3_credentials["bucket_name"]
        self.AWS_S3_REGION_NAME = s3_credentials["region_name"]
        self.AWS_ACCESS_KEY_ID = s3_credentials["aws_access_key_id"]
        self.AWS_SECRET_ACCESS_KEY = s3_credentials["secret_access_key"]
        self.MEDIAFILES_LOCATION = s3_credentials["folder_name"]
        self.AWS_SESSION_TOKEN = s3_credentials["aws_session_token"]
        self.ide_session_id = ide_session_id

    def create_zip_file(self, user_directory_path: str, temp_folder_path: str,
                        clear_temp_folder_on_failed=False) -> str:

        zip_file_path = str(Path(temp_folder_path) / "temp_user_code.zip")

        self.prepare_zip_file(zip_file_path, user_directory_path)
        self._validate_zip_file_size(zip_file_path, temp_folder_path,
                                     clear_temp_folder_on_failed)
        return zip_file_path

    def upload_zip_file_to_private_s3(
        self, zip_file_path: str, file_name: str,
        temp_folder_path: str, clear_temp_folder_on_failed=False,
        s3_key=None) -> str:

        progress_bar = ProgressBarFiniteUtil(zip_file_path)
        try:
            s3_url = self._upload_zip_file_to_private_s3(
                zip_file_path, file_name, progress_bar, s3_key)
        except Exception as exception:

            progress_bar.fail()
            env = get_value_for_key_from_file_path(
                CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)
            if env == EnvValueEnum.mock.value:
                print("s3 upload skipped", exception)
                s3_url = ''
            else:
                if clear_temp_folder_on_failed:
                    clear_directory_or_file(temp_folder_path)
                stack_trace = ''.join(traceback.format_tb(
                    exception.__traceback__))
                stack_trace = f"{exception}: \n{stack_trace}"
                message_str = repr(exception)
                if "RequestTimeTooSkewed" in message_str:
                    raise SystemTimeNotUpToDateException(
                        message=SYSTEM_TIME_NOT_UP_TO_DATE,
                        stack_trace=stack_trace)
                raise SubmissionUploadFailedException(
                    message=QUESTION_SUBMISSION_FAILED,
                    stack_trace=stack_trace)
        return s3_url

    # pylint: disable=consider-using-with
    @staticmethod
    def prepare_zip_file(zip_file_path, temp_folder_path,
                         show_progress_bar=True):
        progress_bar = None
        if show_progress_bar:
            progress_bar = ProgressBarFiniteUtil(temp_folder_path)
        os.chdir(temp_folder_path)

        import subprocess
        is_git_initialized = is_dir_path_exist(
            str(Path(temp_folder_path) / ".git"))
        if not is_git_initialized:
            os.system("git init -q")  # noqa: S605, S607
        os.system(
            "git config --global --add safe.directory " + temp_folder_path)  # noqa: S605
        process = subprocess.Popen(
            'git ls-files -o --exclude-standard -c',  # noqa: S607
            shell=True, stdout=subprocess.PIPE)  # noqa: S602
        file_paths = process.communicate()[0].decode("utf-8")
        file_paths = file_paths.strip("\n").split("\n")

        with zipfile.ZipFile(
            zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file_obj:
            for file_path in file_paths:
                if is_file_path_exist(file_path):
                    zip_file_obj.write(file_path)
                    if progress_bar:
                        progress_bar.update(get_file_size(zip_file_path))

        if progress_bar:
            progress_bar.finish()

    def _upload_zip_file_to_private_s3(
        self, zip_file_path, file_name, progress_bar,
        destination_file_path):

        import boto3
        if not destination_file_path:
            destination_file_path = self._get_destination_file_path(file_name)

        s3 = boto3.resource('s3', region_name=self.AWS_S3_REGION_NAME,
                            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                            aws_session_token=self.AWS_SESSION_TOKEN)

        s3.meta.client.upload_file(
            zip_file_path, self.AWS_STORAGE_BUCKET_NAME, destination_file_path,
            Callback=progress_bar.update)
        progress_bar.finish()
        return self._format_s3_url(
            self.AWS_S3_REGION_NAME, self.AWS_STORAGE_BUCKET_NAME,
            destination_file_path)

    @staticmethod
    def _format_s3_url(
        bucket_region: str, bucket_name: str,
        destination_file_path: str) -> str:

        s3_url = "https://{1}.s3-{0}.amazonaws.com/{2}".format(  # noqa: UP030
            bucket_region, bucket_name, destination_file_path)
        return s3_url

    def _get_destination_file_path(self, file_name: str):

        s3_upload_path = self.MEDIAFILES_LOCATION

        destination_file_path = \
            s3_upload_path + '{}' if s3_upload_path.endswith('/') \
                else s3_upload_path + '/{}'

        destination_file_path = destination_file_path.format(
            S3_UPLOAD_END_PATH.format(self.ide_session_id, file_name))
        return destination_file_path

    @staticmethod
    def _validate_zip_file_size(zip_file_path: str, temp_folder_path: str,
                                clear_temp_folder_on_failed: bool):
        if get_file_size(zip_file_path) > CCBP_UPLOAD_ZIP_FILE_SIZE_MAX_LIMIT:
            if clear_temp_folder_on_failed:
                clear_directory_or_file(temp_folder_path)
            raise CannotSubmitQuestionException(
                message=SUBMISSION_SIZE_EXCEEDED)

    # Not Using
    @staticmethod
    def _get_file_name_to_ignore(user_directory_path: str) -> List[str]:
        exclude_files = []
        if not is_file_path_exist(
            str(Path(user_directory_path) / ".gitignore")):
            return []

        with Path(
                Path(user_directory_path) / ".gitignore").open() as file:
            lines = file.readlines()
            for line in lines:
                new_line = line
                if new_line and not new_line.startswith('#'):
                    if new_line.startswith("*"):
                        new_line = " " + new_line
                    new_line = new_line.lstrip("/")
                    new_line = new_line.strip("\n")
                    new_line = new_line.replace(".", "\\.")
                    if new_line:
                        exclude_files.append(new_line.strip("\n"))
        return exclude_files

    # Not Using
    @staticmethod
    def _is_path_should_exclude(
            arcname: str, exclude_file_names: List[str]) -> bool:

        if exclude_file_names and \
                re.findall('|'.join(exclude_file_names), arcname):
            return True
        return False
