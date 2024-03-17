from typing import Optional

from ccbp_ide_cli.constants.config.config import CCBP_VERSION_FILE_PATH
from ccbp_ide_cli.exceptions.exception_messages import \
    UNABLE_TO_GET_VERSION_DETAILS
from ccbp_ide_cli.exceptions.exceptions import UnableToGetVersionException
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator
from ccbp_ide_cli.utils.file_utils import get_file_content_as_json
from ccbp_ide_cli.utils.output_utils import print_success_message


class CCBPVersion:

    @exception_handling_decorator
    def ccbp_version(self):

        version = self.get_version()

        if not version:
            raise UnableToGetVersionException(UNABLE_TO_GET_VERSION_DETAILS)

        print_success_message(f"\nVersion : {version}")
        return version

    @staticmethod
    def get_version() -> Optional[str]:
        version_details = get_file_content_as_json(CCBP_VERSION_FILE_PATH)
        try:
            version = version_details["version"]
        except Exception:
            version = None

        return version
