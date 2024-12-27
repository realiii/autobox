# -*- coding: utf-8 -*-
"""
Types and Aliases
"""


from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING, Type, TypeAlias, Union


if TYPE_CHECKING:  # pragma: no cover
    from autobox.enum import (
        ArealUnit, FieldType, GeometryType, LinearUnit, WorkspaceType)
    # noinspection PyProtectedMember
    from autobox.filter import AbstractFilter
    # noinspection PyProtectedMember
    from autobox.parameter import InputOutputParameter, InputParameter


PATH: TypeAlias = Path | None
BOOL: TypeAlias = bool | None
STRING: TypeAlias = str | None
STRINGS: TypeAlias = list[str] | tuple[str, ...]
MAP_STR: TypeAlias = dict[str, STRING]
MAP_STR_LIST: TypeAlias = dict[str, str | list[MAP_STR]]
MAP_DICT_STR_LIST: TypeAlias = dict[str, dict[str, str | list[str]]]
TOOLS_MAP: TypeAlias = dict[str, dict[str, list[str]]]
PARAMETER: TypeAlias = Union['InputOutputParameter', 'InputParameter']
TYPE_PARAMS: TypeAlias = tuple[Type['InputOutputParameter'], ...]
TYPE_FILTERS: TypeAlias = tuple[Type['AbstractFilter'], ...]
AREAL_UNITS: TypeAlias = list['ArealUnit'] | tuple['ArealUnit', ...]
FIELD_TYPES: TypeAlias = list['FieldType'] | tuple['FieldType', ...]
GEOMETRY_TYPES: TypeAlias = list['GeometryType'] | tuple['GeometryType', ...]
LINEAR_UNITS: TypeAlias = list['LinearUnit'] | tuple['LinearUnit', ...]
WORKSPACE_TYPES: TypeAlias = list['WorkspaceType'] | tuple['WorkspaceType', ...]


class ToolAttributes(NamedTuple):
    """
    Tool Attributes
    """
    show_modifies_input: bool = False
    do_not_add_to_map: bool = False
    show_enable_undo: bool = False
    show_consumes_credits: bool = False
# End ToolAttributes class


if __name__ == '__main__':  # pragma: no cover
    pass
