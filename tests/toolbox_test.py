# -*- coding: utf-8 -*-
"""
Toolbox Class Tests
"""


from shutil import copyfile

from pytest import approx, mark, raises

from autobox.enum import (
    ArealUnit, FieldType, GeometryType, LinearUnit, WorkspaceType)
from autobox.filter import (
    ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, WorkspaceTypeFilter)
from helpers import DEFAULT_EXECUTION_CODE, read_from_zip
from autobox import ScriptTool
from autobox.parameter import (
    ArealUnitParameter, DoubleParameter, FeatureClassParameter,
    FeatureDatasetParameter, FeatureLayerParameter, FieldParameter,
    FileParameter, LinearUnitParameter, LongParameter, RasterDatasetParameter,
    StringParameter, TableParameter, TinParameter, WorkspaceParameter)
from autobox.script import ExecutionScript, ValidationScript
from autobox.toolbox import Toolbox
from autobox.constant import (
    DOT, EXT, ScriptToolContentKeys, TOOL, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC,
    TOOL_CONTENT, TOOL_CONTENT_RC, TOOL_SCRIPT_EXECUTE_LINK,
    TOOL_SCRIPT_EXECUTE_PY, TOOL_SCRIPT_VALIDATE_PY)
from autobox.toolset import Toolset
from autobox.type import ToolAttributes


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


def test_toolbox_repr():
    """
    Test Toolbox Representation
    """
    assert repr(Toolbox(name='AbCdE')) == "Toolbox(name='AbCdE', label='AbCdE', alias='AbCdE', description=None)"
# End test_toolbox_repr function


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


def test_toolbox_with_toolsets_and_tools(tmp_path):
    """
    Test a Toolbox that has toolsets and tools, no root tools
    """
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
    tbx.add_toolset(toolset2)
    tbx.add_toolset(toolset1)

    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()
    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = {
        'alias': 'toolsetnoroot', 'displayname': '$rc:title', 'toolsets': {
            '$rc:toolset1.name': {
                'tools': ['ScriptInToolset', 'SubScriptInToolset']},
            '$rc:toolset2.name': {'tools': ['AScript']},
            '$rc:toolset3.name': {'tools': ['BScript']},
            '$rc:toolset4.name': {'tools': ['CScript']}, '$rc:toolset5.name': {
                'tools': ['Anudder', 'SecondScriptInToolset',
                          'SecondSubScriptInToolset']}},
        'version': '1.0'
    }
    compare_resource = {
        'map': {'title': 'toolset_no_root',
                'toolset1.name': 'His Tools',
                'toolset2.name': 'Her Tools\\A Toolset',
                'toolset3.name': 'Her Tools\\B Toolset',
                'toolset4.name': 'Her Tools\\C Toolset',
                'toolset5.name': 'His Tools\\Another Toolset'}
    }

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_with_toolsets_and_tools function


