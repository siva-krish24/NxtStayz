from typing import List


def get_input_from_user(message: str, options: List[str]):
    user_input = strip_and_lower_string(input(message))
    while user_input not in options:
        user_input = strip_and_lower_string(input(message))
    return user_input


def strip_and_lower_string(string: str) -> str:
    return string.strip().lower()
