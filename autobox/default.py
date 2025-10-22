# -*- coding: utf-8 -*-
"""
Classes for Default Value
"""


from abc import ABCMeta, abstractmethod
from enum import StrEnum
from typing import Any, ClassVar, NoReturn, Self, Type

from autobox.enum import ArealUnit, LinearUnit, TimeUnit
from autobox.type import NUMBER, STRING
from autobox.util import copier, enum_repr


__all__ = ['ArealUnitValue', 'CellSizeXY', 'Envelope', 'Extent',
           'LinearUnitValue', 'MDomain', 'Point', 'TimeUnitValue', 'XDomain',
           'XYDomain', 'YDomain', 'ZDomain']


class AbstractDefault(metaclass=ABCMeta):
    """
    Abstract Default
    """
    def __eq__(self, other: Self) -> bool:
        """
        Equality
        """
        if not isinstance(other, self.__class__):
            return False
        return self.as_tuple() == other.as_tuple()
    # End eq built-in

    def __hash__(self) -> int:
        """
        Hash
        """
        return hash(self.as_tuple())
    # End hash built-in

    @abstractmethod
    def as_tuple(self) -> tuple:  # pragma: no cover
        """
        As Tuple
        """
        pass
    # End as_tuple method
# End AbstractDefault class


class BaseRangeDomain(AbstractDefault):
    """
    Base Range Domain
    """
    def __init__(self, minimum: NUMBER, maximum: NUMBER) -> None:
        """
        Initialize the BaseRangeDomain class
        """
        super().__init__()
        minimum, maximum = self._validate_range(minimum, maximum)
        self._min: NUMBER = minimum
        self._max: NUMBER = maximum
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(minimum=self.minimum, maximum=self.maximum)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return (f'{self.__class__.__name__}('
                f'minimum={self.minimum!r}, maximum={self.maximum!r})')
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        return f'{self.minimum} {self.maximum}'
    # End str built-in

    def _validate_range(self, minimum: NUMBER, maximum: NUMBER) \
            -> tuple[NUMBER, NUMBER]:
        """
        Validate Range
        """
        minimum = self._validate_value(minimum, 'minimum')
        maximum = self._validate_value(maximum, 'maximum')
        minimum, maximum = min(minimum, maximum), max(minimum, maximum)
        if minimum == maximum:
            raise ValueError('minimum and maximum must be different')
        return minimum, maximum
    # End _validate_range method

    @staticmethod
    def _validate_value(value: NUMBER,
                        text: str) -> NUMBER | NoReturn:
        """
        Validate Value
        """
        if isinstance(value, (int, float)):
            return value
        raise TypeError(f'{text} must be a number')
    # End _validate_value method

    @property
    def minimum(self) -> NUMBER:
        """
        Minimum Value
        """
        return self._min
    # End minimum property

    @property
    def maximum(self) -> NUMBER:
        """
        Maximum Value
        """
        return self._max
    # End maximum property

    def as_tuple(self) -> tuple[NUMBER, NUMBER]:
        """
        As Tuple
        """
        return self.minimum, self.maximum
    # End as_tuple method
# End BaseRangeDomain class


class MDomain(BaseRangeDomain):
    """
    M Domain
    """
# End MDomain class


class XDomain(BaseRangeDomain):
    """
    X Domain
    """
# End XDomain class


class YDomain(BaseRangeDomain):
    """
    Y Domain
    """
# End YDomain class


class ZDomain(BaseRangeDomain):
    """
    Z Domain
    """
# End ZDomain class


class BaseUnitValue(AbstractDefault):
    """
    Base Unit Value
    """
    unit_type: ClassVar[Type[StrEnum]] = StrEnum

    def __init__(self, value: NUMBER, unit: StrEnum) -> None:
        """
        Initialize the BaseUnitValue class
        """
        super().__init__()
        self._value: NUMBER = self._validate_value(value)
        self._unit: StrEnum = self._validate_unit(unit)
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(value=self.value, unit=self.unit)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return (f'{self.__class__.__name__}('
                f'value={self.value!r}, unit={enum_repr(self.unit)})')
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        return f'{self.value} {self.unit}'
    # End str built-in

    @staticmethod
    def _validate_value(value: NUMBER) -> NUMBER | NoReturn:
        """
        Validate Value
        """
        if isinstance(value, (int, float)):
            return value
        raise TypeError('value must be a number')
    # End _validate_value method

    def _validate_unit(self, value: StrEnum) -> StrEnum | NoReturn:
        """
        Validate Unit
        """
        if isinstance(value, self.unit_type):
            return value
        raise TypeError(f'unit must be a {self.unit_type.__name__}')
    # End _validate_unit method

    @property
    def unit(self) -> StrEnum:
        """
        Unit
        """
        return self._unit
    # End unit property

    @property
    def value(self) -> NUMBER:
        """
        Value
        """
        return self._value
    # End value property

    def as_tuple(self) -> tuple[NUMBER, StrEnum]:
        """
        As Tuple
        """
        return self.value, self.unit
    # End as_tuple method
# End BaseUnitValue class


class ArealUnitValue(BaseUnitValue):
    """
    Areal Unit Value
    """
    unit_type: ClassVar[Type[ArealUnit]] = ArealUnit
# End ArealUnitValue class


class LinearUnitValue(BaseUnitValue):
    """
    Linear Unit Value
    """
    unit_type: ClassVar[Type[LinearUnit]] = LinearUnit
# End LinearUnitValue class


class TimeUnitValue(BaseUnitValue):
    """
    Time Unit Value
    """
    unit_type: ClassVar[Type[TimeUnit]] = TimeUnit
# End TimeUnitValue class


