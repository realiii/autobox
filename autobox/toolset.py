# -*- coding: utf-8 -*-
"""
Toolset
"""


from typing import NoReturn, Optional, TYPE_CHECKING

from autobox.constant import ILLUSTRATION, PARENT
from autobox.util import validate_toolset_name


if TYPE_CHECKING:  # pragma: no cover
    from autobox import ScriptTool


class Toolset:
    """
    Toolset
    """
    def __init__(self, name: str) -> None:
        """
        Initialize the Toolset class

        :param name: The name of the toolset, some special characters
            are not allowed.
        """
        super().__init__()
        self._name: str = self._validate_name(name)
        self._toolsets: list['Toolset'] = []
        self._tools: list['ScriptTool'] = []
        self._parent: Optional['Toolset'] = None
    # End init built-in

    def __repr__(self) -> str:
        """
        Class Representation
        """
        return f'{self.__class__.__name__}(name={self.name!r})'
    # End repr built-in

    @staticmethod
    def _validate_name(name: str) -> str | NoReturn:
        """
        Validate Name
        """
        if not (validated_name := validate_toolset_name(name)):
            raise ValueError(f'Invalid toolset name: {name}')
        return validated_name
    # End _validate_name method

    @property
    def name(self) -> str:
        """
        Name
        """
        return self._name
    # End name property

    @property
    def has_tools(self) -> bool:
        """
        Has Tools
        """
        if self.tools:
            return True
        toolsets = list(self.toolsets)
        while toolsets:
            toolset = toolsets.pop(0)
            if toolset.has_tools:  # pragma: no cover
                return True
            toolsets.extend(toolset.toolsets)
        return False
    # End has_tools property

    @property
    def tools(self) -> list['ScriptTool']:
        """
        Tools
        """
        return self._tools
    # End tools property

    @property
    def toolsets(self) -> list['Toolset']:
        """
        Toolsets
        """
        return self._toolsets
    # End toolsets property

    @property
    def parent(self) -> Optional['Toolset']:
        """
        Parent Toolset
        """
        return self._parent

    @parent.setter
    def parent(self, value: Optional['Toolset']) -> None:
        self._parent = value
    # End parent property

    @property
    def qualified_name(self) -> str:
        """
        Qualified Name
        """
        names = [self.name]
        toolset = self.parent
        while toolset:
            names.append(toolset.name)
            toolset = toolset.parent
        return '\\'.join(reversed(names))
    # End qualified_name property

    def add_script_tool(self, tool: 'ScriptTool') -> None:
        """
        Add Script Tool
        """
        if not hasattr(tool, ILLUSTRATION):
            raise TypeError(f'Expected a tool, got: {tool}')
        self.tools.append(tool)
    # End add_script_tool method

    def add_toolset(self, toolset: 'Toolset') -> None:
        """
        Add Toolset
        """
        if not hasattr(toolset, PARENT):
            raise TypeError(f'Expected a toolset, got: {toolset}')
        toolset.parent = self
        self.toolsets.append(toolset)
    # End add_toolset method
# End Toolset class


if __name__ == '__main__':  # pragma: no cover
    pass