def test_toolbox_with_execution_scripts(tmp_path, data_path):
    """
    Test Toolbox with Execution Scripts (varying configurations)
    """
    compare_path = data_path.joinpath('script_execute.atbx')
    assert compare_path.is_file()

    scripts_path = data_path / 'scripts'
    assert scripts_path.is_dir()
    example_name = 'example.py'
    example = scripts_path / example_name
    assert example.is_file()
    example_sub = scripts_path / 'subfolder' / example_name
    assert example_sub.is_file()

    name = 'simple.py'
    tmp_example = tmp_path / name
    copyfile(scripts_path / 'c_software' / name, tmp_example)

    tbx = Toolbox(name='script_execute')
    tool1 = ScriptTool(name='ScriptEmbeddedDefaultScript', label='Embedded Script (Default Script)')
    tool1.execution_script = ExecutionScript.from_code(DEFAULT_EXECUTION_CODE)
    tool2 = ScriptTool(name='ScriptPathAlongsideToolbox', label='Script Path Alongside Toolbox')
    tool2.execution_script = ExecutionScript.from_file(example, embed=False)
    tool3 = ScriptTool(name='ScriptPathAlongsideToolboxEmbedded', label='Script Path Alongside Toolbox (Embedded)')
    tool3.execution_script = ExecutionScript.from_file(example, embed=True)
    tool4 = ScriptTool(name='ScriptPathDifferentLocation', label='Script Path Different Location')
    tool4.execution_script = ExecutionScript.from_file(tmp_example, embed=False)
    tool5 = ScriptTool(name='ScriptPathDifferentLocationEmbedded', label='Script Path Different Location (Embedded)')
    tool5.execution_script = ExecutionScript.from_file(tmp_example, embed=True)
    tool6 = ScriptTool(name='ScriptPathSubFolderAlongsideToolbox', label='Script Path Sub Folder Alongside Toolbox')
    tool6.execution_script = ExecutionScript.from_file(example_sub, embed=False)
    tool7 = ScriptTool(name='ScriptPathSubFolderAlongsideToolboxEmbedded', label='Script Path Sub Folder Alongside Toolbox (Embedded)')
    tool7.execution_script = ExecutionScript.from_file(example_sub, embed=True)

    for tool in [tool1, tool2, tool3, tool4, tool5, tool6, tool7]:
        tbx.add_script_tool(tool)

    tbx_path = tbx.save(scripts_path, overwrite=True)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource

    exe1 = read_from_zip(tbx_path, name=f'{tool1.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_PY}', as_json=False)
    assert exe1 == DEFAULT_EXECUTION_CODE
    exe2 = read_from_zip(tbx_path, name=f'{tool2.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_LINK}', as_json=False)
    assert exe2.startswith('..\\..') and exe2.endswith(example_name)
    exe3 = read_from_zip(tbx_path, name=f'{tool3.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_PY}', as_json=False)
    assert exe3 == 'from numpy import ndarray'
    exe4 = read_from_zip(tbx_path, name=f'{tool4.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_LINK}', as_json=False)
    assert not exe4.startswith('..') and exe4.endswith(name)
    exe5 = read_from_zip(tbx_path, name=f'{tool5.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_PY}', as_json=False)
    assert exe5 == 'from numpy import ndarray'
    exe6 = read_from_zip(tbx_path, name=f'{tool6.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_LINK}', as_json=False)
    assert exe6.startswith('..') and exe6.endswith(example_name) and 'subfolder' in exe6
    exe7 = read_from_zip(tbx_path, name=f'{tool7.name}{DOT}{TOOL}/{TOOL_SCRIPT_EXECUTE_PY}', as_json=False)
    assert exe7 == 'from numpy import ndarray, abs as abs_'

    tbx_path.unlink()
# End test_toolbox_with_execution_scripts function


def test_toolbox_with_validation_script(tmp_path, data_path):
    """
    Test Toolbox with Validation Script (varying configurations)
    """
    compare_path = data_path.joinpath('script_validate.atbx')
    assert compare_path.is_file()

    scripts_path = data_path / 'scripts'
    assert scripts_path.is_dir()
    validator = scripts_path / 'validator.py'
    assert validator.is_file()

    tbx = Toolbox(name='script_validate')
    tool1 = ScriptTool(name='ScriptDefaultValidation', label='Script Default Validation')
    tool2 = ScriptTool(name='ScriptCustomValidation', label='Script Custom Validation')
    tool2.validation_script = ValidationScript.from_file(validator)

    tbx.add_script_tool(tool1)
    tbx.add_script_tool(tool2)

    tbx_path = tbx.save(tmp_path, overwrite=True)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource

    with raises(KeyError):
        read_from_zip(tbx_path, name=f'{tool1.name}{DOT}{TOOL}/{TOOL_SCRIPT_VALIDATE_PY}', as_json=False)

    exe2 = read_from_zip(tbx_path, name=f'{tool2.name}{DOT}{TOOL}/{TOOL_SCRIPT_VALIDATE_PY}', as_json=False)
    assert 'class ToolValidator' in exe2
# End test_toolbox_with_validation_script function


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


