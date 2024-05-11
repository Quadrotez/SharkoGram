import re


def get_value_from_brackets(string, index):
    if index < len(matches := re.findall(r'\((.*?)\)', string)):
        return matches[index]
    else:
        return False


def get_word(string: str, index: int):
    return string.split(' ')[index - 1] if len(string.split(' ')) > index - 1 else ''
