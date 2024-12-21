# -*- coding: utf-8 -*-
"""
Utility Functionality
"""


from pathlib import Path
from re import sub
from tempfile import mkdtemp

from stoolbox.constants import DOUBLE_UNDERSCORE, EXT, UNDERSCORE
from stoolbox.types import STRING




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
    reserved = ('CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)),
                *(f'LPT{i}' for i in range(1, 10)))
    if value.upper() in reserved:
        return
    return value
# End validate_toolbox_name function


def validate_toolbox_alias(value: str) -> STRING:
    """
    Validates the toolbox alias.  Alias must not start with a number,
    contain only letters and numbers.
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
# End validate_toolbox_alias function


def make_temp_folder() -> Path:
    """
    Make Temporary Folder
    """
    return Path(mkdtemp())
# End make_temp_folder function


if __name__ == '__main__':  # pragma: no cover
    pass