def test_build_parameters_toolbox(tmp_path, data_path):
    """
    Build Parameters Toolbox
    """
    compare_path = data_path.joinpath('parameters.atbx')
    assert compare_path.is_file()

    param1 = StringParameter(
        label='Simple String Label', name='Simple_String_Name',
        category='cat 1', description='plain text description',
        default_value='the quick brown fox')
    param2 = StringParameter(
        label='Multi String Label', name='multi_string_name', category='cat 1',
        description='<p><b>all bold</b></p>',
        default_value=('jumps over the', 'second line', 'includes "double quote" characters', "includes 'single quote' characters"),
        is_required=False, is_multi=True)
    param3 = StringParameter(
        label='Derived String Label', name='DerivedStringName', category='cat 2',
        description='<p><span style=\"text-decoration:underline;\">underline </span><span>and </span><i>emphasis</i></p>',
        default_value='lazy dog')
    param3.set_derived()
    tool1 = ScriptTool(name='ScriptWithStringParameters', label='Script with String Parameters')
    for p in param1, param2, param3:
        tool1.add_parameter(p)

    param1 = WorkspaceParameter(label='Workspaces', name='workspaces', description='Allow for multiple workspaces', is_multi=True)
    param2 = WorkspaceParameter(label='Output Workspace', name='output_workspace_name', is_input=False)
    param3 = FeatureDatasetParameter(label='A Feature Dataset', name='a_feature_dataset_name', is_input=False)
    param4 = FeatureClassParameter(label='Main Feature Class', name='main_feature_class_name', is_input=False, is_required=False)
    param5 = FeatureClassParameter(label='Feature Class Input', name='feature_class_input_name')
    param6 = FeatureLayerParameter(label='Feature Layer Example', name='feature_layer_example')
    param7 = RasterDatasetParameter(label='Raster Dataset Input', name='raster_dataset_input_name')
    param8 = RasterDatasetParameter(label='Raster Dataset Output', name='raster_dataset_output_name', is_input=False)
    param9 = TinParameter(label='Tin Man', name='tin_man_name')
    param10 = TableParameter(label='Table Input', name='table_input_name')
    param11 = TableParameter(label='Table Output', name='table_output_name', is_input=False)
    tool2 = ScriptTool(name='ScriptWithDataElementParameters', label='Script with Data Element Parameters')
    for p in param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11:
        tool2.add_parameter(p)

    param1 = LongParameter(label='Long', name='long_name', default_value=123)
    param2 = LongParameter(label='Long Multi', name='long_multi_name', default_value=(12, 34, 56), is_multi=True)
    param3 = DoubleParameter(label='Double', name='double_name', default_value=123.456)
    param4 = DoubleParameter(label='Double Multi', name='double_multi_name', default_value=(23.456, 789.1), is_multi=True)
    tool3 = ScriptTool(name='ScriptWithNumericParameters', label='Script with Numeric Parameters')
    for p in param1, param2, param3, param4:
        tool3.add_parameter(p)

    tbx = Toolbox(name='parameters', label='parameters', alias='parameters')
    tbx.add_script_tool(tool1)
    tbx.add_script_tool(tool2)
    tbx.add_script_tool(tool3)

    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource

    updated = ScriptToolContentKeys.updated

    name = f'{tool1.name}{DOT}{TOOL}/{TOOL_CONTENT}'
    source_content = read_from_zip(tbx_path, name=name, as_json=True)
    compare_content = read_from_zip(compare_path, name=name, as_json=True)
    source_content.pop(updated)
    compare_content.pop(updated)
    assert source_content == compare_content

    name = f'{tool1.name}{DOT}{TOOL}/{TOOL_CONTENT_RC}'
    source_resource = read_from_zip(tbx_path, name=name, as_json=True)
    compare_resource = read_from_zip(compare_path, name=name, as_json=True)
    assert source_resource == compare_resource

    name = f'{tool2.name}{DOT}{TOOL}/{TOOL_CONTENT}'
    source_content = read_from_zip(tbx_path, name=name, as_json=True)
    compare_content = read_from_zip(compare_path, name=name, as_json=True)
    source_content.pop(updated)
    compare_content.pop(updated)
    assert source_content == compare_content

    name = f'{tool2.name}{DOT}{TOOL}/{TOOL_CONTENT_RC}'
    source_resource = read_from_zip(tbx_path, name=name, as_json=True)
    compare_resource = read_from_zip(compare_path, name=name, as_json=True)
    assert source_resource == compare_resource

    name = f'{tool3.name}{DOT}{TOOL}/{TOOL_CONTENT}'
    source_content = read_from_zip(tbx_path, name=name, as_json=True)
    compare_content = read_from_zip(compare_path, name=name, as_json=True)
    source_content.pop(updated)
    compare_content.pop(updated)
    assert source_content == compare_content

    name = f'{tool3.name}{DOT}{TOOL}/{TOOL_CONTENT_RC}'
    source_resource = read_from_zip(tbx_path, name=name, as_json=True)
    compare_resource = read_from_zip(compare_path, name=name, as_json=True)
    assert source_resource == compare_resource