class BaseBoundingBox(AbstractDefault):
    """
    Base Bounding Box
    """
    def __init__(self, x: XDomain, y: YDomain) -> None:
        """
        Initialize the Envelope class
        """
        super().__init__()
        self._x: XDomain = self._validate_domain(x, XDomain)
        self._y: YDomain = self._validate_domain(y, YDomain)
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(x=self.x_domain, y=self.y_domain)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return (f'{self.__class__.__name__}('
                f'x={self.x_domain!r}, y={self.y_domain!r})')
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        return (f'{self.x_domain.minimum} {self.y_domain.minimum} '
                f'{self.x_domain.maximum} {self.y_domain.maximum}')
    # End str built-in

    @staticmethod
    def _validate_domain(value, type_) -> BaseRangeDomain | NoReturn:
        """
        Validate Domain
        """
        if isinstance(value, type_):
            return value
        raise TypeError(f'Expected a {type_.__name__}, got: {value}')
    # End _validate_domain method

    @property
    def x_domain(self) -> XDomain:
        """
        X Domain
        """
        return self._x
    # End x_domain property

    @property
    def y_domain(self) -> YDomain:
        """
        Y Domain
        """
        return self._y
    # End y_domain property

    def as_tuple(self) -> tuple[NUMBER, NUMBER, NUMBER, NUMBER]:
        """
        As Tuple
        """
        return (self.x_domain.minimum, self.y_domain.minimum,
                self.x_domain.maximum, self.y_domain.maximum)
    # End as_tuple method
# End BaseBoundingBox class


class Envelope(BaseBoundingBox):
    """
    Envelope
    """
# End Envelope class


class Extent(BaseBoundingBox):
    """
    Extent
    """
    def __init__(self, x: XDomain, y: YDomain, crs: STRING = None) -> None:
        """
        Initialize the Extent class
        """
        super().__init__(x=x, y=y)
        self._crs: STRING = self._validate_coordinate_system(crs)
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(x=self.x_domain, y=self.y_domain, crs=self.crs)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        values = super().__repr__()
        if self._crs:
            return f'{values[:-1]}, crs={self.crs!r})'
        return values
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        values = super().__str__()
        if self.crs:
            return f'{values} {self.crs}'
        return values
    # End str built-in

    @staticmethod
    def _validate_coordinate_system(value: STRING) -> STRING | NoReturn:
        """
        Validate Coordinate System
        """
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError('coordinate system must be a string or None')
        return value.strip() or None
    # End _validate_coordinate_system method

    @property
    def coordinate_reference_system(self) -> STRING:
        """
        Coordinate Reference System
        """
        return self._crs
    # End coordinate_reference_system property
    crs = coordinate_reference_system

    def as_tuple(self) -> tuple[NUMBER, NUMBER, NUMBER, NUMBER, STRING]:
        """
        As Tuple
        """
        return *super().as_tuple(), self.crs
    # End as_tuple method
# End Extent class


class XYDomain(BaseBoundingBox):
    """
    XY Domain
    """
# End XYDomain class


class CellSizeXY(AbstractDefault):
    """
    Cell Size XY
    """
    def __init__(self, x: NUMBER, y: NUMBER) -> None:
        """
        Initialize the CellSizeXY class
        """
        super().__init__()
        self._x: NUMBER = self._validate_value(x, 'x')
        self._y: NUMBER = self._validate_value(y, 'y')
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(x=self.x_size, y=self.y_size)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return (f'{self.__class__.__name__}('
                f'x={self.x_size!r}, y={self.y_size!r})')
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        return f'{self.x_size} {self.y_size}'
    # End str built-in

    @staticmethod
    def _validate_value(value: NUMBER, text: str) -> NUMBER | NoReturn:
        """
        Validate Value
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f'{text} must be a number')
        if isinstance(value, (int, float)) and value > 0:
            return value
        raise ValueError(f'{text} must be a greater than 0')
    # End _validate_value method

    @property
    def x_size(self) -> NUMBER:
        """
        X Cell Size
        """
        return self._x
    # End x_size property

    @property
    def y_size(self) -> NUMBER:
        """
        Y Cell Size
        """
        return self._y
    # End y_size property

    def as_tuple(self) -> tuple[NUMBER, NUMBER]:
        """
        As Tuple
        """
        return self.x_size, self.y_size
    # End as_tuple method
# End CellSizeXY class


class Point(AbstractDefault):
    """
    Point
    """
    def __init__(self, x: NUMBER, y: NUMBER) -> None:
        """
        Initialize the Point class
        """
        super().__init__()
        self._x: NUMBER = self._validate_value(x, 'x')
        self._y: NUMBER = self._validate_value(y, 'y')
    # End init built-in

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Deep Copy
        """
        kwargs = dict(x=self.x, y=self.y)
        return copier(instance=self, memo=memo, kwargs=kwargs)
    # End deepcopy built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return f'{self.__class__.__name__}(x={self.x!r}, y={self.y!r})'
    # End repr built-in

    def __str__(self) -> str:
        """
        String
        """
        return f'{self.x} {self.y}'
    # End str built-in

    @staticmethod
    def _validate_value(value: NUMBER, text: str) -> NUMBER | NoReturn:
        """
        Validate Value
        """
        if isinstance(value, (int, float)):
            return value
        raise TypeError(f'{text} must be a number')
    # End _validate_value method

    @property
    def x(self) -> NUMBER:
        """
        X Coordinate
        """
        return self._x
    # End x property

    @property
    def y(self) -> NUMBER:
        """
        Y Size
        """
        return self._y
    # End y property

    def as_tuple(self) -> tuple[NUMBER, NUMBER]:
        """
        As Tuple
        """
        return self.x, self.y
    # End as_tuple method
# End Point class


if __name__ == '__main__':  # pragma: no cover
    pass
