from progressbar import ProgressBar
from yaspin import yaspin
from yaspin.spinners import Spinners

from ccbp_ide_cli.constants.enums import SpinnerStatusEnum
from ccbp_ide_cli.utils.file_utils import get_file_size, is_file_path_exist, \
    get_directory_size
from ccbp_ide_cli.utils.output_utils import get_success_message, \
    get_failure_message, reset_color


class ProgressBarFiniteUtil:

    def __init__(self, file_path: str):
        if is_file_path_exist(file_path):
            self.file_size = get_file_size(file_path)
        else:
            self.file_size = get_directory_size(file_path)
        self.progressbar = ProgressBar(max_value=self.file_size)
        self.progressbar.update(min(1, self.file_size))
        self.seen_so_far = 0

    def update(self, bytes_transferred: int):
        if bytes_transferred:
            self.seen_so_far += bytes_transferred
            if self.seen_so_far > self.file_size:
                self.seen_so_far = self.file_size
            self.progressbar.update(self.seen_so_far)

    def finish(self):
        self.progressbar.finish()

    def fail(self):
        self.progressbar.finish(dirty=True)


class ProgressBarInFiniteUtil:

    def __init__(self, message: str, spin_location="right"):
        self.can_run = True
        self.spinner = yaspin()
        self.spinner.spinner = Spinners.line
        self.spinner.text = message
        self.spinner.side = spin_location
        self.spinner.start()

    def stop(self, status=SpinnerStatusEnum.success.value):
        if status == SpinnerStatusEnum.success.value:
            status = get_success_message(status)
            self.spinner.ok(status)
        else:
            status = get_failure_message(status)
            self.spinner.fail(status)
        reset_color()
