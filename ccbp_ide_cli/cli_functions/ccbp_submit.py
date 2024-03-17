import os
import uuid
from pathlib import Path
from typing import Dict, Tuple, List, Optional

from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.api_end_points import \
    GET_S3_CREDENTIALS_END_POINT_CONFIG, \
    SUBMIT_QUESTION_RESPONSES_END_POINT_CONFIG, \
    SUBMIT_QUESTION_RESPONSES_FOR_EXAM_END_POINT_CONFIG
from ccbp_ide_cli.constants.config.config import \
    CCBP_NPM_RUN_TEST_CMD, CCBP_TEST_RESULT_FILES, \
    CCBP_QUESTION_SUBMISSION_URL_FORMAT, \
    CCBP_NPM_INSTALL_CMD, CCBP_TEST_RESULT_JSON_FILE_PATH, \
    CCBP_IDE_API_CUSTOM_BASE_URL_CONFIG, CCBP_ENV_FILE_PATH, \
    CCBP_IDE_ENV_KEY_NAME, CCBP_IDE_API_DEFAULT_BASE_URL, \
    CCBP_WORKSPACE_TEMP_DIR_PATH, CCBP_JAVA_RUN_TEST_CMD, \
    CCBP_JAVA_TESTS_FOLDER_NAME, CCBP_JAVA_TESTS_RESULTS_FOLDER_PATH, \
    CCBP_IDE_V2_TEMP_DIR_PATH, CCBP_JAVA_TEST_CASE_IDS_FILE_PATH, \
    CCBP_IDE_V2_EXAM_ATTEMPT_ID_ENV
from ccbp_ide_cli.constants.enums import SessionTypeEnum, FileTypeEnum, \
    SpinnerStatusEnum, IDESessionTestTypeEnum, IDETypeEnum, EvaluationResult

from ccbp_ide_cli.exceptions.exception_messages import \
    CANNOT_SUBMIT_SESSION, SUBMISSION_FOLDER_IS_EMPTY, \
    TESTS_RESULTS_NOT_GENERATED, INVALID_QUESTION_ID, \
    NODE_MODULES_INSTALLATION_FAILED
from ccbp_ide_cli.exceptions.exceptions import \
    CannotSubmitQuestionException, TestsResultsNotGeneratedException, \
    NodeModulesInstallationFailedException
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import \
    is_empty_folder, download_file_and_extract_file, clear_directory_or_file, \
    copy_directory, is_file_path_exist, copy_file, get_file_content_as_json, \
    is_dir_path_exist, create_dir, get_value_for_key_from_file_path, \
    remove_all_files_in_directory_except_node_modules, extract_zip_file_to_dir
from ccbp_ide_cli.utils.java_test_utils import save_java_test_results, \
    save_java_test_results_with_incorrect_status
from ccbp_ide_cli.utils.output_utils import print_success_message, \
    get_right_tick, get_wrong_tick, print_failure_message
from ccbp_ide_cli.utils.progressbar_util import ProgressBarInFiniteUtil


