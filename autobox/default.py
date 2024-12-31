# -*- coding: utf-8 -*-
"""
Classes for Default Value
"""


from typing import NoReturn


class CellSizeXY:
    """
    Cell Size XY
    """
    def __init__(self, x: float | int, y: float | int) -> None:
        """
        Initialize the CellSizeXY class
        """
        super().__init__()
        self._x: float | int = self._validate_value(x, 'x')
        self._y: float | int = self._validate_value(y, 'y')
    # End init built-in

    def __repr__(self) -> str:
        """
        String Representation
        """
        return f'{self._x} {self._y}'
    # End repr built-in

    @staticmethod
    def _validate_value(value: float | int, text: str) -> float | int | NoReturn:
        """
        Validate Value
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f'{text} must be a number')
        if isinstance(value, (int, float)) and value > 0:
            return value
        raise ValueError(f'{text} must be a greater than 0')
    # End _validate_value method
# End CellSizeXY class


if __name__ == '__main__':  # pragma: no cover
    pass
