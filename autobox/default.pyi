# -*- coding: utf-8 -*-
"""
Classes for Default Value
"""


from enum import StrEnum
from typing import ClassVar, NoReturn, Self, Type

from autobox.enum import ArealUnit, LinearUnit, TimeUnit
from autobox.type import NUMBER, STRING


class BaseRangeDomain:
    """
    Base Range Domain
    """
    _min: NUMBER
    _max: NUMBER

    def __init__(self, minimum: NUMBER, maximum: NUMBER) -> None: ...
    def __eq__(self, other: Self) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
    def _validate_range(self, minimum: NUMBER, maximum: NUMBER) -> tuple[NUMBER, NUMBER]: ...
    @staticmethod
    def _validate_value(value: NUMBER, text: str) -> NUMBER | NoReturn: ...
    @property
    def maximum(self) -> NUMBER: ...
    @property
    def minimum(self) -> NUMBER: ...
    def as_tuple(self) -> tuple[NUMBER, NUMBER]: ...
# End BaseRangeDomain class


class BaseUnitValue:
    """
    Base Unit Value
    """
    unit_type: ClassVar[Type[StrEnum]]

    _value: NUMBER
    _unit: StrEnum

    def __init__(self, value: NUMBER, unit: StrEnum) -> None: ...
    @staticmethod
    def _validate_value(value: NUMBER) -> NUMBER | NoReturn: ...
    def _validate_unit(self, value: StrEnum) -> StrEnum | NoReturn: ...
    def as_tuple(self) -> tuple[int, StrEnum]: ...
# End BaseUnitValue class


class BaseBoundingBox:
    """
    Base Bounding Box
    """
    _x: XDomain
    _y: YDomain

    def __init__(self, x: XDomain, y: YDomain) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self): ...
    @staticmethod
    def _validate_domain(value, type_) -> BaseRangeDomain | NoReturn: ...
    def as_tuple(self) -> tuple[NUMBER, NUMBER, NUMBER, NUMBER]: ...
# End BaseBoundingBox class


class ArealUnitValue(BaseUnitValue):
    """
    Areal Unit Value
    """
    _unit: ArealUnit

    def __init__(self, value: NUMBER, unit: ArealUnit) -> None: ...
    @staticmethod
    def _validate_value(value: NUMBER) -> NUMBER | NoReturn: ...
    def _validate_unit(self, value: ArealUnit) -> ArealUnit | NoReturn: ...
    def as_tuple(self) -> tuple[int, ArealUnit]: ...
# End ArealUnitValue class


class Envelope(BaseBoundingBox):
    """
    Envelope
    """
# End Envelope class


class Extent(BaseBoundingBox):
    """
    Extent
    """
    _crs: STRING

    def __init__(self, x: XDomain, y: YDomain, crs: STRING = None) -> None: ...
    @staticmethod
    def _validate_coordinate_system(value: STRING) -> STRING | NoReturn: ...
# End Extent class


class CellSizeXY:
    """
    Cell Size XY
    """
    _x: NUMBER
    _y: NUMBER

    def __init__(self, x: NUMBER, y: NUMBER) -> None: ...
    def __eq__(self, other: Self) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def _validate_value(value: NUMBER, text: str) -> NUMBER | NoReturn: ...
    def as_tuple(self) -> tuple[NUMBER, NUMBER]: ...
# End CellSizeXY class


class LinearUnitValue(BaseUnitValue):
    """
    Linear Unit Value
    """
    _unit: LinearUnit

    def __init__(self, value: NUMBER, unit: LinearUnit) -> None: ...
    @staticmethod
    def _validate_value(value: NUMBER) -> NUMBER | NoReturn: ...
    def _validate_unit(self, value: LinearUnit) -> LinearUnit | NoReturn: ...
    def as_tuple(self) -> tuple[int, LinearUnit]: ...
# End LinearUnitValue class


class MDomain(BaseRangeDomain): ...


class Point:
    """
    Point
    """
    _x: NUMBER
    _y: NUMBER

    def __init__(self, x: NUMBER, y: NUMBER) -> None: ...
    def __eq__(self, other: Self) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def _validate_value(value: NUMBER, text: str) -> NUMBER | NoReturn: ...
    def as_tuple(self) -> tuple[NUMBER, NUMBER]: ...
# End Point class


class TimeUnitValue(BaseUnitValue):
    """
    Time Unit Value
    """
    _unit: TimeUnit

    def __init__(self, value: NUMBER, unit: TimeUnit) -> None: ...
    @staticmethod
    def _validate_value(value: NUMBER) -> NUMBER | NoReturn: ...
    def _validate_unit(self, value: TimeUnit) -> TimeUnit | NoReturn: ...
    def as_tuple(self) -> tuple[int, TimeUnit]: ...
# End TimeUnitValue class


class XDomain(BaseRangeDomain): ...
class YDomain(BaseRangeDomain): ...


class XYDomain(BaseBoundingBox):
    """
    XY Domain
    """
# End XYDomain class


class ZDomain(BaseRangeDomain): ...


if __name__ == '__main__':  # pragma: no cover
    pass
