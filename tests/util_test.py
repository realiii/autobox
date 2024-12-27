# -*- coding: utf-8 -*-
"""
Utility Tests
"""


from pytest import mark
from autobox.util import (
    _remove_leading_non_alpha, _validate_alpha_start_sans_special,
    make_parameter_name, validate_parameter_label, validate_parameter_name,
    validate_script_folder_name, validate_toolbox_name, validate_toolset_name,
    wrap_markup)


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
    ('valid_name', 'valid_name'),
    ('valid value', 'valid value'),
    ('in|valid?', 'in valid'),
    ('<<<>>>:', None),
    ('file  name', 'file name'),
    ('   valid  ', 'valid'),
    ('', None),
    ('PRN', 'PRN'),
    ('COM1', 'COM1'),
    ('valid-file-value.ext', 'valid-file-value.ext'),
    ('', None),
    ('______', '______'),
    ('tool?\\:set<>name', 'tool set name'),
    (None, None)
])
def test_validate_toolset_name(value, expected):
    """
    Test Validate Toolset Name
    """
    assert validate_toolset_name(value) == expected
# End test_validate_toolset_name function


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


@mark.parametrize('value, expected', [
    ('validLabel', 'validLabel'),
    ('Valid_Label123', 'Valid_Label123'),
    ('valid label', 'valid label'),
    ('accidental  spaces', 'accidental spaces'),
    ('123 valid', '123 valid'),
    ('', None),
    ('  ', None),
    ('   ', None),
    (None, None)
])
def test_validate_parameter_label(value, expected):
    """
    Test validate_parameter_label
    """
    assert validate_parameter_label(value) == expected
# End test_validate_parameter_label function


@mark.parametrize('value, expected', [
    ('validname', 'validname'),
    ('Valid_name123', 'Valid_name123'),
    ('valid name', 'valid name'),
    ('accidental  spaces', 'accidental spaces'),
    ('123 valid', 'valid'),
    ('', None),
    ('  ', None),
    ('   ', None),
    (None, None)
])
def test_validate_parameter_name(value, expected):
    """
    Test validate_parameter_name
    """
    assert validate_parameter_name(value) == expected
# End test_validate_parameter_name function


@mark.parametrize('value, expected', [
    ('1234', None),
    ('asdf', 'asdf'),
    ('1234asdf', 'asdf'),
    ('1234_asdf', 'asdf'),
    ('asdf1234', 'asdf1234'),
])
def test_remove_leading_numeric(value, expected):
    """
    Test _remove_leading_non_alpha
    """
    assert _remove_leading_non_alpha(value) == expected
# End test_remove_leading_numeric function


@mark.parametrize('value, expected', [
    ('validLabel', 'validlabel'),
    ('Valid_Label123', 'valid_label123'),
    ('valid label', 'valid_label'),
    ('accidental  spaces', 'accidental_spaces'),
    ('123 valid', 'valid'),
    ('123', None),
])
def test_make_parameter_name(value, expected):
    """
    Test make_parameter_name
    """
    value = validate_parameter_label(value)
    assert make_parameter_name(value) == expected
# End test_make_parameter_name function


if __name__ == '__main__':  # pragma: no cover
    pass