class CCBPSubmit(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_submit(self, session_display_id: str):

        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        session_details = self.get_session_details(session_display_id)
        metadata = self.get_metadata_details(session_details["metadata"])
        if metadata:
            resource_id = metadata.get("resource_id")
            self.validate_user_resource(resource_id)

        if session_details["is_submit_enabled"] is False:
            raise CannotSubmitQuestionException(
                CANNOT_SUBMIT_SESSION)
        if is_empty_folder(session_details["user_directory_path"]):
            raise CannotSubmitQuestionException(SUBMISSION_FOLDER_IS_EMPTY)
        self._clear_existing_test_results(
            session_details["user_directory_path"])

        s3_credentials = self._get_cognito_credentials()
        submission_url = self._get_submission_url(
            s3_credentials, session_details, session_display_id)
        submission_id, question_id, test_case_details \
            = self._submit_question_results(submission_url, session_details)

        if submission_id:
            base_url = self._get_base_url()
            question_submission_url = CCBP_QUESTION_SUBMISSION_URL_FORMAT.format(
                base_url=base_url,
                submission_id=submission_id,
                question_id=question_id)
            print_success_message("\nOpen Submission URL : {}".format(
                question_submission_url))
        if test_case_details:
            self._print_test_case_details(test_case_details)

    def _get_cognito_credentials(self):

        end_point_details = GET_S3_CREDENTIALS_END_POINT_CONFIG
        s3_credentials = self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body=None)
        return s3_credentials

    def _get_submission_url(
        self, s3_credentials: Dict[str, str],
            session_details: Dict[str, str], ide_session_id: str) -> str:

        user_directory_path = session_details["user_directory_path"]
        tests_download_url = session_details["tests_download_url"]

        if session_details.get("ide_type") == IDETypeEnum.ccbp_ide.value:
            temp_folder = self.get_question_specific_temp_folder(
                user_directory_path)
            temp_folder_path = str(Path(
                CCBP_WORKSPACE_TEMP_DIR_PATH) / temp_folder)
            Path(temp_folder_path).mkdir(parents=True, exist_ok=True)
        else:
            temp_folder_path = str(Path(
                CCBP_IDE_V2_TEMP_DIR_PATH) / str(uuid.uuid4()))
            Path(temp_folder_path).mkdir(parents=True, exist_ok=True)

        if session_details["test_type"] \
                == IDESessionTestTypeEnum.default.value:
            remove_all_files_in_directory_except_node_modules(temp_folder_path)

        from ccbp_ide_cli.utils.s3_utils import UploadFileToS3Util
        upload_util = UploadFileToS3Util(s3_credentials, ide_session_id)
        print("Zipping ...")
        zip_file_path = upload_util.create_zip_file(
            user_directory_path, temp_folder_path)
        print("Submitting ...")
        submission_s3_url = upload_util.upload_zip_file_to_private_s3(
                zip_file_path, str(uuid.uuid4()), temp_folder_path)

        if session_details["test_type"] == IDESessionTestTypeEnum.default.value:
            self._run_tests(zip_file_path, user_directory_path,
                            temp_folder_path, tests_download_url)
            results_exist = self._copy_test_results(
                temp_folder_path, user_directory_path)
            if not results_exist:
                raise TestsResultsNotGeneratedException(
                    message=TESTS_RESULTS_NOT_GENERATED,
                    submission_url=submission_s3_url)
        else:  # java
            clear_directory_or_file(zip_file_path)
            self._run_java_tests(user_directory_path,
                                 temp_folder_path, tests_download_url)

        return submission_s3_url

    def _submit_question_results(
            self, submission_url: str, session_details: Dict[str, str]) \
            -> Tuple[str, str, Optional[List[Dict[str, str]]]]:

        question_id = None
        metadata = self.get_metadata_details(session_details["metadata"])
        if metadata:
            session_type = metadata["session_type"]
            if session_type == SessionTypeEnum.question.value:
                question_id = metadata["question_id"]

        user_directory_path = session_details["user_directory_path"]

        testcase_results = get_file_content_as_json(
            str(Path(user_directory_path) / CCBP_TEST_RESULT_JSON_FILE_PATH))
        if not testcase_results:
            raise CannotSubmitQuestionException(
                message=TESTS_RESULTS_NOT_GENERATED,
                submission_url=submission_url)
        if not question_id:
            raise CannotSubmitQuestionException(INVALID_QUESTION_ID)

        body = {
            "responses": [
                {
                    "code_submission_url": submission_url,
                    "question_id": question_id,
                    "time_spent": 1,
                    "test_cases_results": [
                        {
                            "test_case_enum": testcase_result["test_case_id"],
                            "evaluation_result":
                                testcase_result["evaluation_result"],
                        }
                        for testcase_result in
                        testcase_results["test_case_results"]
                    ],
                },
            ],
        }
        exam_attempt_id = os.environ.get(CCBP_IDE_V2_EXAM_ATTEMPT_ID_ENV)
        if exam_attempt_id:
            body["exam_attempt_id"] = exam_attempt_id
            body["total_time_spent"] = 1
            end_point_details = \
                SUBMIT_QUESTION_RESPONSES_FOR_EXAM_END_POINT_CONFIG
            submission_response = self.api_util.api_request(
                url_suffix=end_point_details["end_point"],
                method=end_point_details["method"], body=body)
            submission_id = None
            test_case_details = submission_response[
                "submission_result"][0]["test_case_details"]
        else:
            end_point_details \
                = SUBMIT_QUESTION_RESPONSES_END_POINT_CONFIG
            submission_response = self.api_util.api_request(
                url_suffix=end_point_details["end_point"],
                method=end_point_details["method"], body=body)
            submission_id = \
                submission_response["submission_results"][0]["submission_id"]
            test_case_details = None
        return submission_id, question_id, test_case_details

    def _run_tests(self, zip_file_path: str, user_directory_path: str,
                   temp_folder_path: str, tests_download_url: str):

        spinner = ProgressBarInFiniteUtil("Preparing files to evaluate ...")
        extract_zip_file_to_dir(temp_folder_path, zip_file_path)
        clear_directory_or_file(zip_file_path)
        download_file_and_extract_file(
            dir_path=temp_folder_path,
            zip_file_url=tests_download_url)
        spinner.stop()

        os.chdir(temp_folder_path)

        spinner = ProgressBarInFiniteUtil("Installing Dependencies ...")
        exec_status = os.system(CCBP_NPM_INSTALL_CMD)  # noqa: S605
        if self.is_command_execution_status_failed(exec_status):
            self.clear_existing_node_modules(user_directory_path)
            spinner.stop(SpinnerStatusEnum.failure.value)
            raise NodeModulesInstallationFailedException(
                message=NODE_MODULES_INSTALLATION_FAILED)
        spinner.stop()

        spinner = ProgressBarInFiniteUtil("Running Tests ...")
        os.system(CCBP_NPM_RUN_TEST_CMD)  # noqa: S605
        spinner.stop()


    def _run_java_tests(
            self, user_directory_path: str,
            temp_folder_path: str, tests_download_url: str):

        spinner = ProgressBarInFiniteUtil("Preparing files to evaluate ...")

        tests_temp_folder_path = str(Path(
            temp_folder_path) / CCBP_JAVA_TESTS_FOLDER_NAME)
        tests_user_folder_path = str(Path(
            user_directory_path) / CCBP_JAVA_TESTS_FOLDER_NAME)

        # clearing existing temp tests backup data
        clear_directory_or_file(tests_temp_folder_path)
        Path(tests_temp_folder_path).mkdir(parents=True, exist_ok=True)
        Path(tests_user_folder_path).mkdir(parents=True, exist_ok=True)

        # backup user tests data
        copy_directory(tests_user_folder_path, tests_temp_folder_path)
        clear_directory_or_file(tests_user_folder_path)
        Path(tests_user_folder_path).mkdir(parents=True, exist_ok=True)

        download_file_and_extract_file(
            dir_path=tests_user_folder_path,
            zip_file_url=tests_download_url)
        spinner.stop()

        os.chdir(user_directory_path)
        spinner = ProgressBarInFiniteUtil("Running Tests ...")
        os.system(CCBP_JAVA_RUN_TEST_CMD)  # noqa: S605

        save_java_test_results(CCBP_JAVA_TESTS_RESULTS_FOLDER_PATH)
        clear_directory_or_file(CCBP_JAVA_TESTS_RESULTS_FOLDER_PATH)
        results_exist = self._is_test_results(user_directory_path)
        if not results_exist:
            tests_case_ids_file_path = str(Path(
                user_directory_path) / CCBP_JAVA_TEST_CASE_IDS_FILE_PATH)
            save_java_test_results_with_incorrect_status(
                tests_case_ids_file_path)

        # backup user tests data
        clear_directory_or_file(tests_user_folder_path)
        copy_directory(tests_temp_folder_path, tests_user_folder_path)
        clear_directory_or_file(tests_temp_folder_path)
        spinner.stop()

    @staticmethod
    def _copy_test_results(temp_folder_path: str, user_directory_path: str):

        results_exist = False
        for file_details in CCBP_TEST_RESULT_FILES:
            file_path = str(Path(
                temp_folder_path) / file_details["file_path"])
            if file_details["file_type"] == FileTypeEnum.file.value:
                if is_file_path_exist(file_path):
                    results_exist = True
                    copy_file(file_path, user_directory_path)
            elif is_dir_path_exist(file_path):
                results_exist = True
                des_dir = str(Path(
                    user_directory_path) / file_details["file_path"])
                create_dir(des_dir)
                copy_directory(file_path, des_dir)
        return results_exist

    @staticmethod
    def _is_test_results(user_directory_path: str):

        results_exist = False
        for file_details in CCBP_TEST_RESULT_FILES:
            file_path = str(Path(
                user_directory_path) / file_details["file_path"])
            if file_details["file_type"] == FileTypeEnum.file.value:
                if is_file_path_exist(file_path):
                    results_exist = True
            elif is_dir_path_exist(file_path):
                results_exist = True
        return results_exist

    @staticmethod
    def _clear_existing_test_results(user_directory_path: str):

        for file_details in CCBP_TEST_RESULT_FILES:
            file_path = str(Path(
                user_directory_path) / file_details["file_path"])
            clear_directory_or_file(file_path)

    @staticmethod
    def _get_base_url() -> str:

        env = get_value_for_key_from_file_path(
            CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)
        return CCBP_IDE_API_CUSTOM_BASE_URL_CONFIG.get(
            env, CCBP_IDE_API_DEFAULT_BASE_URL)

    @staticmethod
    def _print_test_case_details(
            test_case_details: List[Dict[str, str]]):

        total_test_cases_count = len(test_case_details)
        failed_test_cases_count = 0
        for each in test_case_details:
            if each["evaluation_result"] != EvaluationResult.correct.value:
                failed_test_cases_count += 1

        if failed_test_cases_count:
            print("\nTest Cases:")
            for each in test_case_details:
                if each["evaluation_result"] != EvaluationResult.correct.value:
                    print_failure_message(
                        get_wrong_tick() + " " + each["display_text"])

            for each in test_case_details:
                if each["evaluation_result"] == EvaluationResult.correct.value:
                    print_success_message(
                        get_right_tick() + " " + each["display_text"])
            # print_success_message(
            #     f"{total_test_cases_count - failed_test_cases_count}/{total_test_cases_count} Test cases passed")
            print_failure_message(
                f"{failed_test_cases_count}/{total_test_cases_count} Test cases failed")

        else:
            print_success_message("\nAll test cases passed")
