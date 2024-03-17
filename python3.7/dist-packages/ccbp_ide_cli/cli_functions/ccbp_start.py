import json
from pathlib import Path

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.api_end_points import \
    START_CODING_QUESTION_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import CCBP_USER_INPUT_OPTIONS, \
    CCBP_USER_DIRECTORY_ALREADY_EXIST_USER_INPUT_MESSAGE, \
    CCBP_AUTOMATE_USER_DIRECTORY_OPEN_IN_IDE_FILE_PATH
from ccbp_ide_cli.constants.enums import SessionTypeEnum, \
    IDETypeEnum
from ccbp_ide_cli.exceptions.exception_messages import \
    CANNOT_START_SESSION
from ccbp_ide_cli.exceptions.exceptions import InvalidSessionException
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import \
    create_dir, download_file_and_extract_file, is_empty_folder, \
    clear_directory_or_file, write_content_into_file
from ccbp_ide_cli.utils.input_utils import get_input_from_user
from ccbp_ide_cli.utils.progressbar_util import ProgressBarInFiniteUtil


class CCBPStart(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_start(self, session_display_id: str):

        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(session_display_id)

        metadata = self.get_metadata_details(session_details["metadata"])
        is_invalid_session = False
        if metadata:
            resource_id = metadata.get("resource_id")
            self.validate_user_resource(resource_id)

            session_type = metadata["session_type"]
            if session_type == SessionTypeEnum.question.value:
                question_id = metadata["question_id"]
                self._start_question(question_id)
            elif session_type != SessionTypeEnum.ide_playground.value:
                is_invalid_session = True

        if is_invalid_session:
            raise InvalidSessionException(CANNOT_START_SESSION)

        self._extract_boiler_plate(
                session_details["boilerplate_code_s3_url"],
                session_details["user_directory_path"])

        if session_details.get("ide_type") == IDETypeEnum.ccbp_ide.value:
            self._create_file_with_parent_process(
                session_details["user_directory_path"])

    def _start_question(self, question_id: str):

        end_point_details = START_CODING_QUESTION_END_POINT_CONFIG

        body = {"question_id": question_id}
        self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=body)

    @staticmethod
    def _extract_boiler_plate(
            boiler_plate_url: str, user_director_path, message=None):
        if not message:
            message = "Downloading BoilerPlate Code ..."

        can_extract_boilerplate = is_empty_folder(user_director_path)
        if not can_extract_boilerplate:
            user_input = get_input_from_user(
                CCBP_USER_DIRECTORY_ALREADY_EXIST_USER_INPUT_MESSAGE,
                CCBP_USER_INPUT_OPTIONS)
            if user_input == CCBP_USER_INPUT_OPTIONS[0]:
                can_extract_boilerplate = True
        if can_extract_boilerplate:
            clear_directory_or_file(user_director_path)
            create_dir(user_director_path)

            spinner = ProgressBarInFiniteUtil(message)
            download_file_and_extract_file(
                dir_path=user_director_path, zip_file_url=boiler_plate_url,
                spinner=spinner)
            spinner.stop()

    @staticmethod
    def _create_file_with_parent_process(user_directory_path: str):
        import os
        parent_process_id = os.getppid()

        file_path = str(Path(
            CCBP_AUTOMATE_USER_DIRECTORY_OPEN_IN_IDE_FILE_PATH) /
            f"{parent_process_id}.json")

        content = json.dumps(
            {
                "recentRoots": [user_directory_path],
            },
        )
        write_content_into_file(file_path, content)
