# -*- coding: utf-8 -*-
"""
Script Tool
"""


from datetime import datetime
from json import dump
from pathlib import Path
from typing import NoReturn

from stoolbox.constants import (
    DOT, SCRIPT_STUB, ScriptToolContentKeys,
    ScriptToolContentResourceKeys, TOOL, TOOL_CONTENT, TOOL_CONTENT_RC,
    TOOL_SCRIPT, ToolAttributeKeywords)
from stoolbox.types import STRING, ToolAttributes
from stoolbox.util import (
    validate_script_folder_name, validate_script_name, wrap_markup)


class ScriptTool:
    """
    Script Tool
    """
    def __init__(self, name: str, label: STRING = None,
                 description: STRING = None, summary: STRING = None,
                 attributes: ToolAttributes = ToolAttributes()) -> None:
        """
        Initialize the ScriptTool class
        """
        super().__init__()
        self._name: str = self._validate_name(name)
        self._folder: str = self._validate_folder_name(self._name)
        self._label: STRING = self._validate_label(label)
        self._description: STRING = description
        self._summary: STRING = summary
        self._attributes: ToolAttributes = attributes
    # End init built-in

    @staticmethod
    def _validate_name(name: str) -> str | NoReturn:
        """
        Validate Name
        """
        if not (validated_name := validate_script_name(name)):
            raise ValueError(f'Invalid script name: {name}')
        return validated_name
    # End _validate_name method

    @staticmethod
    def _validate_folder_name(value: str) -> str:
        """
        Validate Folder Name
        """
        return validate_script_folder_name(value)
    # End _validate_folder_name method

    def _validate_label(self, label: STRING) -> str:
        """
        Validate Label
        """
        if not isinstance(label, str):
            return self.name
        return label.strip() or self.name
    # End _validate_label method

    def _build_content(self) -> dict[str, str | dict[str, list]]:
        """
        Build Content
        """
        mapping = {
            ScriptToolContentKeys.type: 'ScriptTool',
            ScriptToolContentKeys.display_name: '$rc:title',
            ScriptToolContentKeys.application_version: '13.4',
            ScriptToolContentKeys.description: '$rc:description',
            ScriptToolContentKeys.attributes: [],
            ScriptToolContentKeys.product: '100',
            ScriptToolContentKeys.updated: (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ScriptToolContentKeys.parameters: '',
        }

        if not self.description:
            mapping.pop(ScriptToolContentKeys.description)
        if not any(self._attributes):
            mapping.pop(ScriptToolContentKeys.attributes)
        else:
            for a, k in zip(self._attributes, ToolAttributeKeywords.ordered):
                if a:
                    mapping[ScriptToolContentKeys.attributes].append(k)
        return mapping
    # End _build_content method

    def _build_resource(self) -> dict[str, dict[str, str]]:
        """
        Build Resource
        """
        data = {ScriptToolContentResourceKeys.title: self.label}
        if self.description:
            data[ScriptToolContentResourceKeys.description] = self.description
        if self.summary:
            data[ScriptToolContentResourceKeys.summary] = self.summary
        return {ScriptToolContentResourceKeys.map: data}
    # End _build_resource method

    def _serialize(self, path: Path) -> Path:
        """
        Serialize Files to Temporary Folder
        """
        content = self._build_content()
        resource = self._build_resource()
        script_path = path.joinpath(f'{self._folder}{DOT}{TOOL}')
        script_path.mkdir()
        for name, data in zip((TOOL_CONTENT, TOOL_CONTENT_RC),
                              (content, resource)):
            file_path = script_path.joinpath(name)
            with file_path.open(
                    mode='w', encoding='utf-8') as fout:
                # noinspection PyTypeChecker
                dump(data, fp=fout, indent=2)
        with script_path.joinpath(TOOL_SCRIPT).open(
                mode='w', encoding='utf-8') as fout:
            fout.write(self.execution_script)
        return script_path
    # End _serialize method

    @property
    def name(self) -> str:
        """
        Name
        """
        return self._name
    # End name property

    @property
    def full_qualified_name(self) -> str:
        """
        Full Qualified Name
        """
        if self._folder == self.name:
            return self.name
        return f'{self.name}:{self._folder}{DOT}{TOOL}'
    # End full_qualified_name property

    @property
    def label(self) -> str:
        """
        Label
        """
        return self._label
    # End label property

    @property
    def description(self) -> STRING:
        """
        Description
        """
        return self._description
    # End description property

    @property
    def summary(self) -> STRING:
        """
        Summary
        """
        return wrap_markup(self._summary)
    # End summary property

    @property
    def execution_script(self) -> str:
        """
        Execution Script, path or content
        """
        return SCRIPT_STUB
    # End execution_script property

    def serialize(self, folder: Path) -> Path:
        """
        Serialize Script Tool to Disk
        """
        return self._serialize(folder)
    # End serialize method
# End ScriptTool class


if __name__ == '__main__':  # pragma: no cover
    pass
