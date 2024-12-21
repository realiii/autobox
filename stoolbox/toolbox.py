# -*- coding: utf-8 -*-
"""
Toolbox
"""


from json import dump
from os import walk
from pathlib import Path
from shutil import rmtree
from typing import NoReturn, Optional, TYPE_CHECKING, Union
from zipfile import ZIP_DEFLATED, ZipFile

from stoolbox.constants import (
    DOLLAR_RC, EXT, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC, ToolboxContentKeys,
    ToolboxContentResourceKeys)
from stoolbox.types import STRING
from stoolbox.util import (
    make_temp_folder, validate_toolbox_alias, validate_toolbox_name)


if TYPE_CHECKING:  # pragma: no cover
    from stoolbox.script import ScriptTool


class Toolbox:
    """
    Toolbox
    """
    def __init__(self, name: str, label: STRING = None,
                 alias: STRING = None, description: STRING = None) -> None:
        """
        Initialize the Toolbox class

        :param name: The value of the toolbox file without the extension.
        :param label: An optional label for the toolbox.
        :param alias: An optional alias for the toolbox, must not contain
            spaces, underscores, special characters.  Must start with a letter.
        :param description: An optional description of the toolbox.
        """
        super().__init__()
        self._name: str = self._validate_name(name)
        self._label: STRING = self._validate_label(label)
        self._alias: STRING = self._validate_alias(alias)
        self._description: STRING = description
        self._tools: list[ScriptTool] = []
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

    def _serialize(self, path: Path) -> None:
        """
        Serialize Files to Temporary Folder
        """
        content = self._build_content(path)
        resource = self._build_resource()
        for name, data in zip((TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC),
                              (content, resource)):
            file_path = path.joinpath(name)
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

    def _build_content(self, path: Path) -> dict[str, str | dict[str, list]]:
        """
        Build Content
        """
        mapping = {
            ToolboxContentKeys.version: '1.0',
            ToolboxContentKeys.alias: self.alias,
            ToolboxContentKeys.display_name:
                f'{DOLLAR_RC}{ToolboxContentResourceKeys.title}',
            ToolboxContentKeys.description:
                f'{DOLLAR_RC}{ToolboxContentResourceKeys.description}',
            ToolboxContentKeys.toolsets: self._build_toolsets(path),
        }
        if not self.description:
            mapping.pop(ToolboxContentKeys.description)
        return mapping
    # End _build_content method

    def _build_resource(self) -> dict[str, dict[str, str]]:
        """
        Build Resource
        """
        data = {ToolboxContentResourceKeys.title: self.label}
        if self.description:
            data[ToolboxContentResourceKeys.description] = self.description
        return {ToolboxContentResourceKeys.map: data}
    # End _build_resource method

    def _build_toolsets(self, path: Path) -> dict[str, dict[str, list[str]]]:
        """
        Build Toolsets
        """
        keys = ToolboxContentKeys
        tools = []
        if not self._tools:
            tools.append('')
        else:
            for tool in self._tools:
                tool.serialize(path)
                tools.append(tool.full_qualified_name)
        return {keys.root: {keys.tools: tools}}
    # End _build_toolsets method

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

    def add_script_tool(self, tool: 'ScriptTool') -> None:
        """
        Add Script Tool
        """
        self._tools.append(tool)
    # End add_script_tool method

    def save(self, folder: Path, overwrite: bool = False) -> Optional[Path]:
        """
        Save toolbox into specified folder.
        """
        if not folder.is_dir():
            return
        toolbox = self._get_toolbox_path(folder, overwrite)
        temporary = make_temp_folder()
        self._serialize(temporary)
        self._save_toolbox(source=temporary, target=toolbox)
        return toolbox
    # End save method
# End Toolbox class


if __name__ == '__main__':  # pragma: no cover
    pass
