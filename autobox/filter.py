# -*- coding: utf-8 -*-
"""
Enumerations
"""


from abc import abstractmethod
from enum import StrEnum
from math import isfinite
from numbers import Real
from typing import ClassVar, Type


from autobox.constant import (
    DOLLAR_RC, DOT, DomainContentKeys, GP_AREAL_UNIT, GP_CODED_VALUE_DOMAIN,
    GP_DOUBLE, GP_FEATURE_CLASS_DOMAIN, GP_FIELD_DOMAIN, GP_FILE_DOMAIN,
    GP_LINEAR_UNIT, GP_LONG, GP_RANGE_DOMAIN, GP_WORKSPACE_DOMAIN,
    ItemsContentKeys, ParameterContentKeys)
from autobox.enum import (
    ArealUnit, FieldType, GeometryType, LinearUnit, WorkspaceType)
from autobox.type import (
    MAP_DICT_STR_LIST, MAP_STR, MAP_STR_LIST, STRING, STRINGS)
from autobox.util import unique


__all__ = ['ArealUnitFilter', 'FeatureClassTypeFilter', 'FieldTypeFilter',
           'FileTypeFilter', 'LinearUnitFilter', 'WorkspaceTypeFilter']


class AbstractFilter:
    """
    Abstract Filter
    """
    def __init__(self, values: list | tuple) -> None:
        """
        Initialize the AbstractEnumerationFilter class
        """
        super().__init__()
        self._values: list = self._validate_values(values)
    # End init built-in

    @abstractmethod
    def _validate_values(self, values: list | tuple) -> list:  # pragma: no cover
        """
        Validate Values
        """
        pass
    # End _validate_values method

    @abstractmethod
    def _serialize(self, name: STRING = None) -> dict:  # pragma: no cover
        """
        Serialize
        """
        pass
    # End _serialize method

    @property
    def values(self) -> list:
        """
        Values
        """
        return self._values
    # End values property

    def serialize(self, name: STRING = None) -> dict:
        """
        Serialize the Filter
        """
        return self._serialize(name)
    # End serialize method
# End AbstractFilter class


class AbstractEnumerationFilter(AbstractFilter):
    """
    Abstract Enumeration Filter
    """
    keyword: ClassVar[str] = ''
    enumeration: ClassVar[Type[StrEnum]] = StrEnum

    def _validate_values(self, values: list[StrEnum] | tuple[StrEnum, ...]) \
            -> list[StrEnum]:
        """
        Validate Values
        """
        if not isinstance(values, (list, tuple)):
            values = values,
        values = [v for v in values if isinstance(v, self.enumeration)]
        return unique([v for v in values if v in self.enumeration])
    # End _validate_values method

    @abstractmethod
    def _serialize(self, name: STRING = None) -> dict:  # pragma: no cover
        """
        Serialize
        """
        pass
    # End _serialize method
# End AbstractEnumerationFilter class


class BaseCodedDomainFilter(AbstractEnumerationFilter):
    """
    Base Enumeration Filter
    """
    def _serialize(self, name: STRING = None) -> dict[str, MAP_STR_LIST]:
        """
        Serialize
        """
        if not self.values:
            return {}
        items = []
        for value in self.values:
            items.append({ItemsContentKeys.type: self.keyword,
                          ItemsContentKeys.value: value.value,
                          ItemsContentKeys.code: value.value})
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: GP_CODED_VALUE_DOMAIN,
            DomainContentKeys.items: items}}
    # End _serialize method
# End BaseCodedDomainFilter class


class BaseTypeListFilter(AbstractEnumerationFilter):
    """
    Base Type List Filter
    """
    items_keyword: ClassVar[str] = ''

    def _serialize(self, name: STRING = None) -> MAP_STR_LIST:
        """
        Serialize
        """
        if not self.values:
            return {}
        items = [v.value for v in self.values]
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: self.keyword,
            self.items_keyword: items}}
    # End _serialize method
# End BaseTypeListFilter class


class ArealUnitFilter(BaseCodedDomainFilter):
    """
    Areal Unit Filter
    """
    keyword: ClassVar[str] = GP_AREAL_UNIT
    enumeration: ClassVar[Type[ArealUnit]] = ArealUnit
