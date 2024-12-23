# -*- coding: utf-8 -*-
"""
Constants
"""


from typing import ClassVar


DOT: str = '.'
SPACE: str = ' '
UNDERSCORE: str = '_'
COLON: str = ':'
DOUBLE_SPACE: str = f'{SPACE}{SPACE}'
DOUBLE_UNDERSCORE: str = f'{UNDERSCORE}{UNDERSCORE}'


EXT: str = '.atbx'
PY: str = '.py'

RC: str = 'rc'
DOLLAR_RC: str = f'${RC}{COLON}'
CONTENT: str = 'content'
NAME: str = 'name'

TOOL: str = 'tool'
SCRIPT: str = 'script'
EXECUTE: str = 'execute'
TOOLSET: str = f'{TOOL}set'
TOOLBOX: str = f'{TOOL}box'

TOOL_CONTENT: str = f'{TOOL}{DOT}{CONTENT}'
TOOL_CONTENT_RC: str = f'{TOOL_CONTENT}{DOT}{RC}'
TOOL_SCRIPT: str = f'{TOOL}{DOT}{SCRIPT}{DOT}'
TOOL_SCRIPT_EXECUTE: str = f'{TOOL_SCRIPT}{EXECUTE}'
TOOL_SCRIPT_EXECUTE_PY: str = f'{TOOL_SCRIPT_EXECUTE}{PY}'
TOOL_SCRIPT_VALIDATE_PY: str = f'{TOOL_SCRIPT}validate{PY}'
TOOL_SCRIPT_EXECUTE_LINK: str = f'{TOOL_SCRIPT_EXECUTE}{DOT}link'
TOOLBOX_CONTENT: str = f'{TOOLBOX}{DOT}{CONTENT}'
TOOLBOX_CONTENT_RC: str = f'{TOOLBOX_CONTENT}{DOT}{RC}'


SCRIPT_STUB: str = '''
# -*- coding: utf-8 -*-
"""
Documentation
"""


import arcpy


def example_script_tool(feature_class, field_name):
    """
    Documentation
    """
    return


if __name__ == '__main__':
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    example_script_tool(param0, param1)
    arcpy.SetParameterAsText(2, 'Result')

'''


class BaseContentKeys:
    """
    Base Content Keys
    """
    display_name: ClassVar[str] = 'displayname'
    description: ClassVar[str] = 'description'
# End BaseContentKeys class


class ToolboxContentKeys(BaseContentKeys):
    """
    Toolbox Content Keys
    """
    version: ClassVar[str] = 'version'
    alias: ClassVar[str] = 'alias'
    toolsets: ClassVar[str] = 'toolsets'
    tools: ClassVar[str] = 'tools'
    root: ClassVar[str] = '<root>'
# End ToolboxContentKeys class


class ScriptToolContentKeys(BaseContentKeys):
    """
    Script Tool Content Keys
    """
    type: ClassVar[str] = 'type'
    application_version: ClassVar[str] = 'app_ver'
    attributes: ClassVar[str] = 'attributes'
    product: ClassVar[str] = 'product'
    updated: ClassVar[str] = 'updated'
    parameters: ClassVar[str] = 'params'
# End ScriptToolContentKeys class


class BaseResourceKeys:
    """
    Base Resource Keys
    """
    map: ClassVar[str] = 'map'
    title: ClassVar[str] = 'title'
# End BaseResourceKeys class


class ToolboxContentResourceKeys(BaseResourceKeys):
    """
    Toolbox Content Resource Keys
    """
    description: ClassVar[str] = 'descr'
# End ToolboxContentResourceKeys class


class ScriptToolContentResourceKeys(BaseResourceKeys):
    """
    Script Tool Content Resource Keys
    """
    description: ClassVar[str] = 'description'
    summary: ClassVar[str] = 'summary'
# End ScriptToolContentResourceKeys class


class ToolAttributeKeywords:
    """
    Tool Attribute Keywords
    """
    show_modifies_input: ClassVar[str] = 'input_data_change'
    do_not_add_to_map: ClassVar[str] = 'block_add_to_map'
    show_enable_undo: ClassVar[str] = 'edit_session'
    show_consumes_credits: ClassVar[str] = 'credits'

    ordered: tuple[str, str, str, str] = (
        show_modifies_input,
        do_not_add_to_map,
        show_enable_undo,
        show_consumes_credits,
    )
# End ToolAttributeKeywords class


if __name__ == '__main__':  # pragma: no cover
    pass
