# -*- coding: utf-8 -*-
"""
Types and Aliases
"""


from datetime import date, datetime, time
from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING, Type, TypeAlias, Union


if TYPE_CHECKING:  # pragma: no cover
    from autobox.enum import (
        ArealUnit, FieldType, GeometryType, LinearUnit, TimeUnit,
        TravelModeUnitType, WorkspaceType)
    # noinspection PyProtectedMember
    from autobox.filter import AbstractFilter
    # noinspection PyProtectedMember
    from autobox.parameter import InputOutputParameter, InputParameter


PATH: TypeAlias = Path | None
BOOL: TypeAlias = bool | None
DATETIME: TypeAlias = datetime | date | time
STRING: TypeAlias = str | None
STRINGS: TypeAlias = list[str] | tuple[str, ...]
NUMBER: TypeAlias = int | float
MAP_STR: TypeAlias = dict[str, STRING]
MAP_STR_LIST: TypeAlias = dict[str, str | list[MAP_STR]]
MAP_DICT_STR_LIST: TypeAlias = dict[str, dict[str, str | list[str]]]
TOOLS_MAP: TypeAlias = dict[str, dict[str, list[str]]]
PARAMETER: TypeAlias = Union['InputOutputParameter', 'InputParameter']
TYPES: TypeAlias = tuple[Type, ...]
TYPE_PARAMS: TypeAlias = tuple[Union[Type['InputOutputParameter'], Type['InputParameter']], ...]
TYPE_FILTERS: TypeAlias = tuple[Type['AbstractFilter'], ...]
AREAL_UNITS: TypeAlias = list['ArealUnit'] | tuple['ArealUnit', ...]
LINEAR_UNITS: TypeAlias = list['LinearUnit'] | tuple['LinearUnit', ...]
TIME_UNITS: TypeAlias = list['TimeUnit'] | tuple['TimeUnit', ...]
FIELD_TYPES: TypeAlias = list['FieldType'] | tuple['FieldType', ...]
GEOMETRY_TYPES: TypeAlias = list['GeometryType'] | tuple['GeometryType', ...]
TRAVEL_MODES: TypeAlias = list['TravelModeUnitType'] | tuple['TravelModeUnitType', ...]
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