# End ArealUnitFilter class


class FeatureClassTypeFilter(BaseTypeListFilter):
    """
    Feature Class Type Filter
    """
    keyword: ClassVar[str] = GP_FEATURE_CLASS_DOMAIN
    enumeration: ClassVar[Type[GeometryType]] = GeometryType

    def _serialize(self, name: STRING = None) -> dict[str, list[MAP_STR]]:
        """
        Serialize
        """
        if not self.values:
            return {}
        data = {DomainContentKeys.type: self.keyword}
        types = GeometryType.ANNOTATION, GeometryType.DIMENSION
        if geometry := [v.value for v in self.values if v not in types]:
            data[DomainContentKeys.geometry_type] = geometry
        if features := [v.value for v in self.values if v in types]:
            data[DomainContentKeys.feature_type] = features
        return {ParameterContentKeys.domain: data}
    # End _serialize method
# End FeatureClassTypeFilter class


class FieldTypeFilter(BaseTypeListFilter):
    """
    Field Type Filter
    """
    keyword: ClassVar[str] = GP_FIELD_DOMAIN
    items_keyword: ClassVar[str] = DomainContentKeys.field_type
    enumeration: ClassVar[Type[FieldType]] = FieldType
# End FieldTypeFilter class


class FileTypeFilter(AbstractEnumerationFilter):
    """
    File Type Filter
    """
    def _validate_values(self, values: STRINGS) -> list[str]:
        """
        Validate Values
        """
        if not isinstance(values, (list, tuple)):
            values = values,
        values = [v.strip() for v in values if isinstance(v, str)]
        values = [v.lstrip(DOT) for v in values]
        return unique([v for v in values if v])
    # End _validate_values method

    def _serialize(self, name: STRING = None) -> MAP_DICT_STR_LIST:
        """
        Serialize
        """
        if not self.values:
            return {}
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: GP_FILE_DOMAIN,
            DomainContentKeys.file_types: list(self.values)}}
    # End _serialize method
# End FileTypeFilter class


class LinearUnitFilter(BaseCodedDomainFilter):
    """
    Linear Unit Filter
    """
    keyword: ClassVar[str] = GP_LINEAR_UNIT
    enumeration: ClassVar[Type[LinearUnit]] = LinearUnit
# End LinearUnitFilter class


class WorkspaceTypeFilter(BaseTypeListFilter):
    """
    Workspace Type Filter
    """
    keyword: ClassVar[str] = GP_WORKSPACE_DOMAIN
    items_keyword: ClassVar[str] = DomainContentKeys.workspace_type
    enumeration: ClassVar[Type[WorkspaceType]] = WorkspaceType
# End WorkspaceTypeFilter class


class AbstractRangeFilter(AbstractFilter):
    """
    Abstract Range Filter
    """
    def __init__(self, minimum: Real, maximum: Real) -> None:
        """
        Initialize the AbstractRangeFilter class
        """
        super().__init__((minimum, maximum))
    # End init built-in

    @abstractmethod
    def _validate_values(self, values: tuple) -> list:  # pragma: no cover
        """
        Validate Values
        """
        pass
    # End _validate_values method

    @staticmethod
    def _validate_and_convert(values: tuple, type_: Type[float | int]) -> list:
        """
        Validate minimum and maximum and convert to float or int.
        """
        if not isinstance(values, tuple):
            return []
        values = {v for v in values if isinstance(v, Real)}
        if len(values) < 2:
            return []
        try:
            values = {type_(v) for v in values if isfinite(v)}
        except (TypeError, ValueError):  # pragma: no cover
            return []
        if len(values) < 2:
            return []
        return [min(values), max(values)]
    # End _validate_and_convert method

    def _serialize(self, name: STRING = None) -> dict[str, MAP_STR]:
        """
        Serialize
        """
        if not self.values:
            return {}
        minimum, maximum = self.values
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: GP_RANGE_DOMAIN,
            DomainContentKeys.minimum: repr(minimum),
            DomainContentKeys.maximum: repr(maximum)}}
    # End _serialize method
