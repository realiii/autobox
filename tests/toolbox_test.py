# -*- coding: utf-8 -*-
"""
Toolbox Class Tests
"""

from pytest import mark, raises

from helpers import read_from_zip
from stoolbox import ScriptTool
from stoolbox.toolbox import Toolbox
from stoolbox.constants import EXT, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC
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
