# -*- coding: utf-8 -*-
"""
Script Tool
"""


from datetime import datetime
from json import dump
from pathlib import Path
from typing import NoReturn, Optional

from stoolbox.constants import (
    COLON, DOT, SCRIPT_STUB, ScriptToolContentKeys,
    ScriptToolContentResourceKeys, TOOL, TOOL_CONTENT, TOOL_CONTENT_RC,
    TOOL_SCRIPT_EXECUTE_LINK, TOOL_SCRIPT_EXECUTE_PY, ToolAttributeKeywords)
from stoolbox.types import PATH, STRING, ToolAttributes
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

        :param name: The name of the script tool, alphanumeric characters only,
            cannot start with a number.
        :param label: An optional label for the script tool.
        :param description: An optional description of the script tool,
            this should be plain text only.
        :param description: An optional summary of the script tool,
            this text can be plain text or html.
        :param attributes: An optional tuple of booleans which set special
            attributes on the script tool.
        """
        super().__init__()
        self._name: str = self._validate_name(name)
        self._folder: str = self._validate_folder_name(self._name)
        self._label: STRING = self._validate_label(label)
        self._description: STRING = description
        self._summary: STRING = summary
        self._attributes: ToolAttributes = attributes
        self._execution: Optional[ExecutionScript] = None
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

    def _serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Files to Temporary Folder
        """
        content = self._build_content()
        resource = self._build_resource()
        script_path = source.joinpath(f'{self._folder}{DOT}{TOOL}')
        script_path.mkdir()
        for name, data in zip((TOOL_CONTENT, TOOL_CONTENT_RC),
                              (content, resource)):
            file_path = script_path.joinpath(name)
            with file_path.open(mode='w', encoding='utf-8') as fout:
                # noinspection PyTypeChecker
                dump(data, fp=fout, indent=2)
        if not self.execution_script:
            self.execution_script = DEFAULT_EXECUTION_SCRIPT
        self.execution_script.serialize(source=script_path, target=target)
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
    def qualified_name(self) -> str:
        """
        Qualified Name
        """
        if self._folder == self.name:
            return self.name
        return f'{self.name}{COLON}{self._folder}{DOT}{TOOL}'
    # End qualified_name property

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
    def execution_script(self) -> Optional['ExecutionScript']:
        """
        Execution Script
        """
        return self._execution

    @execution_script.setter
    def execution_script(self, value: Optional['ExecutionScript']) -> None:
        self._execution = value
    # End execution_script property

    def serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Script Tool to Disk
        """
        return self._serialize(source=source, target=target)
    # End serialize method
# End ScriptTool class


class ExecutionScript:
    """
    Execution Script

    Includes methods for working with script execution files,
    including serialization and verifying folder paths.
    """
    def __init__(self, code: STRING = None, path: PATH = None,
                 embed: bool = False) -> None:
        """
        Initialize the ExecutionScript class
        """
        super().__init__()
        self._code: STRING = code
        self._path: PATH = path
        self._embed: bool = embed
    # End init built-in

    def _serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize File to Temporary Folder
        """
        name = self._get_file_name()
        content = self._get_content(target)
        exec_path = source.joinpath(name)
        with exec_path.open(mode='w', encoding='utf-8') as fout:
            fout.write(content)
        return exec_path
    # End _serialize method

    def _get_content(self, target: Path) -> str:
        """
        Get Content
        """
        if not self._path and not self._code:
            raise ValueError('No code or path provided')
        if self._code:
            return self._code
        if self._embed:
            return self._path.read_text(encoding='utf-8')
        try:
            path = self._path.relative_to(target.resolve())
        except ValueError:
            return str(self._path)
        return f'..\\..\\{path}'
    # End _get_content method

    def _get_file_name(self) -> str:
        """
        Get File Name
        """
        if self._embed:
            return TOOL_SCRIPT_EXECUTE_PY
        return TOOL_SCRIPT_EXECUTE_LINK
    # End _serialize method

    @classmethod
    def from_code(cls, code: str) -> 'ExecutionScript':
        """
        From Code, a string containing python code.
        """
        if not code:
            raise ValueError('No code provided')
        return cls(code=code, embed=True)
    # End from_code method

    @classmethod
    def from_file(cls, path: Path, embed: bool) -> 'ExecutionScript':
        """
        From File, a path to a file containing python code
        """
        try:
            path = Path(path)
        except TypeError:
            raise ValueError(f'Invalid path provided: {path}')
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {path}')
        return cls(path=path.resolve(), embed=embed)
    # End from_file method

    def serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Execution Script to Disk
        """
        return self._serialize(source=source, target=target)
    # End serialize method
# End ExecutionScript class


DEFAULT_EXECUTION_SCRIPT = ExecutionScript.from_code(SCRIPT_STUB)


if __name__ == '__main__':  # pragma: no cover
    pass
