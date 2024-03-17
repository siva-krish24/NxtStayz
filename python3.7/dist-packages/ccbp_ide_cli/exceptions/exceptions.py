class CannotDownloadFileException(Exception):
    def __init__(self, message: str, stack_trace: str = ""):
        self.message = message
        self.stack_trace = stack_trace


class CannotExtractZipFileException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidApiRequestException(Exception):
    def __init__(self, message: str, res_status: str = "",
                 stack_trace: str = ""):
        self.message = message
        self.res_status = res_status
        self.stack_trace = stack_trace


class CannotSubmitQuestionException(Exception):
    def __init__(self, message: str, submission_url: str = ""):
        self.message = message
        self.submission_url = submission_url


class TestsResultsNotGeneratedException(Exception):
    def __init__(self, message: str, submission_url: str = ""):
        self.message = message
        self.submission_url = submission_url


class SubmissionUploadFailedException(Exception):
    def __init__(self, message: str, stack_trace: str = ""):
        self.message = message
        self.stack_trace = stack_trace


class InvalidTokenException(Exception):
    def __init__(self, message: str):
        self.message = message


class QuestionNotStartedException(Exception):
    def __init__(self, message: str):
        self.message = message


class SolutionUnlockingTimeNotCompletedException(Exception):
    def __init__(self, message: str):
        self.message = message


class SolutionNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidSessionException(Exception):
    def __init__(self, message: str):
        self.message = message


class IDETokenNotConfiguredException(Exception):
    def __init__(self, message: str):
        self.message = message


class UserResourceNotUnlockedException(Exception):
    def __init__(self, message: str):
        self.message = message


class UnableToGetVersionException(Exception):
    def __init__(self, message: str):
        self.message = message


class CannotPublishException(Exception):
    def __init__(self, message: str):
        self.message = message


class SystemTimeNotUpToDateException(Exception):
    def __init__(self, message: str, stack_trace: str = ""):
        self.message = message
        self.stack_trace = stack_trace


class NodeModulesInstallationFailedException(Exception):
    def __init__(self, message: str):
        self.message = message


class CannotUpdateSessionException(Exception):
    def __init__(self, message: str):
        self.message = message
