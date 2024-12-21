# -*- coding: utf-8 -*-
"""
Utility Tests
"""

from pytest import mark
from stoolbox.util import (
    _validate_alpha_start_sans_special, validate_script_folder_name,
    validate_toolbox_name, wrap_markup)


@mark.parametrize('value, expected', [
    ('valid_name.txt', 'valid_name.txt'),
    ('valid value.txt', 'valid value.txt'),
    ('in|valid?.txt', 'in_valid_.txt'),
    ('<<<>>>:.txt', '.txt'),
    ('file__name', 'file_name'),
    ('   valid.atbx  ', 'valid'),
    ('.atbx', None),
    ('PRN', None),
    ('COM1', None),
    ('valid-file-value.ext', 'valid-file-value.ext'),
    ('', None),
    ('______', None),
    ('CON', None),
    ('tool?\\:box<>name', 'tool_box_name'),
    (None, None)
])
def test_validate_toolbox_name(value, expected):
    """
    Test Validate Toolbox Name
    """
    assert validate_toolbox_name(value) == expected
# End test_validate_toolbox_name function


@mark.parametrize('value, expected', [
    ('asdf', 'asdf'),
    ('1asdf', 'asdf'),
    ('1asdf1', 'asdf1'),
    ('as)d_f', 'asdf'),
    ('_____', None),
    ('', None),
    (None, None),
    ('12345', None),
])
def test_validate_alpha_start_sans_special(value, expected):
    """
    Validate Alpha Start Sans Special
    """
    assert _validate_alpha_start_sans_special(value) == expected
# End test_validate_alpha_start_sans_special function


@mark.parametrize('value, expected', [
    ('valid_name', 'valid_name'),
    ('COM1', 'COM1_'),
    ('PRN', 'PRN_'),
])
def test_validate_script_folder_name(value, expected):
    """
    Test validate script folder name
    """
    assert validate_script_folder_name(value) == expected
# End test_validate_script_folder_name function


@mark.parametrize('value, expected', [
    (None, None),
    (' ', None),
    ('', None),
    ('asdf', 'asdf'),
    ('<b>asdf</b>', '<xdoc><b>asdf</b></xdoc>'),
    ('<xdoc><b>asdf</b></xdoc>', '<xdoc><b>asdf</b></xdoc>'),
])
def test_wrap_markup(value, expected):
    """
    Test wrap_markup
    """
    assert wrap_markup(value) == expected
# End test_wrap_markup function


if __name__ == '__main__':  # pragma: no cover
    pass
