# -*- coding: utf-8 -*-
"""
Toolbox
"""


from json import dump
from operator import attrgetter
from os import walk
from pathlib import Path
from shutil import rmtree
from typing import NoReturn, TYPE_CHECKING, Union
from zipfile import ZIP_DEFLATED, ZipFile

from stoolbox.constants import (
    DOLLAR_RC, DOT, EXT, NAME, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC, TOOLSET,
    ToolboxContentKeys, ToolboxContentResourceKeys)
from stoolbox.types import PATH, STRING, TOOLS_MAP
from stoolbox.util import (
    make_temp_folder, validate_toolbox_alias, validate_toolbox_name)


if TYPE_CHECKING:  # pragma: no cover
    from stoolbox.script import ScriptTool
    from stoolbox.toolset import Toolset


class Toolbox:
    """
    Toolbox
    """
    def __init__(self, name: str, label: STRING = None,
                 alias: STRING = None, description: STRING = None) -> None:
        """
        Initialize the Toolbox class

        :param name: The name of the toolbox file without the extension.
        :param label: An optional label for the toolbox.
        :param alias: An optional alias for the toolbox, must not contain
            spaces, underscores, special characters.  Must start with a letter.
        :param description: An optional description of the toolbox.
        """
        super().__init__()
        self._name: str = self._validate_name(name)
        self._label: str = self._validate_label(label)
        self._alias: str = self._validate_alias(alias)
        self._description: STRING = description
        self._toolsets: list['Toolset'] = []
        self._tools: list['ScriptTool'] = []
    # End init built-in

    @staticmethod
    def _validate_name(name: str) -> str | NoReturn:
        """
        Validate Name
        """
        if not (validated_name := validate_toolbox_name(name)):
            raise ValueError(f'Invalid toolbox name: {name}')
        return validated_name
    # End _validate_name method

    def _validate_alias(self, alias: STRING) -> str | NoReturn:
        """
        Validate Alias
        """
        if not (validated_alias := validate_toolbox_alias(alias)):
            if not (validated_alias := validate_toolbox_alias(self.name)):
                raise ValueError(f'Invalid toolbox alias: {alias}')
        return validated_alias
    # End _validate_alias method

    def _validate_label(self, label: STRING) -> str:
        """
        Validate Label
        """
        if not isinstance(label, str):
            return self.name
        return label.strip() or self.name
    # End _validate_label method

    def _serialize(self, source: Path, target: Path) -> None:
        """
        Serialize Files to Temporary Folder
        """
        content, toolset_names = self._build_content(
            source=source, target=target)
        resource = self._build_resource(toolset_names)
        for name, data in zip((TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC),
                              (content, resource)):
            file_path = source.joinpath(name)
            with file_path.open(
                    mode='w', encoding='utf-8') as fout:
                # noinspection PyTypeChecker
                dump(data, fp=fout, indent=2)
    # End _serialize method

    @staticmethod
    def _save_toolbox(source: Path, target: Path) -> None:
        """
        Save Toolbox
        """
        with ZipFile(target, mode='w', compression=ZIP_DEFLATED) as zout:
            for folder, _, files in walk(source):
                path = Path(folder)
                for f in files:
                    full_path = path.joinpath(f)
                    zout.write(full_path, full_path.relative_to(source))
        rmtree(source)
    # End _save_toolbox method

    def _get_toolbox_path(self, folder: Path, overwrite: bool) \
            -> Union[Path, NoReturn]:
        """
        Get Toolbox Path, if the file exists and overwrite is False raise
        an exception otherwise delete the file and return the path.
        """
        toolbox_path = folder.joinpath(f'{self.name}{EXT}')
        if toolbox_path.is_file():
            if not overwrite:
                raise FileExistsError(f'File already exists: {toolbox_path}')
            else:
                toolbox_path.unlink(missing_ok=True)
        return toolbox_path
    # End _get_toolbox_path method

    def _build_content(self, source: Path, target: Path) -> tuple[
            dict[str, str | dict[str, list]], dict[str, str]]:
        """
        Build Content
        """
        toolsets, toolset_names = self._build_toolsets(
            source=source, target=target)
        mapping = {
            ToolboxContentKeys.version: '1.0',
            ToolboxContentKeys.alias: self.alias,
            ToolboxContentKeys.display_name:
                f'{DOLLAR_RC}{ToolboxContentResourceKeys.title}',
            ToolboxContentKeys.description:
                f'{DOLLAR_RC}{ToolboxContentResourceKeys.description}',
            ToolboxContentKeys.toolsets: toolsets,
        }
        if not self.description:
            mapping.pop(ToolboxContentKeys.description)
        return mapping, toolset_names
    # End _build_content method

    def _build_resource(self, toolset_names: dict[str, str]) \
            -> dict[str, dict[str, str]]:
        """
        Build Resource
        """
        data = {ToolboxContentResourceKeys.title: self.label}
        if self.description:
            data[ToolboxContentResourceKeys.description] = self.description
        return {ToolboxContentResourceKeys.map: {**data, **toolset_names}}
    # End _build_resource method

    def _build_toolsets(self, source: Path, target: Path) \
            -> tuple[TOOLS_MAP, dict[str, str]]:
        """
        Build Toolsets (and tools)
        """
        nada = {ToolboxContentKeys.root: {ToolboxContentKeys.tools: ['']}}
        has_toolset_tools = any(t.has_tools for t in self.toolsets)
        if not self.tools and not has_toolset_tools:
            return nada, {}
        root_mapping = self._build_root_tools(source=source, target=target)
        if not has_toolset_tools:
            return root_mapping or nada, {}
        toolset_tools, toolset_names = self._build_toolset_tools(
            source=source, target=target)
        return {**root_mapping, **toolset_tools} or nada, toolset_names
    # End _build_toolsets method

    def _build_root_tools(self, source: Path, target: Path) -> TOOLS_MAP:
        """
        Build Root Tools
        """
        if not self.tools:
            return {}
        tools = self._make_tools_list(
            source=source, target=target, tools=self.tools)
        return {ToolboxContentKeys.root: {ToolboxContentKeys.tools: tools}}
    # End _build_root_tools method

    @staticmethod
    def _make_tools_list(source: Path, target: Path,
                         tools: list['ScriptTool']) -> list[str]:
        """
        Make Tools List
        """
        names = []
        for tool in sorted(tools, key=attrgetter(NAME)):
            tool.serialize(source=source, target=target)
            names.append(tool.qualified_name)
        return names
    # End _make_tools_list method

    def _build_toolset_tools(self, source: Path, target: Path) \
            -> tuple[TOOLS_MAP, dict[str, str]]:
        """
        Build Toolset Tools and Toolset Mapping
        """
        counter = 0
        toolset_tools = {}
        toolset_names = {}
        for toolset in self.toolsets:
            if not (tools := self._make_tools_list(
                    source=source, target=target, tools=toolset.tools)):
                continue
            counter += 1
            indexed_name = f'{TOOLSET}{counter}{DOT}{NAME}'
            toolset_tools[f'{DOLLAR_RC}{indexed_name}'] = {
                ToolboxContentKeys.tools: tools}
            toolset_names[indexed_name] = toolset.qualified_name
        return toolset_tools, toolset_names
    # End _build_toolset_tools method

    @property
    def name(self) -> str:
        """
        Name
        """
        return self._name
    # End name property

    @property
    def label(self) -> str:
        """
        Label
        """
        return self._label
    # End label property

    @property
    def alias(self) -> str:
        """
        Alias
        """
        return self._alias
    # End alias property

    @property
    def description(self) -> STRING:
        """
        Description
        """
        return self._description
    # End description property

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

    def add_script_tool(self, tool: 'ScriptTool') -> None:
        """
        Add Script Tool
        """
        self.tools.append(tool)
    # End add_script_tool method

    def add_toolset(self, toolset: 'Toolset') -> None:
        """
        Add Toolset
        """
        self.toolsets.append(toolset)
    # End add_toolset method

    def save(self, folder: Path, overwrite: bool = False) -> PATH:
        """
        Save toolbox into specified folder.
        """
        if not folder.is_dir():
            return
        toolbox = self._get_toolbox_path(folder=folder, overwrite=overwrite)
        temporary = make_temp_folder()
        self._serialize(source=temporary, target=folder)
        self._save_toolbox(source=temporary, target=toolbox)
        return toolbox
    # End save method
# End Toolbox class


if __name__ == '__main__':  # pragma: no cover
    pass
