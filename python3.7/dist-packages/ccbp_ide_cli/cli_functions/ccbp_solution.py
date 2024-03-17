import json
from pathlib import Path

from ccbp_ide_cli.cli_functions.ccbp_start import CCBPStart
from ccbp_ide_cli.constants.api_end_points import \
    IDE_CODING_QUESTION_SOLUTIONS_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import \
    CCBP_AUTOMATE_USER_DIRECTORY_OPEN_IN_IDE_FILE_PATH
from ccbp_ide_cli.constants.enums import SessionTypeEnum, IDETypeEnum
from ccbp_ide_cli.exceptions.exception_messages import \
    SESSION_IS_NOT_A_SOLUTION
from ccbp_ide_cli.exceptions.exceptions import InvalidSessionException
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import \
    write_content_into_file, clear_directory_or_file


class CCBPSolution(CCBPStart):

    def __init__(self):
        super().__init__()
        self.api_util = None

    @exception_handling_decorator
    def ccbp_solution(self, session_display_id: str):

        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(session_display_id)

        metadata = self.get_metadata_details(session_details["metadata"])
        question_id = None
        is_invalid_session = False
        if metadata:
            session_type = metadata["session_type"]
            if session_type == SessionTypeEnum.solution.value:
                question_id = metadata["question_id"]
            else:
                is_invalid_session = True
        else:
            is_invalid_session = True

        if is_invalid_session:
            raise InvalidSessionException(SESSION_IS_NOT_A_SOLUTION)

        if question_id:
            self._validate_solution_access(question_id, session_display_id)
            self._extract_boiler_plate(
                    session_details["boilerplate_code_s3_url"],
                    session_details["user_directory_path"],
                    message="Downloading Solution ...")

            if session_details.get("ide_type") == IDETypeEnum.ccbp_ide.value:
                self._create_file_with_parent_process(
                    session_details["user_directory_path"])

    def _validate_solution_access(
            self, question_id: str, session_display_id: str):

        from ccbp_ide_cli.exceptions.exceptions import \
            QuestionNotStartedException, \
            SolutionUnlockingTimeNotCompletedException, \
            SolutionNotFoundException
        from ccbp_ide_cli.exceptions.exception_messages import \
            QUESTION_NOT_STARTED, TIME_LEFT_TO_UNLOCK_SOLUTIONS, \
            SOLUTION_NOT_FOUND

        question_solutions = self._get_solutions(question_id)
        question_solution = question_solutions["solutions_details"][0]

        solution_details = question_solution["solution_details"]
        if not solution_details:
            raise QuestionNotStartedException(QUESTION_NOT_STARTED)

        time_left = solution_details[
            "time_left_to_unlock_solutions_in_seconds"]
        if time_left > 0:
            raise SolutionUnlockingTimeNotCompletedException(
                TIME_LEFT_TO_UNLOCK_SOLUTIONS.format(time_left))

        is_solution_found = False
        for solution in solution_details["solutions"]:
            if solution["session_details"]["session_display_id"] \
                    == session_display_id:
                is_solution_found = True

        if not is_solution_found:
            raise SolutionNotFoundException(SOLUTION_NOT_FOUND)

    def _get_solutions(self, question_id: str):
        end_point_details = IDE_CODING_QUESTION_SOLUTIONS_END_POINT_CONFIG

        body = {"question_ids": [question_id]}
        solutions = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=body)
        return solutions

    @staticmethod
    def _create_file_with_parent_process(user_directory_path: str):
        import os
        parent_process_id = os.getppid()

        file_path = str(Path(
            CCBP_AUTOMATE_USER_DIRECTORY_OPEN_IN_IDE_FILE_PATH) /
            f"{parent_process_id}_solution.json")
        clear_directory_or_file(file_path)
        content = json.dumps(
            {
                "recentRoots": [user_directory_path],
            },
        )
        write_content_into_file(file_path, content)
