# -*- coding: utf-8 -*-
"""
Script Tool Class Tests
"""


from json import loads

from pytest import mark, raises

from autobox import ScriptTool
from autobox.constant import (
    SCRIPT_STUB, ScriptToolContentKeys, TOOL_CONTENT, TOOL_CONTENT_RC,
    TOOL_ICON, TOOL_ILLUSTRATION, TOOL_SCRIPT_EXECUTE_LINK,
    TOOL_SCRIPT_EXECUTE_PY, TOOL_SCRIPT_VALIDATE_PY)
from autobox.parameter import FeatureClassParameter
from helpers import DATETIME_PATTERN, read_from_zip
from autobox.script import ExecutionScript, ValidationScript
from autobox.type import ToolAttributes


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
        assert tool.execution_script is None
# End test_script_tool_validate_name function


def test_script_tool_repr():
    """
    Test Script Tool Representation
    """
    assert repr(ScriptTool(name='AbCdE')) == "ScriptTool(name='AbCdE', label='AbCdE', description=None)"
# End test_script_tool_repr function


def test_script_tool_bad_add():
    """
    Test Toolset Bad Add
    """
    tbx = ScriptTool(name='AbCdE')
    with raises(TypeError):
        tbx.add_parameter(1)
# End test_toolset_bad_add function


def test_script_parameter_repetition():
    """
    Test script parameter repetition
    """
    fc1 = FeatureClassParameter(label='asdf', name='ASDF123')
    fc2 = FeatureClassParameter(label='asdf', name='asdf123')
    tool = ScriptTool(name='A_Tool', label='A Tool')
    tool.add_parameter(fc1)
    tool.add_parameter(fc2)
    with raises(ValueError):
        tool._check_parameter_repeats()
# End test_script_parameter_repetition function


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
    script_folder = tool.serialize(tmp_path, compare_path)
    assert script_folder.is_dir()
    assert script_folder.name == 'Script.tool'

    exec_path = script_folder.joinpath(TOOL_SCRIPT_EXECUTE_PY)
    assert exec_path.is_file()
    source_script = exec_path.read_text()
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
    images_path = data_path.joinpath('images')
    assert images_path.is_dir()
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
    tool.icon = images_path.joinpath('python_icon.png')
    tool.illustration = images_path.joinpath('numpy_illustration.png')

    script_folder = tool.serialize(tmp_path, compare_path)
    assert script_folder.is_dir()
    assert script_folder.name == 'TheScriptNameSansSpaces.tool'

    exec_path = script_folder.joinpath(TOOL_SCRIPT_EXECUTE_PY)
    assert exec_path.is_file()
    source_script = exec_path.read_text()
    assert source_script == SCRIPT_STUB

    source_content = loads(script_folder.joinpath(TOOL_CONTENT).read_text())
    source_resource = loads(script_folder.joinpath(TOOL_CONTENT_RC).read_text())
    compare_content = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT}', as_json=True)
    compare_resource = read_from_zip(compare_path, name=f'{script_folder.name}/{TOOL_CONTENT_RC}', as_json=True)

    assert script_folder.joinpath(f'{TOOL_ICON}.png').is_file()
    assert script_folder.joinpath(f'{TOOL_ILLUSTRATION}.png').is_file()

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


def test_execution_script_instantiation():
    """
    Test instantiation of ExecutionScript
    """
    es = ExecutionScript()
    assert not es._code
    assert not es._path
    assert not es._embed
# End test_execution_script_instantiation function


def test_execution_script_from_code():
    """
    Test
    """
    with raises(ValueError):
        ExecutionScript.from_code('')
    with raises(ValueError):
        ExecutionScript.from_code(None)
    es = ExecutionScript.from_code('print("Hello World")')
    assert es._code
    assert not es._path
    assert es._embed
    assert es._get_file_name() == TOOL_SCRIPT_EXECUTE_PY
# End test_execution_script_from_code function


