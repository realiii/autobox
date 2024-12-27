# -*- coding: utf-8 -*-
"""
Script Tool
"""


from abc import abstractmethod
from datetime import datetime
from json import dump
from operator import itemgetter
from pathlib import Path
from shutil import copyfile
from typing import NoReturn, Self

from autobox.constant import (
    COLON, DEPENDENCY, DOT, ENCODING, ICON, ILLUSTRATION, ParameterContentKeys,
    SCRIPT, SCRIPT_STUB, SEMI_COLON, SPACE, ScriptToolContentKeys,
    ScriptToolContentResourceKeys, TOOL, TOOL_CONTENT, TOOL_CONTENT_RC,
    TOOL_ICON, TOOL_ILLUSTRATION, TOOL_SCRIPT_EXECUTE_LINK,
    TOOL_SCRIPT_EXECUTE_PY, TOOL_SCRIPT_VALIDATE_PY, ToolAttributeKeywords)
from autobox.type import MAP_STR, PARAMETER, PATH, STRING, ToolAttributes
from autobox.util import (
    get_repeated_names, validate_path, validate_script_folder_name,
    validate_script_name, wrap_markup)


class AbstractScript:
    """
    Abstract Script
    """
    def __init__(self, code: STRING = None, path: PATH = None,
                 embed: bool = False) -> None:
        """
        Initialize the AbstractScript class
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
        with exec_path.open(mode='w', encoding=ENCODING) as fout:
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
            return self._path.read_text(encoding=ENCODING)
        try:
            path = self._path.relative_to(target.resolve())
        except ValueError:
            return str(self._path)
        return f'..\\..\\{path}'
    # End _get_content method

    @staticmethod
    def _validate_code(code: str) -> None | NoReturn:
        """
        Validate Code
        """
        if not code:
            raise ValueError('No code provided')
    # End _validate_code method

    @abstractmethod
    def _get_file_name(self) -> str:  # pragma: no cover
        """
        Get File Name
        """
        pass
    # End _serialize method

    def serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Execution Script to Disk
        """
        return self._serialize(source=source, target=target)
    # End serialize method
# End AbstractScript class


class ExecutionScript(AbstractScript):
    """
    Execution Script
    """
    def _get_file_name(self) -> str:
        """
        Get File Name
        """
        if self._embed:
            return TOOL_SCRIPT_EXECUTE_PY
        return TOOL_SCRIPT_EXECUTE_LINK
    # End _serialize method

    @classmethod
    def from_code(cls, code: str) -> Self:
        """
        From Code, a string containing python code.
        """
        cls._validate_code(code)
        return cls(code=code, embed=True)
    # End from_code method

    @classmethod
    def from_file(cls, path: Path, embed: bool) -> Self:
        """
        From File, a path to a file containing python code.
        """
        path = validate_path(path, text=SCRIPT)
        return cls(path=path, embed=embed)
    # End from_file method
# End ExecutionScript class


class ValidationScript(AbstractScript):
    """
    Validation Script
    """
    def __init__(self, code: STRING = None, path: PATH = None) -> None:
        """
        Use the class methods to create an instance of this class.
        """
        super().__init__(code=code, path=path, embed=True)
    # End init built-in

    def _get_file_name(self) -> str:
        """
        Get File Name
        """
        return TOOL_SCRIPT_VALIDATE_PY
    # End _serialize method

    @classmethod
    def from_code(cls, code: str) -> Self:
        """
        From Code, a string containing python code.
        """
        cls._validate_code(code)
        return cls(code=code)
    # End from_code method

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """
        From File, a path to a file containing python code.
        """
        path = validate_path(path, text=SCRIPT)
        return cls(path=path)
    # End from_file method
# End ValidationScript class


