import json
import os
from xml.etree import ElementTree
from pathlib import Path

from ccbp_ide_cli.constants.config.config import \
    CCBP_TEST_RESULT_JSON_FILE_PATH
from ccbp_ide_cli.utils.file_utils import write_content_into_file, \
    is_dir_path_exist, get_file_content_as_json


def save_java_test_results(tests_xml_files_path):
    if not is_dir_path_exist(tests_xml_files_path):
        return

    test_case_results = []
    is_invalid_test_ids_generated = False
    for test_case_file in os.listdir(tests_xml_files_path):
        if not test_case_file.endswith(".xml"):
            continue

        xml_file = test_case_file

        file_path = str(Path(tests_xml_files_path) / xml_file)

        tree = ElementTree.parse(file_path)  # noqa: S314
        root = tree.getroot()

        test_cases_in_a_file = []

        for testcase in root.iter("testcase"):
            test_case = {}

            if testcase.attrib["classname"] == testcase.attrib["name"]:
                is_invalid_test_ids_generated = True
                break

            test_case["test_case_id"] = testcase.attrib["classname"] + \
                "." + testcase.attrib["name"]

            if testcase.find("failure") is not None or \
                    testcase.find("error") is not None:
                test_case["evaluation_result"] = "INCORRECT"
            else:
                test_case["evaluation_result"] = "CORRECT"

            test_cases_in_a_file.append(test_case)

        if is_invalid_test_ids_generated:
            break

        test_case_results.extend(test_cases_in_a_file)

    if is_invalid_test_ids_generated:
        return

    response = {
        "test_case_results": test_case_results,
    }
    write_content_into_file(
        CCBP_TEST_RESULT_JSON_FILE_PATH, json.dumps(response))


def save_java_test_results_with_incorrect_status(
        test_case_ids_file_path: str):
    test_case_ids_dict = get_file_content_as_json(test_case_ids_file_path)

    test_case_ids = []
    for each in test_case_ids_dict:
        if "test_case_name_enum" in each:
            test_case_ids.append(each["test_case_name_enum"])
        else:
            test_case_id = next(iter(each.values()))
            test_case_ids.append(test_case_id)

    evaluation_response_data = {
        "test_case_results": [
            {
                "test_case_id": test_case_id,
                "evaluation_result": "INCORRECT",
            }
            for test_case_id in test_case_ids
        ],
    }
    write_content_into_file(
        CCBP_TEST_RESULT_JSON_FILE_PATH, json.dumps(evaluation_response_data))
