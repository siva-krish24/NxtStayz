import enum


class SessionTypeEnum(enum.Enum):
    question = "QUESTION"
    solution = "SOLUTION"
    ide_playground = "IDE_PLAYGROUND"


class FileTypeEnum(enum.Enum):
    file = "FILE"
    dir = "DIR"


class EnvValueEnum(enum.Enum):
    local = "local"
    mock = "mock"
    otg_beta = "otg_beta"
    otg_gamma = "otg_gamma"
    otg_prod = "otg_prod"
    ccbp_beta = "ccbp_beta"
    ccbp_gamma = "ccbp_gamma"
    ccbp_prod = "ccbp_prod"
    kossip_beta = "kossip_beta"
    kossip_gamma = "kossip_gamma"
    kossip_prod = "kossip_prod"


class SpinnerStatusEnum(enum.Enum):
    success = "Done"
    failure = "Fail"


class UserActionStatus(enum.Enum):
    success = "SUCCESS"
    failure = "FAILURE"


class IDETypeEnum(enum.Enum):
    ccbp_ide = "CCBP_IDE"
    replit = "REPLIT"
    ccbp_ide_v2 = "CCBP_IDE_V2"


class IDESessionTestTypeEnum(enum.Enum):
    default = "DEFAULT"
    java = "JAVA"


class EvaluationResult(enum.Enum):
    correct = "CORRECT"
    incorrect = "INCORRECT"
