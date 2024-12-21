# -*- coding: utf-8 -*-
"""
Script Tool Class Tests
"""


from json import loads

from pytest import mark, raises

from stoolbox import ScriptTool
from stoolbox.constants import (
    SCRIPT_STUB, ScriptToolContentKeys, TOOL_CONTENT, TOOL_CONTENT_RC,
    TOOL_SCRIPT)
from helpers import DATETIME_PATTERN, read_from_zip
from stoolbox.types import ToolAttributes


@mark.parametrize('name, expected', [
    ('good', 'good'),
    ('not good', 'notgood'),
    ('12345asdf', 'asdf'),
    (None, None),
    ('', None),
    ('  ', None),
    ('12345', None),
])
def test_script_tool_validate_name(name, expected):
    """
    Test Script Tool Validate Name
    """
    if not expected:
        with raises(ValueError):
            ScriptTool(name)
    else:
        tool = ScriptTool(name)
        assert tool.name == expected
        assert tool.label == expected
        assert tool.description is None
        assert tool.summary is None
        assert tool.execution_script
# End test_script_tool_validate_name function


@mark.parametrize('label, expected', [
    ('good', 'good'),
    ('not good', 'not good'),
    ('12345asdf', '12345asdf'),
    (None, 'bob'),
    ('', 'bob'),
    ('  ', 'bob'),
    ('12345', '12345'),
])
def test_script_tool_validate_label(label, expected):
    """
    Test Script Tool Validate Label
    """
    tool = ScriptTool(name='bob', label=label)
    assert tool.label == expected
# End test_script_tool_validate_label function


def test_script_tool_serialize_root_simple(tmp_path, data_path):
    """
    Test Script Tool Serialize, simple
    """
    compare_path = data_path.joinpath('root_script_simple.atbx')
    assert compare_path.is_file()
    tool = ScriptTool(name='Script')
    script_folder = tool.serialize(tmp_path)
    assert script_folder.is_dir()
    assert script_folder.name == 'Script.tool'

    assert script_folder.joinpath(TOOL_SCRIPT).is_file()
    source_script = script_folder.joinpath(TOOL_SCRIPT).read_text()
    assert source_script == SCRIPT_STUB

    source_content = loads(script_folder.joinpath(TOOL_CONTENT).read_text())
    source_resource = loads(script_folder.joinpath(TOOL_CONTENT_RC).read_text())
    compare_content = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT}', as_json=True)
    compare_resource = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT_RC}', as_json=True)

    updated = ScriptToolContentKeys.updated
    assert updated in source_content
    assert DATETIME_PATTERN.match(source_content[updated])
    source_content.pop(updated)
    assert updated in compare_content
    assert DATETIME_PATTERN.match(compare_content[updated])
    compare_content.pop(updated)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_script_tool_serialize_root_simple function


def test_script_tool_serialize_root(tmp_path, data_path):
    """
    Test Script Tool Serialize
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
    script_folder = tool.serialize(tmp_path)
    assert script_folder.is_dir()
    assert script_folder.name == 'TheScriptNameSansSpaces.tool'

    assert script_folder.joinpath(TOOL_SCRIPT).is_file()
    source_script = script_folder.joinpath(TOOL_SCRIPT).read_text()
    assert source_script == SCRIPT_STUB

    source_content = loads(script_folder.joinpath(TOOL_CONTENT).read_text())
    source_resource = loads(script_folder.joinpath(TOOL_CONTENT_RC).read_text())
    compare_content = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT}', as_json=True)
    compare_resource = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT_RC}', as_json=True)

    updated = ScriptToolContentKeys.updated
    assert updated in source_content
    assert DATETIME_PATTERN.match(source_content[updated])
    source_content.pop(updated)
    assert updated in compare_content
    assert DATETIME_PATTERN.match(compare_content[updated])
    compare_content.pop(updated)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_script_tool_serialize_root function


if __name__ == '__main__':  # pragma: no cover
    pass