@mark.parametrize('embed, expected', [
    (True, TOOL_SCRIPT_EXECUTE_PY),
    (False, TOOL_SCRIPT_EXECUTE_LINK),
])
def test_execution_script_from_file(data_path, embed, expected):
    """
    Test Execution Script from File
    """
    scripts_path = data_path / 'scripts'
    assert scripts_path.is_dir()
    with raises(ValueError):
        ExecutionScript.from_file(None, embed=True)
    with raises(FileNotFoundError):
        ExecutionScript.from_file('', embed=True)
    es = ExecutionScript.from_file(scripts_path / 'example.py', embed=embed)
    assert not es._code
    assert es._path
    assert es._embed is embed
    assert es._get_file_name() == expected
# End test_execution_script_from_file function


@mark.parametrize('embed, expected', [
    (True, 'from numpy import ndarray'),
    (False, '..\\..\\example.py')
])
def test_execution_script_get_content_relative(data_path, embed, expected):
    """
    Test Execution Script, embedded or relative path
    """
    execution_path = data_path / 'scripts'
    assert execution_path.is_dir()
    es = ExecutionScript()
    with raises(ValueError):
        es._get_content(None)
    es = ExecutionScript.from_file(execution_path / 'example.py', embed=embed)
    assert es._get_content(execution_path) == expected
# End test_execution_script_get_content_relative function


@mark.parametrize('embed, expected', [
    (True, 'from numpy import ndarray'),
    (False, '..')
])
def test_execution_script_get_content_absolute(tmp_path, data_path, embed, expected):
    """
    Test Execution Script, embedded or absolute path
    """
    execution_path = data_path / 'scripts'
    assert execution_path.is_dir()
    es = ExecutionScript()
    with raises(ValueError):
        es._get_content(None)
    name = 'example.py'
    es = ExecutionScript.from_file(execution_path / name, embed=embed)
    if embed:
        assert es._get_content(tmp_path) == expected
    else:
        assert not es._get_content(tmp_path).startswith(expected)
        assert es._get_content(tmp_path).endswith(name)
# End test_execution_script_get_content_absolute function


def test_validation_script_instantiation():
    """
    Test instantiation of ValidationScript
    """
    es = ValidationScript()
    assert not es._code
    assert not es._path
    assert es._embed
# End test_validation_script_instantiation function


def test_validation_script_from_code():
    """
    Test
    """
    with raises(ValueError):
        ValidationScript.from_code('')
    with raises(ValueError):
        ValidationScript.from_code(None)
    es = ValidationScript.from_code('print("Hello World")')
    assert es._code
    assert not es._path
    assert es._embed
    assert es._get_file_name() == TOOL_SCRIPT_VALIDATE_PY
# End test_validation_script_from_code function


def test_validation_script_from_file(data_path):
    """
    Test Validation Script from File
    """
    scripts_path = data_path / 'scripts'
    assert scripts_path.is_dir()
    with raises(ValueError):
        ValidationScript.from_file(None)
    with raises(FileNotFoundError):
        ValidationScript.from_file('')
    es = ValidationScript.from_file(scripts_path / 'validator.py')
    assert not es._code
    assert es._path
    assert es._embed
    assert es._get_file_name() == TOOL_SCRIPT_VALIDATE_PY
# End test_validation_script_from_file function


def test_script_images(data_path):
    """
    Test Script Images (icon and illustration)
    """
    images_path = data_path.joinpath('images')
    assert images_path.is_dir()
    tif_image = images_path.joinpath('python_icon.tif')
    tool = ScriptTool(name='bob')
    tool.icon = None
    tool.illustration = None

    with raises(ValueError):
        tool.icon = Ellipsis
    with raises(FileNotFoundError):
        tool.icon = 'python_icon.png'
    with raises(TypeError):
        tool.icon = tif_image

    with raises(ValueError):
        tool.illustration = Ellipsis
    with raises(FileNotFoundError):
        tool.illustration = 'python_icon.png'
    with raises(TypeError):
        tool.illustration = tif_image
# End test_script_images function


if __name__ == '__main__':  # pragma: no cover
    pass