# End test_build_parameters_toolbox function


def test_build_filter_parameter_toolbox(tmp_path, data_path):
    """
    Test build filter parameter toolbox
    """
    compare_path = data_path.joinpath('filter.atbx')
    assert compare_path.is_file()

    workspace = WorkspaceParameter(label='Workspace', name='Workspace')
    workspace.category = 'Elements'
    workspace.filter = WorkspaceTypeFilter((WorkspaceType.FILE_SYSTEM,))
    feature_class = FeatureClassParameter(label='Feature Class', name='Feature_Class')
    feature_class.category = 'Elements'
    feature_class.filter = FeatureClassTypeFilter((GeometryType.POLYGON, GeometryType.POLYLINE))
    feature_layer = FeatureLayerParameter(label='Feature Layer', name='Feature_Layer')
    feature_layer.category = 'Elements'
    feature_layer.filter = FeatureClassTypeFilter((GeometryType.POINT, GeometryType.MULTIPOINT))
    field = FieldParameter(label='Field Type', name='Field_Type')
    field.category = 'Elements'
    field.filter = FieldTypeFilter((FieldType.SHORT, FieldType.LONG, FieldType.BIG_INTEGER))
    field.dependency = feature_layer
    file = FileParameter(label='File Type', name='File_Type')
    file.category = 'Elements'
    file.filter = FileTypeFilter(('txt', 'csv'))

    areal = ArealUnitParameter(label='Areal Unit', name='Areal_Unit')
    areal.category = 'Units'
    areal.filter = ArealUnitFilter((ArealUnit.ARES, ArealUnit.HECTARES))
    areal.dependency = feature_class
    linear = LinearUnitParameter(label='Linear Unit', name='Linear_Unit')
    linear.category = 'Units'
    linear.filter = LinearUnitFilter((LinearUnit.METERS, LinearUnit.KILOMETERS))
    linear.dependency = feature_layer

    long_value = LongParameter(label='Long Value', name='Long_Value')
    long_value.category = 'Value Filters'
    long_value.filter = LongValueFilter((1, 2, 3))
    double_value = DoubleParameter(label='Double Value', name='Double_Value')
    double_value.category = 'Value Filters'
    double_value.filter = DoubleValueFilter((1.1, 2.22, 3.333))
    string_value = StringParameter(label='String Value', name='String_Value')
    string_value.category = 'Value Filters'
    string_value.filter = StringValueFilter(('A', 'BB', 'C"""C', "D'''C"))

    long_range = LongParameter(label='Long Range', name='Long_Range')
    long_range.category = 'Range Filters'
    long_range.filter = LongRangeFilter(-1, 9876543210)
    double_range = DoubleParameter(label='Double Range', name='Double_Range')
    double_range.category = 'Range Filters'
    double_range.filter = DoubleRangeFilter(-999.999, 9876.543)

    script = ScriptTool(name='ScriptWithFilters', label='Script with Filters')
    for p in (workspace, feature_class, feature_layer, field, file,
              areal, linear, long_value, double_value, string_value,
              long_range, double_range):
        script.add_parameter(p)
    tbx = Toolbox(name='filter', label='filter', alias='filter')
    tbx.add_script_tool(script)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()

    source_content = read_from_zip(tbx_path, name=TOOLBOX_CONTENT, as_json=True)
    source_resource = read_from_zip(tbx_path, name=TOOLBOX_CONTENT_RC, as_json=True)
    compare_content = read_from_zip(compare_path, name=TOOLBOX_CONTENT, as_json=True)
    compare_resource = read_from_zip(compare_path, name=TOOLBOX_CONTENT_RC, as_json=True)

    assert source_content == compare_content
    assert source_resource == compare_resource

    updated = ScriptToolContentKeys.updated

    name = f'{script.name}{DOT}{TOOL}/{TOOL_CONTENT}'
    source_content = read_from_zip(tbx_path, name=name, as_json=True)
    compare_content = read_from_zip(compare_path, name=name, as_json=True)
    source_content.pop(updated)
    compare_content.pop(updated)

    source_params = source_content.pop('params')
    compare_params = compare_content.pop('params')
    source_double_range = source_params.pop(double_range.name)
    compare_double_range = compare_params.pop(double_range.name)

    source_domain = source_double_range.pop('domain')
    _ = compare_double_range.pop('domain')

    assert source_double_range == compare_double_range

    assert source_domain['type'] == 'GPRangeDomain'
    min_value = float(source_domain['min'])
    max_value = float(source_domain['max'])
    assert approx((-999.999, 9876.543), abs=0.001) == (min_value, max_value)

    assert source_double_range == compare_double_range
    assert source_params == compare_params
    assert source_content == compare_content

    name = f'{script.name}{DOT}{TOOL}/{TOOL_CONTENT_RC}'
    source_resource = read_from_zip(tbx_path, name=name, as_json=True)
    compare_resource = read_from_zip(compare_path, name=name, as_json=True)
    assert source_resource == compare_resource
