# -*- coding: utf-8 -*-
"""
Utility Functionality
"""


from pathlib import Path
from re import sub
from tempfile import mkdtemp

from stoolbox.constants import (
    DOUBLE_SPACE, DOUBLE_UNDERSCORE, EXT, SPACE, UNDERSCORE)
from stoolbox.types import STRING


WINDOWS_RESERVED: tuple[str, ...] = (
    'CON', 'PRN', 'AUX', 'NUL',
    *(f'COM{i}' for i in range(1, 10)),
    *(f'LPT{i}' for i in range(1, 10))
)


def validate_toolbox_name(value: str) -> STRING:
    """
    Validates the toolbox value, needs to be a valid file value on window.
    Returns a sanitized version of it if possible, otherwise None.
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    if value.casefold().endswith(EXT):
        if not (value := value[:-len(EXT)]):
            return
    value = sub(r'[<>:"/\\|?*\x00-\x1F]', repl=UNDERSCORE, string=value)
    while DOUBLE_UNDERSCORE in value:
        value = value.replace(DOUBLE_UNDERSCORE, UNDERSCORE)
    value = value.strip(UNDERSCORE)
    if not value or value == UNDERSCORE:
        return
    if value.upper() in WINDOWS_RESERVED:
        return
    return value
# End validate_toolbox_name function


def validate_toolbox_alias(value: str) -> STRING:
    """
    Validates the toolbox alias.  Alias must not start with a number,
    contain only letters and numbers.
    """
    return _validate_alpha_start_sans_special(value)
# End validate_toolbox_alias function


def validate_script_name(value: str) -> STRING:
    """
    Validates the script name.  Name must not start with a number,
    contain only letters and numbers.
    """
    return _validate_alpha_start_sans_special(value)
# End validate_script_name function


def validate_script_folder_name(value: str) -> STRING:
    """
    Validate the script folder name.  Input needs to be the validated script
    name, check if the name is reserved and change with a trailing underscore
    if the name is reserved.
    """
    if value.upper() in WINDOWS_RESERVED:
        return f'{value}{UNDERSCORE}'
    return value
# End validate_script_folder_name function


def _validate_alpha_start_sans_special(value: str) -> STRING:
    """
    Validate that the value is a string, starts with a letter, and does not
    contain any special characters.  Attempt to make a valid name.
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    if not (value := ''.join(c for c in value if c.isalnum())):
        return
    first, *_ = value
    while first.isnumeric():
        if not (value := value[1:]):
            return
        first, *_ = value
    return value
# End _validate_alpha_start_sans_special function


def validate_toolset_name(value: str) -> STRING:
    """
    Validate that the value is a string, is not empty, and does not
    contain special characters.
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    value = sub(r'[\\/:*?&"<>|]', repl=SPACE, string=value)
    while DOUBLE_SPACE in value:
        value = value.replace(DOUBLE_SPACE, SPACE)
    if not (value := value.strip()):
        return
    return value
# End validate_toolset_name function


def make_temp_folder() -> Path:
    """
    Make Temporary Folder
    """
    return Path(mkdtemp())
# End make_temp_folder function


def wrap_markup(value: STRING) -> STRING:
    """
    Wrap text with xdoc if the text appears to be html-ish.
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    begin, end = '<xdoc>', '</xdoc>'
    if value.startswith(begin) and value.endswith(end):
        return value
    if '</' in value and '>' in value:
        return f'{begin}{value}{end}'
    return value
# End wrap_markup function


if __name__ == '__main__':  # pragma: no cover
    pass
