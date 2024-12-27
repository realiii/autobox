# -*- coding: utf-8 -*-
"""
Filter Stubs
"""


from abc import abstractmethod
from enum import StrEnum
from numbers import Real
from typing import ClassVar, Type

from autobox.enum import (
    ArealUnit, FieldType, GeometryType, LinearUnit, WorkspaceType)
from autobox.type import (
    AREAL_UNITS, FIELD_TYPES, GEOMETRY_TYPES, LINEAR_UNITS, MAP_DICT_STR_LIST,
    MAP_STR, MAP_STR_LIST, STRING, STRINGS, WORKSPACE_TYPES)


class AbstractFilter:
    """
    Abstract Filter
    """
    _values: list

    def __init__(self, values: list | tuple) -> None: ...
    @abstractmethod
    def _validate_values(self, values: list | tuple) -> list: ...
    @abstractmethod
    def _serialize(self, name: STRING = None) -> dict: ...
    @property
    def values(self) -> list: ...
    def serialize(self, name: STRING = None) -> dict: ...
# End AbstractFilter class


class AbstractEnumerationFilter(AbstractFilter):
    """
    Abstract Enumeration Filter
    """
    keyword: ClassVar[str]
    enumeration: ClassVar[Type[StrEnum]]
    _values: list[StrEnum]

    def __init__(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> None: ...
    def _validate_values(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> list[StrEnum]: ...
    def _serialize(self, name: STRING = None) -> dict: ...
    @property
    def values(self) -> list[StrEnum]: ...
    def serialize(self, name: STRING = None) -> dict: ...
# End AbstractEnumerationFilter class


class BaseCodedDomainFilter(AbstractEnumerationFilter):
    """
    Base Enumeration Filter
    """
    keyword: ClassVar[str]
    enumeration: ClassVar[Type[StrEnum]]
    _values: list[StrEnum]

    def __init__(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> None: ...
    def _validate_values(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> list[StrEnum]: ...
    def _serialize(self, name: STRING = None) -> dict[str, list[MAP_STR]]: ...
    @property
    def values(self) -> list[StrEnum]: ...
    def serialize(self, name: STRING = None) -> dict[str, list[MAP_STR]]: ...
# End BaseCodedDomainFilter class


class BaseTypeListFilter(AbstractEnumerationFilter):
    """
    Base Type List Filter
    """
    keyword: ClassVar[str]
    items_keyword: ClassVar[str]
    enumeration: ClassVar[Type[StrEnum]]
    _values: list[StrEnum]

    def __init__(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> None: ...
    def _validate_values(self, values: list[StrEnum] | tuple[StrEnum, ...]) -> list[StrEnum]: ...
    def _serialize(self, name: STRING = None) -> dict[str, list[MAP_STR]]: ...
    @property
    def values(self) -> list[StrEnum]: ...
    def serialize(self, name: STRING = None) -> dict[str, list[MAP_STR]]: ...
# End BaseTypeListFilter class


class ArealUnitFilter(BaseCodedDomainFilter):
    """
    Areal Unit Filter
    """
    keyword: ClassVar[str]
    enumeration: ClassVar[Type[ArealUnit]]
    _values: list[ArealUnit]

    def __init__(self, values: AREAL_UNITS) -> None: ...
    def _validate_values(self, values: AREAL_UNITS) -> list[ArealUnit]: ...
    def _serialize(self, name: STRING = None) -> dict[str, MAP_STR_LIST]: ...
    @property
    def values(self) -> list[ArealUnit]: ...
    def serialize(self, name: STRING = None) -> dict[str, MAP_STR_LIST]: ...
# End ArealUnitFilter class


class FeatureClassTypeFilter(BaseTypeListFilter):
    """
    Feature Class Type Filter
    """
    keyword: ClassVar[str]
    items_keyword: ClassVar[str]
    enumeration: ClassVar[Type[GeometryType]]
    _values: list[FieldType]

    def __init__(self, values: GEOMETRY_TYPES) -> None: ...
    def _validate_values(self, values: GEOMETRY_TYPES) -> list[GeometryType]: ...
    def _serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
    @property
    def values(self) -> list[GeometryType]: ...
    def serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
# End FeatureClassTypeFilter class


class FieldTypeFilter(BaseTypeListFilter):
    """
    Field Type Filter
    """
    keyword: ClassVar[str]
    items_keyword: ClassVar[str]
    enumeration: ClassVar[Type[FieldType]]
    _values: list[FieldType]

    def __init__(self, values: FIELD_TYPES) -> None: ...
    def _validate_values(self, values: FIELD_TYPES) -> list[FieldType]: ...
    def _serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
    @property
    def values(self) -> list[FieldType]: ...
    def serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
# End FieldTypeFilter class


class FileTypeFilter(BaseTypeListFilter):
    """
    Field Type Filter
    """
    _values: list[str]

    def __init__(self, values: STRINGS) -> None: ...
    def _validate_values(self, values: STRINGS) -> list[str]: ...
    def _serialize(self, name: STRING = None) -> MAP_DICT_STR_LIST: ...
    @property
    def values(self) -> list[str]: ...
    def serialize(self, name: STRING = None) -> MAP_DICT_STR_LIST: ...
# End FileTypeFilter class


class LinearUnitFilter(BaseCodedDomainFilter):
    """
    Linear Unit Filter
    """
    keyword: ClassVar[str]
    enumeration: ClassVar[Type[LinearUnit]]
    _values: list[LinearUnit]

    def __init__(self, values: LINEAR_UNITS) -> None: ...
    def _validate_values(self, values: LINEAR_UNITS) -> list[LinearUnit]: ...
    def _serialize(self, name: STRING = None) -> dict[str, MAP_STR_LIST]: ...
    @property
    def values(self) -> list[LinearUnit]: ...
    def serialize(self, name: STRING = None) -> dict[str, MAP_STR_LIST]: ...
# End LinearUnitFilter class


class WorkspaceTypeFilter(BaseTypeListFilter):
    """
    Workspace Type Filter
    """
    keyword: ClassVar[str]
    items_keyword: ClassVar[str]
    enumeration: ClassVar[Type[WorkspaceType]]
    _values: list[WorkspaceType]

    def __init__(self, values: WORKSPACE_TYPES) -> None: ...
    def _validate_values(self, values: WORKSPACE_TYPES) -> list[WorkspaceType]: ...
    def _serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
    @property
    def values(self) -> list[WorkspaceType]: ...
    def serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
# End WorkspaceTypeFilter class


class AbstractRangeFilter(AbstractFilter):
    """
    Abstract Range Filter
    """
    def __init__(self, minimum: Real, maximum: Real) -> None: ...
    @abstractmethod
    def _validate_values(self, values: tuple) -> list: ...
    @staticmethod
    def _validate_and_convert(values: tuple, type_: Type[float | int]) -> list: ...
    def _serialize(self, name: STRING = None) -> dict[str, MAP_STR]: ...
# End AbstractRangeFilter class


class LongRangeFilter(AbstractRangeFilter):
    """
    Long Range Filter
    """
    def _validate_values(self, values: tuple[int, int]) -> list[int]: ...
# End LongRangeFilter class


class DoubleRangeFilter(AbstractRangeFilter):
    """
    Double Range Filter
    """
    def _validate_values(self, values: tuple[float, float]) -> list[float]: ...
# End DoubleRangeFilter class


class AbstractNumberValueFilter(AbstractFilter):
    """
    Abstract Number Value Filter
    """
    keyword: ClassVar[str]
    @abstractmethod
    def _validate_values(self, values: list | tuple) -> list: ...
    @staticmethod
    def _validate_and_convert(values: list | tuple, type_: Type[float | int]) -> list: ...
    def _serialize(self, name: STRING = None) -> MAP_STR_LIST: ...
# End AbstractNumberValueFilter class


class LongValueFilter(AbstractNumberValueFilter):
    """
    Long Value Filter
    """
    keyword: ClassVar[str]
    def _validate_values(self, values: list[int] | tuple[int, ...]) -> list[int]: ...
# End LongValueFilter class


class DoubleValueFilter(AbstractNumberValueFilter):
    """
    Double Value Filter
    """
    keyword: ClassVar[str]
    def _validate_values(self, values: list[float] | tuple[float, ...]) -> list[float]: ...
# End DoubleValueFilter class


class StringValueFilter(AbstractFilter):
    """
    String Value Filter
    """
    def _validate_values(self, values: STRINGS) -> list[str]: ...
    def _serialize(self, name: STRING = None) -> tuple[MAP_STR_LIST, MAP_STR]: ...
# End StringValueFilter class


if __name__ == '__main__':  # pragma: no cover
    pass
