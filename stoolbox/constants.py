# -*- coding: utf-8 -*-
"""
Constants
"""


from typing import ClassVar


SPACE: str = ' '
UNDERSCORE: str = '_'
DOUBLE_UNDERSCORE: str = f'{UNDERSCORE}{UNDERSCORE}'
EXT: str = '.atbx'
RC: str = 'rc'
DOLLAR_RC: str = f'${RC}:'
TOOLBOX_CONTENT: str = 'toolbox.content'
TOOLBOX_CONTENT_RC: str = f'{TOOLBOX_CONTENT}.{RC}'


class ToolboxContentKeys:
    """
    Toolbox Content Keys
    """
    version: ClassVar[str] = 'version'
    alias: ClassVar[str] = 'alias'
    display_name: ClassVar[str] = 'displayname'
    description: ClassVar[str] = 'description'
    toolsets: ClassVar[str] = 'toolsets'
    tools: ClassVar[str] = 'tools'
    root: ClassVar[str] = '<root>'
# End ToolboxContentKeys class


class ToolboxContentResourceKeys:
    """
    Toolbox Content Resource Keys
    """
    map: ClassVar[str] = 'map'
    description: ClassVar[str] = 'descr'
    title: ClassVar[str] = 'title'
# End ToolboxContentResourceKeys class


if __name__ == '__main__':  # pragma: no cover
    pass
