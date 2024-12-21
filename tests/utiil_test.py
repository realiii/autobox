# -*- coding: utf-8 -*-
"""
Utility Tests
"""

from pytest import mark
from stoolbox.util import validate_toolbox_alias, validate_toolbox_name


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
def test_validate_toolbox_alias(value, expected):
    """
    Validate Toolbox Alias
    """
    assert validate_toolbox_alias(value) == expected
# End test_validate_toolbox_alias function


if __name__ == '__main__':  # pragma: no cover
    pass
