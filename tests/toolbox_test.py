# -*- coding: utf-8 -*-
"""
Toolbox Class Tests
"""

from pytest import mark, raises

from helpers import read_from_zip
from stoolbox import ScriptTool
from stoolbox.toolbox import Toolbox
from stoolbox.constants import EXT, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC
from stoolbox.toolset import Toolset
from stoolbox.types import ToolAttributes


@mark.parametrize('name, label, alias, description, compare_name', [
    ('basic', None, None, None, 'basic'),
    ('empty', 'An Empty Toolbox', 'emptynounderscore', 'We should have included a description too.', 'empty'),
])
def test_toolbox_save(tmp_path, data_path, name, label, alias, description, compare_name):
    """
    Test Toolbox save method, compare with simple toolboxes.
    """
    compare_path = data_path.joinpath(f'{compare_name}{EXT}')
    assert compare_path.is_file()
    tbx = Toolbox(name=name, label=label, alias=alias, description=description)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_save function


def test_toolbox_save_with_root_script(tmp_path, data_path):
    """
    Test Toolbox save method with a fairly fleshed out script tool at root.
    """
    compare_path = data_path.joinpath('root_script.atbx')
    assert compare_path.is_file()
    tool = ScriptTool(
        name='TheScriptNameSansSpaces',
        label='The Script Label With Spaces',
        description="Here is where you'd put all the deliciousness about the script capabilities",
        summary="<p><span>and if you needed more text to summarize the details then do it here, "
                "from the looks of it you can also include fancy text as </span><b>bold</b><span>, "
                "</span><i>italics </i><span>(emphasis), and "
                "</span><span style=\"text-decoration:underline;\">underline</span><span>. "
                "And even though this box is super tiny could also include bullet list "
                "like this:</span></p><ul><li><p><span>the box is expanding as more "
                "content is added</span></p></li><li><p><span>this is kinda nice but the "
                "overall window does not change sice</span></p></li><li><p><span>one more "
                "bullet point for funsies</span></p></li></ul><p><span>and heck, lets' "
                "put in a link to </span><a href=\"http://www.google.com/\">www.google.com </a><span>"
                "which is better than just www.yahoo.com.</span></p>",
        attributes=ToolAttributes(
            show_modifies_input=True, do_not_add_to_map=True,
            show_enable_undo=True, show_consumes_credits=True)
    )

    tbx = Toolbox(name='root_script')
    tbx.add_script_tool(tool)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_save_with_root_script function


def test_toolbox_save_with_bad_tool_names(tmp_path, data_path):
    """
    Test Toolbox save method with basic tools but having invalid folder names
    """
    compare_path = data_path.joinpath('silly_scripts.atbx')
    assert compare_path.is_file()
    tool1 = ScriptTool(name='COM1', label='COM1 not a valid Folder')
    tool2 = ScriptTool(name='LPT1', label='Is tihs a printer?')

    tbx = Toolbox(name='silly_scripts')
    tbx.add_script_tool(tool1)
    tbx.add_script_tool(tool2)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_save_with_bad_tool_names function


def test_toolbox_with_toolsets_sans_tools(tmp_path, data_path):
    """
    Test a Toolbox that has toolsets but no tools
    """
    compare_path = data_path.joinpath('toolsets_sans_tools.atbx')
    assert compare_path.is_file()
    toolset1 = Toolset(name='A Toolset')
    toolset2 = Toolset(name='B Toolset')
    toolset3 = Toolset(name='C Toolset')
    toolset2.add_toolset(toolset3)

    tbx = Toolbox(name='toolsets_sans_tools')
    tbx.add_toolset(toolset1)
    tbx.add_toolset(toolset2)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_with_toolsets_sans_tools function


