from ccbp_ide_cli.cli_functions.mixins.common_mixin import CommonMixin
from ccbp_ide_cli.constants.api_end_points import STOP_CCBP_IDE_SESSION
from ccbp_ide_cli.utils.api_utils.get_api_util import get_api_util
from ccbp_ide_cli.utils.exception_handler import exception_handling_decorator


class CCBPStop(CommonMixin):

    def __init__(self):
        self.api_util = None

    @exception_handling_decorator
    def ccbp_stop(self, drop_instance_id: str, stop_reason: str):
        self.validate_ide_token()

        api_util = get_api_util()
        self.api_util = api_util

        self._stop_ccbp_ide(drop_instance_id, stop_reason)

    def _stop_ccbp_ide(self, drop_instance_id: str, stop_reason: str):
        end_point_details = STOP_CCBP_IDE_SESSION
        self.api_util.api_request(
            url_suffix=end_point_details["end_point"],
            method=end_point_details["method"], body={
                "drop_id": drop_instance_id,
                "stop_reason": stop_reason,
            })
