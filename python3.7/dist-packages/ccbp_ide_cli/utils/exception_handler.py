import datetime
import traceback

from ccbp_ide_cli.constants.config.config import CCBP_ENV_FILE_PATH, \
    CCBP_IDE_ENV_KEY_NAME
from ccbp_ide_cli.constants.enums import EnvValueEnum, UserActionStatus
from ccbp_ide_cli.exceptions.exception_messages import \
    UNKNOWN_EXCEPTION_OCCURRED, UNKNOWN_EXCEPTION_OCCURRED_RES_STATUS
from ccbp_ide_cli.exceptions.exceptions import InvalidApiRequestException, \
    CannotDownloadFileException, CannotExtractZipFileException, \
    CannotSubmitQuestionException, TestsResultsNotGeneratedException, \
    SubmissionUploadFailedException, InvalidTokenException, \
    QuestionNotStartedException, SolutionUnlockingTimeNotCompletedException, \
    SolutionNotFoundException, InvalidSessionException, \
    IDETokenNotConfiguredException, UserResourceNotUnlockedException, \
    UnableToGetVersionException, CannotPublishException, \
    SystemTimeNotUpToDateException, NodeModulesInstallationFailedException, \
    CannotUpdateSessionException
from ccbp_ide_cli.utils.file_utils import get_value_for_key_from_file_path
from ccbp_ide_cli.utils.logging_utils import log_data
from ccbp_ide_cli.utils.output_utils import print_failure_message


# pylint: disable=too-many-branches, too-many-statements
def exception_handling_decorator(func):  # noqa: C901, PLR0915
    def function_wrapper(*args, **kwargs):  # noqa: PLR0912, C901, PLR0915

        action = func.__name__.upper()
        status = UserActionStatus.failure.value
        exception_obj = None
        failure_message = ""
        failure_reason = ""
        start_timestamp = datetime.datetime.now()
        stack_trace = ""
        submission_url = ""

        try:
            func(*args, **kwargs)
            status = UserActionStatus.success.value
        except InvalidApiRequestException as exception:
            exception_obj = exception
            stack_trace = exception.stack_trace
        except CannotExtractZipFileException as exception:
            exception_obj = exception
        except CannotDownloadFileException as exception:
            exception_obj = exception
            stack_trace = exception.stack_trace
        except CannotSubmitQuestionException as exception:
            exception_obj = exception
            submission_url = exception.submission_url
        except TestsResultsNotGeneratedException as exception:
            exception_obj = exception
            submission_url = exception.submission_url
        except SubmissionUploadFailedException as exception:
            exception_obj = exception
            stack_trace = exception.stack_trace
        except InvalidTokenException as exception:
            exception_obj = exception
        except QuestionNotStartedException as exception:
            exception_obj = exception
        except SolutionUnlockingTimeNotCompletedException as exception:
            exception_obj = exception
        except SolutionNotFoundException as exception:
            exception_obj = exception
        except InvalidSessionException as exception:
            exception_obj = exception
        except IDETokenNotConfiguredException as exception:
            exception_obj = exception
        except UserResourceNotUnlockedException as exception:
            exception_obj = exception
        except UnableToGetVersionException as exception:
            exception_obj = exception
        except CannotPublishException as exception:
            exception_obj = exception
        except SystemTimeNotUpToDateException as exception:
            stack_trace = exception.stack_trace
            exception_obj = exception
        except NodeModulesInstallationFailedException as exception:
            exception_obj = exception
        except CannotUpdateSessionException as exception:
            exception_obj = exception
        except Exception as exception:
            stack_trace = ''.join(traceback.format_tb(
                exception.__traceback__))
            stack_trace = f"{exception}: \n{stack_trace}"
            failure_message = UNKNOWN_EXCEPTION_OCCURRED
            failure_reason = UNKNOWN_EXCEPTION_OCCURRED_RES_STATUS
            env = get_value_for_key_from_file_path(
                CCBP_ENV_FILE_PATH, CCBP_IDE_ENV_KEY_NAME)
            if env == EnvValueEnum.mock.value:
                raise
        end_timestamp = datetime.datetime.now()

        if status == UserActionStatus.failure.value:
            if not failure_message:
                failure_message = exception_obj.message
            print_failure_message(f"\n{failure_message}")

        if exception_obj:
            try:
                if exception_obj.res_status:
                    failure_reason = exception_obj.res_status
                else:
                    failure_reason = exception_obj.__class__.__name__
            except AttributeError:
                failure_reason = exception_obj.__class__.__name__

        log_data(
            action=action, status=status, failure_message=failure_message,
            failure_reason=failure_reason, start_timestamp=start_timestamp,
            end_timestamp=end_timestamp, stack_trace=stack_trace,
            submission_url=submission_url, **kwargs)

    return function_wrapper
