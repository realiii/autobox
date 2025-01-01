# -*- coding: utf-8 -*-
"""
Classes for Default Value
"""


from typing import NoReturn, Self, Type

from autobox.type import NUMBER


class BaseRangeDomain:
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

    def __repr__(self) -> str:
        """
        String Representation
        """
        return f'{self.minimum} {self.maximum}'
    # End repr built-in

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
    def maximum(self) -> NUMBER:
        """
        Maximum Value
        """
        return self._max
    # End maximum property

    @property
    def minimum(self) -> NUMBER:
        """
        Minimum Value
        """
        return self._min
    # End minimum property

    def as_tuple(self) -> tuple[NUMBER, NUMBER]:
        """
        As Tuple
        """
        return self.minimum, self.maximum
    # End as_tuple method
# End BaseRangeDomain class


class CellSizeXY:
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

    def __eq__(self, other: 'CellSizeXY') -> bool:
        """
        Equality
        """
        if not isinstance(other, CellSizeXY):
            return False
        return self.as_tuple() == other.as_tuple()
    # End eq built-in

    def __hash__(self) -> int:
        """
        Hash
        """
        return hash(self.as_tuple())
    # End hash built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return f'{self._x} {self._y}'
    # End repr built-in

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

    def as_tuple(self) -> tuple[NUMBER, NUMBER]:
        """
        As Tuple
        """
        return self._x, self._y
    # End as_tuple method
# End CellSizeXY class


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


class XYDomain:
    """
    XY Domain
    """
    def __init__(self, x: XDomain, y: YDomain) -> None:
        """
        Initialize the XYDomain class
        """
        super().__init__()
        self._x: XDomain = self._validate_domain(x, XDomain)
        self._y: YDomain = self._validate_domain(y, YDomain)
    # End init built-in

    def __eq__(self, other: 'XYDomain') -> bool:
        """
        Equality
        """
        if not isinstance(other, XYDomain):
            return False
        return self.as_tuple() == other.as_tuple()
    # End eq built-in

    def __hash__(self) -> int:
        """
        Hash
        """
        return hash(self.as_tuple())
    # End hash built-in

    def __repr__(self):
        """
        String Representation
        """
        return (f'{self._x.minimum} {self._y.minimum} '
                f'{self._x.maximum} {self._y.maximum}')
    # End repr built-in

    @staticmethod
    def _validate_domain(value: XDomain | YDomain,
                         type_: Type[XDomain | YDomain]) \
            -> XDomain | YDomain | NoReturn:
        """
        Validate Domain
        """
        if isinstance(value, type_):
            return value
        raise TypeError(f'Expected a {type_.__name__}, got: {value}')
    # End _validate_domain method

    def as_tuple(self) -> tuple[NUMBER, NUMBER, NUMBER, NUMBER]:
        """
        As Tuple
        """
        return (self._x.minimum, self._y.minimum,
                self._x.maximum, self._y.maximum)
    # End as_tuple method
# End XYDomain class


class ZDomain(BaseRangeDomain):
    """
    Z Domain
    """
# End ZDomain class


if __name__ == '__main__':  # pragma: no cover
    pass
