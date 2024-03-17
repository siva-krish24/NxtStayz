from colorama import Fore, Style


def print_failure_message(message, color=None):
    if not color:
        color = Fore.RED

    _print_message(color, message)


def print_success_message(message, color=None):
    if not color:
        color = Fore.GREEN

    _print_message(color, message)


def get_failure_message(message, color=None):
    if not color:
        color = Fore.RED
    return color + message


def get_success_message(message, color=None):
    if not color:
        color = Fore.GREEN
    return color + message


def reset_color():
    print(Style.RESET_ALL, end='')


# pylint: disable = anomalous-backslash-in-string
def enable_cursor():
    import os
    os.system("echo -n \"\e[?25h\"")  # noqa: Q003, S605, S607, W605


def _print_message(color, message):
    print(color + message)
    print(Style.RESET_ALL)


def get_right_tick():
    return "\u2714"


def get_wrong_tick():
    return "\u2718"