# End AbstractRangeFilter class


class LongRangeFilter(AbstractRangeFilter):
    """
    Long Range Filter
    """
    def _validate_values(self, values: tuple[int, int]) -> list[int]:
        """
        Validate Values
        """
        return self._validate_and_convert(values, type_=int)
    # End _validate_values method
# End LongRangeFilter class


class DoubleRangeFilter(AbstractRangeFilter):
    """
    Double Range Filter
    """
    def _validate_values(self, values: tuple[float, float]) -> list[float]:
        """
        Validate Values
        """
        return self._validate_and_convert(values, type_=float)
    # End _validate_values method
# End DoubleRangeFilter class


class AbstractNumberValueFilter(AbstractFilter):
    """
    Abstract Number Value Filter
    """
    keyword: ClassVar[str] = ''

    @abstractmethod
    def _validate_values(self, values: list | tuple) -> list:  # pragma: no cover
        """
        Validate Values
        """
        pass
    # End _validate_values method

    @staticmethod
    def _validate_and_convert(values: list | tuple,
                              type_: Type[float | int]) -> list:
        """
        Validate values and convert to float or int.
        """
        if not isinstance(values, (list, tuple)):
            return []
        if not (values := unique([v for v in values if isinstance(v, Real)])):
            return []
        try:
            return unique([type_(v) for v in values if isfinite(v)])
        except (TypeError, ValueError):  # pragma: no cover
            return []
    # End _validate_and_convert method

    def _serialize(self, name: STRING = None) -> MAP_STR_LIST:
        """
        Serialize
        """
        if not self.values:
            return {}
        items = []
        for value in self.values:
            items.append({ItemsContentKeys.type: self.keyword,
                          ItemsContentKeys.value: repr(value),
                          ItemsContentKeys.code: repr(value)})
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: GP_CODED_VALUE_DOMAIN,
            DomainContentKeys.items: items}}
    # End _serialize method
# End AbstractNumberValueFilter class


class LongValueFilter(AbstractNumberValueFilter):
    """
    Long Value Filter
    """
    keyword: ClassVar[str] = GP_LONG

    def _validate_values(self, values: list[int] | tuple[int, ...]) -> list[int]:
        """
        Validate Values
        """
        return self._validate_and_convert(values, type_=int)
    # End _validate_values method
# End LongValueFilter class


class DoubleValueFilter(AbstractNumberValueFilter):
    """
    Double Value Filter
    """
    keyword: ClassVar[str] = GP_DOUBLE

    def _validate_values(self, values: list[float] | tuple[float, ...]) -> list[float]:
        """
        Validate Values
        """
        return self._validate_and_convert(values, type_=float)
    # End _validate_values method
# End DoubleValueFilter class


class StringValueFilter(AbstractFilter):
    """
    String Value Filter
    """
    def _validate_values(self, values: STRINGS) -> list[str]:
        """
        Validate Values
        """
        if not isinstance(values, (list, tuple)):
            values = values,
        return unique([v for v in values if isinstance(v, str)])
    # End _validate_values method

    def _serialize(self, name: STRING = None) -> tuple[MAP_STR_LIST, MAP_STR]:
        """
        Serialize content and resources
        """
        if not isinstance(name, str) or not self.values:
            return {}, {}
        items = []
        resources = {}
        name_domain = f'{name.casefold()}{DOT}{ParameterContentKeys.domain}'
        for value in self.values:
            code = f'{name_domain}{DOT}{value}'
            items.append({ItemsContentKeys.value: value,
                          ItemsContentKeys.code: f'{DOLLAR_RC}{code}'})
            resources[code] = value
        return {ParameterContentKeys.domain: {
            DomainContentKeys.type: GP_CODED_VALUE_DOMAIN,
            DomainContentKeys.items: items}}, resources
    # End _serialize method

    def serialize(self, name: STRING = None) -> tuple[MAP_STR_LIST, MAP_STR]:
        """
        Serialize the Filter
        """
        return self._serialize(name)
    # End serialize method
# End StringValueFilter class


if __name__ == '__main__':  # pragma: no cover
    pass
