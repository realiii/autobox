# -*- coding: utf-8 -*-
"""
Toolset Tests
"""


from pytest import mark, raises

from autobox import ScriptTool
from autobox.toolset import Toolset


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
def test_toolset_validate_name(value, expected):
    """
    Test Toolset validate name method
    """
    if expected is None:
        with raises(ValueError):
            Toolset._validate_name(value)
    else:
        assert Toolset._validate_name(value) == expected
# End test_toolset_validate_name function


def test_toolset_repr():
    """
    Test Toolset Representation
    """
    assert repr(Toolset(name='AbCdE')) == "Toolset(name='AbCdE')"
# End test_toolset_repr function


def test_toolset_bad_add():
    """
    Test Toolset Bad Add
    """
    tbx = Toolset(name='AbCdE')
    with raises(TypeError):
        tbx.add_toolset(1)
    with raises(TypeError):
        tbx.add_script_tool('asdf')
# End test_toolset_bad_add function


def test_toolset_has_tools():
    """
    Test Toolset has tools
    """
    tsa = Toolset(name='A')
    assert not tsa.has_tools
    tsa.add_script_tool(ScriptTool(name='AA'))
    assert tsa.has_tools
    tsb = Toolset(name='B')
    tsc = Toolset(name='C')
    tsa.add_toolset(tsb)
    tsb.add_toolset(tsc)
    assert not tsb.has_tools
    assert not tsc.has_tools
    tsb.add_script_tool(ScriptTool(name='BB'))
    assert tsb.has_tools
    assert not tsc.has_tools
# End test_toolset_has_tools function


def test_toolset_add_toolset():
    """
    Test Toolset add toolset
    """
    tsa = Toolset(name='A')
    tsb = Toolset(name='B')
    assert tsb.parent is None
    tsa.add_toolset(tsb)
    assert tsb.parent is tsa
# End test_toolset_add_toolset function


def test_toolset_qualified_name():
    """
    Test Toolset qualified name
    """
    tsa = Toolset(name='A')
    tsb = Toolset(name='B')
    assert tsa.qualified_name == 'A'
    assert tsb.qualified_name == 'B'
    tsa.add_toolset(tsb)
    assert tsb.qualified_name == 'A\\B'
# End test_toolset_qualified_name function


if __name__ == '__main__':  # pragma: no cover
    pass
