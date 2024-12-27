# -*- coding: utf-8 -*-
"""
Utility Functionality
"""


from collections import Counter
from pathlib import Path
from re import sub
from tempfile import mkdtemp
from typing import NoReturn, TYPE_CHECKING

from autobox.constant import (
    DOUBLE_SPACE, DOUBLE_UNDERSCORE, EXT, SPACE, UNDERSCORE)
from autobox.type import STRING


if TYPE_CHECKING:  # pragma: no cover
    from autobox.parameter import BaseParameter
    from autobox.script import ScriptTool
    from autobox.toolset import Toolset


WINDOWS_RESERVED: set[str] = (
        {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$'} |
        {'COM%s' % c for c in '123456789\xb9\xb2\xb3'} |
        {'LPT%s' % c for c in '123456789\xb9\xb2\xb3'}
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
    return _remove_leading_non_alpha(value)
# End _validate_alpha_start_sans_special function


def _remove_leading_non_alpha(value: str) -> STRING:
    """
    Remove Leading Non-alpha characters
    """
    if not value:
        return
    first, *_ = value
    while not first.isalpha():
        if not (value := value[1:]):
            return
        first, *_ = value
    return value
# End _remove_leading_non_alpha function


def validate_toolset_name(value: str) -> STRING:
    """
    Validate that the value is a string, is not empty, and does not
    contain special characters.
    """
    return _validate_name_no_special(
        value, single=SPACE, double=DOUBLE_SPACE)
# End validate_toolset_name function


def _validate_name_no_special(value: str, single: str, double: str) -> STRING:
    """
    Validate that the value is a string, is not empty, and does not
    contain special characters.
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    value = sub(r'[\\/:*?&"<>|]', repl=single, string=value)
    while double in value:
        value = value.replace(double, single)
    if not (value := value.strip()):
        return
    return value
# End _validate_name_no_special function


def validate_parameter_name(value: str) -> STRING:
    """
    Validate that the value is a string, is not empty, does not
    contain special characters, and does not start with a number.
    """
    value = _validate_name_no_special(
        value, single=SPACE, double=DOUBLE_SPACE)
    value = _validate_name_no_special(
        value, single=UNDERSCORE, double=DOUBLE_UNDERSCORE)
    return _remove_leading_non_alpha(value)
# End validate_parameter_name function


def validate_parameter_label(value: str) -> STRING:
    """
    Validate Parameter Label
    """
    if not isinstance(value, str):
        return
    if not (value := value.strip()):
        return
    while DOUBLE_SPACE in value:
        value = value.replace(DOUBLE_SPACE, SPACE)
    return value
# End validate_parameter_label function


def make_parameter_name(value: str) -> STRING:
    """
    Make Parameter Name from Validated Parameter Label, general aim of this
    function is to make a valid python identifier starting with a letter.
    """
    value = ''.join(c if c.isalnum() else UNDERSCORE for c in value)
    if not (value := _remove_leading_non_alpha(value)):
        return
    return value.casefold()
# End make_parameter_name function


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


def validate_path(path: Path, text: str) -> Path | NoReturn:
    """
    Validate Path
    """
    try:
        path = Path(path)
    except TypeError:
        raise ValueError(f'Invalid {text} path provided: {path}')
    if not path.is_file():
        raise FileNotFoundError(f'File not found: {path}')
    return path.resolve()
# End validate_path function


def unique(values: list | tuple) -> list:
    """
    Unique list of elements, order preserving
    """
    return list(dict.fromkeys(values))
# End unique function


def get_repeated_names(values: list['Toolset'] | list['ScriptTool'] |
                               list['BaseParameter']) -> set[str]:
    """
    Get Repeated Names, case-insensitive check.
    """
    counter = Counter(v.name.casefold() for v in values)
    return {n for n, c in counter.items() if c > 1}
# End get_repeated_names method


if __name__ == '__main__':  # pragma: no cover
    pass