# End test_build_filter_parameter_toolbox function


def test_toolbox_toolset_repetition(tmp_path):
    """
    Test catching toolset repetition on a toolbox
    """
    tool = ScriptTool(name='A_Tool', label='A Tool')
    tbx = Toolbox(name='pete')
    toolset1 = Toolset(name='A Toolset')
    toolset1.add_script_tool(tool)
    tbx.add_toolset(toolset1)
    tbx.add_toolset(toolset1)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)

    tbx = Toolbox(name='pete')
    toolset2 = Toolset(name='A Toolset')
    for toolset in toolset1, toolset2:
        toolset.add_script_tool(tool)
        tbx.add_toolset(toolset)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)

    tbx = Toolbox(name='pete')
    toolset1 = Toolset(name='A Toolset')
    toolset2 = Toolset(name='B Toolset')
    toolset3 = Toolset(name='B Toolset')
    for toolset in toolset2, toolset3:
        toolset.add_script_tool(tool)
        toolset1.add_toolset(toolset)
    tbx.add_toolset(toolset1)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)
# End test_toolbox_toolset_repetition function


def test_toolbox_script_repetition(tmp_path):
    """
    Test catching script tool repetition on a toolbox
    """
    toolset1 = Toolset(name='A Toolset')
    toolset2 = Toolset(name='A Toolset')
    tool1 = ScriptTool(name='A_Tool', label='A Tool')
    tool2 = ScriptTool(name='A_Tool', label='A Tool')

    tbx = Toolbox(name='pete')
    tbx.add_script_tool(tool1)
    tbx.add_script_tool(tool1)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)

    tbx = Toolbox(name='pete')
    tbx.add_script_tool(tool1)
    tbx.add_script_tool(tool2)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)

    tbx = Toolbox(name='pete')
    toolset1.add_script_tool(tool1)
    tbx.add_toolset(toolset1)
    tbx.add_script_tool(tool2)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)

    tbx = Toolbox(name='pete')
    toolset1.add_script_tool(tool1)
    toolset2.add_script_tool(tool2)
    tbx.add_toolset(toolset1)
    tbx.add_toolset(toolset2)
    with raises(ValueError):
        tbx.save(tmp_path, overwrite=True)
# End test_toolbox_script_repetition function


if __name__ == '__main__':  # pragma: no cover
    pass