DEFAULT_EXECUTION_SCRIPT = ExecutionScript.from_code(SCRIPT_STUB)


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
        self._label: str = self._validate_label(label, name=self._name)
        self._description: STRING = description
        self._summary: STRING = summary
        self._attributes: ToolAttributes = attributes
        self._execution: ExecutionScript | None = None
        self._validation: ValidationScript | None = None
        self._icon: PATH = None
        self._illustration: PATH = None
        self._parameters: list[PARAMETER] = []
    # End init built-in

    def __repr__(self) -> str:
        """
        Class Representation
        """
        return (f'{self.__class__.__name__}(name={self.name!r}, '
                f'label={self.label!r}, description={self.description!r})')
    # End repr built-in

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

    @staticmethod
    def _validate_label(label: STRING, name: str) -> str:
        """
        Validate Label
        """
        if not isinstance(label, str):
            return name
        return label.strip() or name
    # End _validate_label method

    def _build_content(self) -> tuple[dict[str, str | dict[str, list]], MAP_STR]:
        """
        Build Content
        """
        parameter_content, parameter_resource = self._build_parameters()
        mapping = {
            ScriptToolContentKeys.type: 'ScriptTool',
            ScriptToolContentKeys.display_name: '$rc:title',
            ScriptToolContentKeys.application_version: '13.4',
            ScriptToolContentKeys.description: '$rc:description',
            ScriptToolContentKeys.attributes: [],
            ScriptToolContentKeys.product: '100',
            ScriptToolContentKeys.updated: (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ScriptToolContentKeys.parameters: parameter_content,
        }
        if not self.description:
            mapping.pop(ScriptToolContentKeys.description)
        if not any(self.attributes):
            mapping.pop(ScriptToolContentKeys.attributes)
        else:
            for a, k in zip(self.attributes, ToolAttributeKeywords.ordered):
                if a:
                    mapping[ScriptToolContentKeys.attributes].append(k)
        return mapping, parameter_resource
    # End _build_content method

    def _build_parameters(self) -> tuple[dict[str, dict] | str, MAP_STR]:
        """
        Build Parameters
        """
        if not self.parameters:
            return '', {}
        parameters = {}
        resources = {}
        self._check_parameter_repeats()
        categories = self._build_categories()
        for parameter in self.parameters:
            content, resource = parameter.serialize(categories)
            resources.update(resource)
            parameters[parameter.name] = content
        prefix = (f'{ScriptToolContentKeys.parameters}{DOT}'
                  f'{ParameterContentKeys.category}')
        for name, i in sorted(categories.items(), key=itemgetter(1)):
            resources[f'{prefix}{i}'] = name
        return parameters, resources
    # End _build_parameters method

    def _build_categories(self) -> dict[str, int]:
        """
        Build Categories
        """
        counter = 1
        categories = {}
        for parameter in self.parameters:
            if not (category := parameter.category):
                continue
            if category in categories:
                continue
            categories[category] = counter
            counter += 1
        return categories
    # End _build_categories method

    def _build_resource(self, parameters: MAP_STR) -> dict[str, MAP_STR]:
        """
        Build Resource
        """
        data = {ScriptToolContentResourceKeys.title: self.label}
        if self.description:
            data[ScriptToolContentResourceKeys.description] = self.description
        if self.summary:
            data[ScriptToolContentResourceKeys.summary] = self.summary
        data.update(parameters)
        return {ScriptToolContentResourceKeys.map: data}
    # End _build_resource method

    def _copy_images(self, source: Path) -> None:
        """
        Copy Images
        """
        for name, path in zip((TOOL_ICON, TOOL_ILLUSTRATION),
                              (self.icon, self.illustration)):
            if not path:
                continue
            copyfile(path, source.joinpath(f'{name}{path.suffix}'))
    # End _copy_images method

    def _check_parameter_repeats(self) -> None | NoReturn:
        """
        Check for Parameter name repetitions, must be unique on a tool
        regardless of case.
        """
        if not (names := get_repeated_names(self.parameters)):
            return
        names = {t.name for t in self.parameters if t.name.casefold() in names}
        names = f'{SEMI_COLON}{SPACE}'.join(sorted(names))
        raise ValueError(f'Parameter name repetition detected: {names}')
    # End _check_parameter_repeats method

    @staticmethod
    def _validate_image(path: PATH, text: str) -> PATH:
        """
        Validate Image Path
        """
        if not path:
            return
        path = validate_path(path, text=text)
        if path.suffix.casefold() not in ('.png', '.jpg'):
            raise TypeError(f'Invalid {text} file type: {path.suffix}')
        return path
    # End _validate_image method

    def _serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Files to Temporary Folder
        """
        content, parameter_resource = self._build_content()
        resource = self._build_resource(parameter_resource)
        script_path = source.joinpath(f'{self._folder}{DOT}{TOOL}')
        script_path.mkdir()
        for name, data in zip((TOOL_CONTENT, TOOL_CONTENT_RC),
                              (content, resource)):
            file_path = script_path.joinpath(name)
            with file_path.open(mode='w', encoding=ENCODING) as fout:
                # noinspection PyTypeChecker
                dump(data, fp=fout, indent=2)
        if not self.execution_script:
            self.execution_script = DEFAULT_EXECUTION_SCRIPT
        self.execution_script.serialize(source=script_path, target=target)
        if self.validation_script:
            self.validation_script.serialize(source=script_path, target=target)
        self._copy_images(script_path)
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
    def attributes(self) -> ToolAttributes:
        """
        Attributes
        """
        return self._attributes
    # End attributes property

    @property
    def execution_script(self) -> ExecutionScript | None:
        """
        Execution Script
        """
        return self._execution

    @execution_script.setter
    def execution_script(self, value: ExecutionScript | None) -> None:
        self._execution = value
    # End execution_script property

    @property
    def validation_script(self) -> ValidationScript | None:
        """
        Validation Script
        """
        return self._validation

    @validation_script.setter
    def validation_script(self, value: ValidationScript | None) -> None:
        self._validation = value
    # End validation_script property

    @property
    def icon(self) -> PATH:
        """
        Icon Path
        """
        return self._icon

    @icon.setter
    def icon(self, value: PATH) -> None:
        self._icon = self._validate_image(value, text=ICON)
    # End icon property

    @property
    def illustration(self) -> PATH:
        """
        Illustration
        """
        return self._illustration

    @illustration.setter
    def illustration(self, value: PATH) -> None:
        self._illustration = self._validate_image(value, text=ILLUSTRATION)
    # End illustration property

    @property
    def parameters(self) -> list[PARAMETER]:
        """
        Parameters
        """
        return self._parameters
    # End parameters property

    def add_parameter(self, parameter: PARAMETER) -> None:
        """
        Add Parameter
        """
        if not hasattr(parameter, DEPENDENCY):
            raise TypeError(f'Expected a parameter, got: {parameter}')
        self.parameters.append(parameter)
    # End add_parameter method

    def serialize(self, source: Path, target: Path) -> Path:
        """
        Serialize Script Tool to Disk
        """
        return self._serialize(source=source, target=target)
    # End serialize method
# End ScriptTool class


if __name__ == '__main__':  # pragma: no cover
    pass