def test_toolbox_with_toolsets_and_tools(tmp_path, data_path):
    """
    Test a Toolbox that has toolsets and tools, no root tools
    """
    compare_path = data_path.joinpath('toolset_no_root.atbx')
    assert compare_path.is_file()
    toolset1 = Toolset(name='His Tools')
    toolset2 = Toolset(name='Her Tools')
    toolset3 = Toolset(name='Another Toolset')
    toolset4 = Toolset(name='A Toolset')
    toolset5 = Toolset(name='B Toolset')
    toolset6 = Toolset(name='C Toolset')

    toolset1.add_toolset(toolset3)
    toolset2.add_toolset(toolset4)
    toolset2.add_toolset(toolset5)
    toolset2.add_toolset(toolset6)

    tool1 = ScriptTool(name='ScriptInToolset', label='Script In Toolset')
    tool2 = ScriptTool(name='SubScriptInToolset', label='Sub Script in Toolset')
    toolset1.add_script_tool(tool1)
    toolset1.add_script_tool(tool2)

    tool3 = ScriptTool(name='Anudder', label='Another Script')
    tool4 = ScriptTool(name='SecondScriptInToolset', label='Script in Toolset (Second)')
    tool5 = ScriptTool(name='SecondSubScriptInToolset', label='Sub Script in Toolset (Second)')
    toolset3.add_script_tool(tool3)
    toolset3.add_script_tool(tool4)
    toolset3.add_script_tool(tool5)

    tool6 = ScriptTool(name='AScript', label='A Script')
    toolset4.add_script_tool(tool6)
    tool7 = ScriptTool(name='BScript', label='B Script')
    toolset5.add_script_tool(tool7)
    tool8 = ScriptTool(name='CScript', label='C Script')
    toolset6.add_script_tool(tool8)

    tbx = Toolbox(name='toolset_no_root')
    tbx.add_toolset(toolset3)
    tbx.add_toolset(toolset2)
    tbx.add_toolset(toolset4)
    tbx.add_toolset(toolset5)
    tbx.add_toolset(toolset6)
    tbx.add_toolset(toolset1)

    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_with_toolsets_and_tools function


def test_toolbox_with_toolsets_and_tools_plus_root(tmp_path, data_path):
    """
    Test a Toolbox that has toolsets and tools + tool at root
    """
    compare_path = data_path.joinpath('toolsets_with_tools.atbx')
    assert compare_path.is_file()
    toolset1 = Toolset(name='A')
    toolset2 = Toolset(name='B')
    toolset3 = Toolset(name='C')
    toolset4 = Toolset(name='D')
    toolset3.add_toolset(toolset4)

    tool_root = ScriptTool(
        name='ScriptInRoot', label='Script in Root',
        description='simple description', summary='plain summary, no formatting')
    tool1 = ScriptTool(name='ScriptInToolsetA', label='Script in Toolset A')
    toolset1.add_script_tool(tool1)
    tool2 = ScriptTool(name='ScriptInToolsetB', label='Script in Toolset B')
    toolset2.add_script_tool(tool2)
    tool3 = ScriptTool(name='ScriptInToolsetC', label='Script in Toolset C')
    toolset3.add_script_tool(tool3)
    tool4 = ScriptTool(name='ScriptInToolsetD', label='Script in Toolset D')
    toolset4.add_script_tool(tool4)

    tbx = Toolbox(name='toolsets_with_tools')
    tbx.add_script_tool(tool_root)
    tbx.add_toolset(toolset1)
    tbx.add_toolset(toolset2)
    tbx.add_toolset(toolset3)
    tbx.add_toolset(toolset4)

    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_with_toolsets_and_tools_plus_root function


def test_toolbox_save_bogus_path(tmp_path):
    """
    Test toolbox save when using a bogus path
    """
    tbx = Toolbox(name='bob')
    assert tbx.save(tmp_path / 'loblaw') is None
# End test_toolbox_save_bogus_path function


def test_toolbox_get_toolbox_path(tmp_path):
    """
    Test Toolbox _get_toolbox_path method
    """
    tbx = Toolbox(name='bob')
    expected = tmp_path.joinpath('bob.atbx')
    assert not expected.is_file()
    path = tbx._get_toolbox_path(tmp_path, overwrite=True)
    assert not path.is_file()
    assert path == expected
    tbx.save(tmp_path)
    assert path.is_file()
    with raises(FileExistsError):
        tbx._get_toolbox_path(tmp_path, overwrite=False)
    assert path.is_file()
    tbx._get_toolbox_path(tmp_path, overwrite=True)
    assert not path.is_file()
# End test_toolbox_get_toolbox_path function


@mark.parametrize('name', [
    'example', None
])
def test_toolbox_validate_name(name):
    """
    Test Toolbox validate_name method
    """
    if name:
        assert Toolbox._validate_name(name) == name
    else:
        with raises(ValueError):
            Toolbox._validate_name(name)
# End test_toolbox_validate_name function


def test_toolbox_validate_alias_raise():
    """
    Test Toolbox validate_alias method, exception
    """
    with raises(ValueError):
        Toolbox(name='1234')
# End test_toolbox_validate_alias_raise function


if __name__ == '__main__':  # pragma: no cover
    pass
