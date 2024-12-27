# -*- coding: utf-8 -*-
"""
Toolbox
"""

from json import dump
from operator import attrgetter
from os import walk
from pathlib import Path
from shutil import rmtree
from typing import NoReturn, TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from autobox.constant import (
    DOLLAR_RC, DOT, ENCODING, EXT, ILLUSTRATION, NAME, PARENT, SEMI_COLON,
    SPACE, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC, TOOLSET, ToolboxContentKeys,
    ToolboxContentResourceKeys)
from autobox.type import MAP_STR, PATH, STRING, TOOLS_MAP
from autobox.util import (
    get_repeated_names, make_temp_folder, validate_toolbox_alias,
    validate_toolbox_name)


if TYPE_CHECKING:  # pragma: no cover
    from autobox.script import ScriptTool
    from autobox.toolset import Toolset


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
        self._label: str = self._validate_label(label, name=self._name)
        self._alias: str = self._validate_alias(alias, name=self._name)
        self._description: STRING = description
        self._toolsets: list['Toolset'] = []
        self._tools: list['ScriptTool'] = []
    # End init built-in

    def __repr__(self) -> str:
        """
        Class Representation
        """
        return (f'{self.__class__.__name__}(name={self.name!r}, '
                f'label={self.label!r}, alias={self.alias!r}, '
                f'description={self.description!r})')
    # End repr built-in

    @staticmethod
    def _validate_name(name: str) -> str | NoReturn:
        """
        Validate Name
        """
        if not (validated_name := validate_toolbox_name(name)):
            raise ValueError(f'Invalid toolbox name: {name}')
        return validated_name
    # End _validate_name method

    @staticmethod
    def _validate_alias(alias: STRING, name: str) -> str | NoReturn:
        """
        Validate Alias
        """
        if not (validated_alias := validate_toolbox_alias(alias)):
            if not (validated_alias := validate_toolbox_alias(name)):
                raise ValueError(f'Invalid toolbox alias: {alias}')
        return validated_alias
    # End _validate_alias method

    @staticmethod
    def _validate_label(label: STRING, name: str) -> str:
        """
        Validate Label
        """
        if not isinstance(label, str):
            return name
        return label.strip() or name
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
            with file_path.open(mode='w', encoding=ENCODING) as fout:
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

    def _get_toolbox_path(self, folder: Path, overwrite: bool) -> Path | NoReturn:
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
            dict[str, str | dict[str, list]], MAP_STR]:
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

    def _build_resource(self, toolset_names: MAP_STR) -> dict[str, MAP_STR]:
        """
        Build Resource
        """
        data = {ToolboxContentResourceKeys.title: self.label}
        if self.description:
            data[ToolboxContentResourceKeys.description] = self.description
        return {ToolboxContentResourceKeys.map: {**data, **toolset_names}}
    # End _build_resource method

    def _build_toolsets(self, source: Path, target: Path) \
            -> tuple[TOOLS_MAP, MAP_STR]:
        """
        Build Toolsets (and tools)
        """
        nada = {ToolboxContentKeys.root: {ToolboxContentKeys.tools: ['']}}
        has_toolset_tools = any(t.has_tools for t in self.toolsets)
        if not self.tools and not has_toolset_tools:
            return nada, {}
        self._check_tool_repeats()
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
            -> tuple[TOOLS_MAP, MAP_STR]:
        """
        Build Toolset Tools and Toolset Mapping
        """
        counter = 0
        toolset_tools = {}
        toolset_names = {}
        toolsets = list(self.toolsets)
        self._check_toolset_repeats(toolsets)
        while toolsets:
            toolset = toolsets.pop(0)
            self._check_toolset_repeats(toolset.toolsets)
            toolsets.extend(toolset.toolsets)
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

    @staticmethod
    def _check_toolset_repeats(toolsets: list['Toolset']) -> None | NoReturn:
        """
        Check for Toolset name repetitions, toolset names must be unique
        at same depth but not across the entire toolbox regardless of case.
        """
        if not (names := get_repeated_names(toolsets)):
            return
        paths = {t.qualified_name
                 for t in toolsets if t.name.casefold() in names}
        paths = f'{SEMI_COLON}{SPACE}'.join(sorted(paths))
        raise ValueError(f'Toolset name repetition detected: {paths}')
    # End _check_toolset_repeats method

    def _check_tool_repeats(self) -> None | NoReturn:
        """
        Check for Tool name repetitions, tool names must be unique across
        the toolbox regardless of case.
        """
        tools = list(self.tools)
        toolsets = list(self.toolsets)
        while toolsets:
            toolset = toolsets.pop(0)
            tools.extend(toolset.tools)
            toolsets.extend(toolset.toolsets)
        if not (names := get_repeated_names(tools)):
            return
        names = {t.name for t in tools if t.name.casefold() in names}
        names = f'{SEMI_COLON}{SPACE}'.join(sorted(names))
        raise ValueError(f'Tool name repetition detected: {names}')
    # End _check_tool_repeats method

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
