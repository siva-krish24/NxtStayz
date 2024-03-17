def clear_ide_token_config():
    from ccbp_ide_cli.constants.config.config import CCBP_CREDENTIALS_FILE_PATH
    from ccbp_ide_cli.utils.file_utils import clear_directory_or_file
    clear_directory_or_file(CCBP_CREDENTIALS_FILE_PATH)
