import contextlib
import io
import json
import os
import time
import traceback
import zipfile
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional

import requests

from ccbp_ide_cli.constants.enums import SpinnerStatusEnum
from ccbp_ide_cli.exceptions.exceptions import \
    CannotDownloadFileException


def is_file_path_exist(file_path: str) -> bool:
    return Path(file_path).is_file()


def is_dir_path_exist(file_path: str) -> bool:
    return Path(file_path).is_dir()


def get_value_for_key_from_file_path(
        file_path: str, key: str) -> Optional[str]:

    if key == "env" and os.environ.get("BACKEND_STAGE"):
        return os.environ.get("BACKEND_STAGE")

    if key == "ide_token" and os.environ.get("USER_IDE_TOKEN"):
        return os.environ.get("USER_IDE_TOKEN")

    if not is_file_path_exist(file_path):
        return

    with Path(file_path).open() as file:
        lines = file.readlines()
        for line in lines:
            key_value_pair = line.split("=")
            if len(key_value_pair) == 2 and key_value_pair[0] == key:  # noqa: PLR2004
                return key_value_pair[1].strip("\n")
    return None


def create_file_path_if_not_exist(file_path: str):
    file_path = strip_path(file_path)
    if is_file_path_exist(file_path):
        return

    dir_path = "/".join(file_path.split("/")[:-1])
    create_dir(dir_path)

    with Path(file_path).open("w+"):
        pass


def write_key_value_pair_into_file(file_path: str, key: str, value: str):
    create_file_path_if_not_exist(file_path)

    with Path(file_path).open("w+") as file:
        file.write(key + "=" + value)


def write_content_into_file(file_path: str, content: str):
    create_file_path_if_not_exist(file_path)

    with Path(file_path).open("w+") as file:
        file.write(content)


def create_dir(folder_path):
    with contextlib.suppress(FileExistsError):
        Path(folder_path).mkdir(parents=True, exist_ok=True)


def strip_path(file_path: str) -> str:
    return file_path.rstrip("/")


# pylint: disable=consider-using-with,
def extract_zip_response_to_dir(dir_path, response):
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall(dir_path)


def extract_zip_file_to_dir(dir_path: str, zip_file_path: str):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(dir_path)


def download_file_and_extract_file(dir_path, zip_file_url, spinner=None):
    retries = 2
    stack_trace = ""
    while retries:
        try:
            response = requests.get(zip_file_url, stream=True, timeout=30)
            if response and response.status_code >= 400:  # noqa: PLR2004
                stack_trace = response.content.decode("utf-8")
            extract_zip_response_to_dir(dir_path, response)
            break
        except requests.exceptions.Timeout:
            time.sleep(2)
            retries -= 1
        except Exception as exception:
            if not stack_trace:
                stack_trace = ''.join(traceback.format_tb(
                    exception.__traceback__))
                stack_trace = f"{exception}: \n{stack_trace}"
            _stop_spinner(spinner)
            from ccbp_ide_cli.exceptions.exception_messages import \
                DOWNLOAD_ZIP_FILE_FAILED
            message = DOWNLOAD_ZIP_FILE_FAILED
            raise CannotDownloadFileException(
                message=message, stack_trace=stack_trace)


def _stop_spinner(spinner):
    if spinner:
        spinner.stop(SpinnerStatusEnum.failure.value)


def is_empty_folder(path):
    try:
        if os.listdir(path):
            return False
    except FileNotFoundError:
        pass
    return True


def clear_directory_or_file(path):
    import shutil
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        Path(path).unlink()
    except FileNotFoundError:
        pass


def clear_dir_recursively(dir_path):
    if not is_dir_path_exist(dir_path):
        return

    files_path = dir_path + "/*" if not dir_path.endswith("/") \
        else dir_path + "*"
    hidden_files_path = dir_path + "/.*" if not dir_path.endswith("/") \
        else dir_path + ".*"

    os.system(f"rm -rf {files_path} {hidden_files_path}")  # noqa: S605


def copy_directory(src, dst):
    os.system(f"cp -r {src}/. {dst}")  # noqa: S605


def copy_file(src, dst):
    os.system(f"cp -r {src} {dst}/")  # noqa: S605


def get_file_content_as_json(file_path):
    if not is_file_path_exist(file_path):
        return None

    with Path(file_path).open() as file:
        try:
            return json.load(file)
        except JSONDecodeError:
            return None


def get_file_size(file_path) -> int:
    stat_info = Path(file_path).stat()
    return stat_info.st_size


# pylint: disable=unused-variable
def get_directory_size(file_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(file_path):  # noqa: B007
        for f in filenames:
            fp = str(Path(dirpath) / f)
            # skip if it is symbolic link
            if not Path(fp).is_symlink():
                total_size += Path(fp).stat().st_size

    return total_size


# pylint: disable=anomalous-backslash-in-string
def remove_all_files_in_directory_except_node_modules(directory: str):
    if not is_dir_path_exist(directory):
        return
    if is_empty_folder(directory):
        return

    directory = directory[:-1] if directory.endswith("/") else directory

    cmd = "find {directory}/* ! -regex '^{directory}/node_modules\(/.*\)?' " \
          "-delete".format(directory=directory)  # noqa: W605, UP032, W605, ISC002

    os.system(cmd)  # noqa: S605

    rm_hidden_cmd = "find {directory}/ -maxdepth 1 -name \".*\""\
                        .format(directory=directory) + " -exec rm -rf {} +"  # noqa: UP032, Q003
    os.system(rm_hidden_cmd) # noqa: S605
