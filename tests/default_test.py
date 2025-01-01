# -*- coding: utf-8 -*-
"""
Test Default Value Classes
"""


from pytest import mark, raises

from autobox.default import (
    ArealUnitValue, BaseRangeDomain, BaseUnitValue, CellSizeXY, LinearUnitValue,
    TimeUnitValue, XDomain, XYDomain, YDomain)
from autobox.enum import ArealUnit, LinearUnit, TimeUnit


@mark.parametrize('x, y, exception', [
    (None, None, TypeError),
    (-1, -2, ValueError),
])
def test_cell_size_xy_raises(x, y, exception):
    """
    Test Cell Size XY exceptions
    """
    with raises(exception):
        CellSizeXY(x=x, y=y)
# End test_cell_size_xy_raises function


@mark.parametrize('x, y, expected', [
    (1, 2, '1 2'),
    (1.11, 2.22, '1.11 2.22'),
])
def test_cell_size_xy_repr(x, y, expected):
    """
    Test Cell Size XY repr
    """
    assert repr(CellSizeXY(x=x, y=y)) == expected
# End test_cell_size_xy_repr function


def test_cell_size_xy_hash_support():
    """
    Test Cell Size XY hash implementation
    """
    xy = CellSizeXY(1, 2)
    assert xy == CellSizeXY(1, 2)
    assert xy != (1, 2)
    assert xy.as_tuple() == (1, 2)
    assert len({xy, xy}) == 1
# End test_cell_size_xy_hash_support function


@mark.parametrize('minimum, maximum, exception', [
    ('', '', TypeError),
    (0, 0, ValueError),
])
def test_range_domain_raise(minimum, maximum, exception):
    """
    Test range domain exceptions
    """
    with raises(exception):
        BaseRangeDomain(minimum, maximum)
# End test_range_domain_raise function


@mark.parametrize('minimum, maximum, expected', [
    (0, 100, '0 100'),
    (0.123, 123.456, '0.123 123.456'),
    (-10, 20, '-10 20'),
    (123.45, 12.345, '12.345 123.45'),
])
def test_range_domain_repr(minimum, maximum, expected):
    """
    Test range domain repr
    """
    assert repr(BaseRangeDomain(minimum, maximum)) == expected
# End test_range_domain_repr function


def test_range_domain_hash_support():
    """
    Test range domain hash implementation
    """
    domain = BaseRangeDomain(1, 2)
    assert domain == BaseRangeDomain(1, 2)
    assert domain != (1, 2)
    assert domain.as_tuple() == (1, 2)
    assert len({domain, domain}) == 1
# End test_range_domain_hash_support function


@mark.parametrize('x, y, exception', [
    ('', '', TypeError),
    (0, 0, TypeError),
])
def test_xy_domain_raise(x, y, exception):
    """
    Test xy domain exceptions
    """
    with raises(exception):
        XYDomain(x, y)
# End test_xy_domain_raise function


def test_xy_domain_repr():
    """
    Test xy domain exceptions
    """
    xy = XYDomain(XDomain(0, 100), YDomain(1000, 2000))
    assert repr(xy) == '0 1000 100 2000'
# End test_xy_domain_repr function


def test_xy_domain_hash_support():
    """
    Test XY domain hash implementation
    """
    domain = XYDomain(XDomain(0, 100), YDomain(1000, 2000))
    assert domain == XYDomain(XDomain(0, 100), YDomain(1000, 2000))
    assert domain != (0, 1000, 100, 2000)
    assert domain.as_tuple() == (0, 1000, 100, 2000)
    assert len({domain, domain}) == 1
# End test_xy_domain_hash_support function


@mark.parametrize('cls, value, unit, exception', [
    (ArealUnitValue, '', '', TypeError),
    (ArealUnitValue, 0, 0, TypeError),
])
def test_unit_value_raise(cls, value, unit, exception):
    """
    Test unit value exceptions
    """
    with raises(exception):
        cls(value, unit)
# End test_unit_value_raise function


@mark.parametrize('cls, value, unit, expected', [
    (ArealUnitValue, 0, ArealUnit.SQUARE_MILLIMETERS, '0 SquareMillimeters'),
    (LinearUnitValue, 0.123, LinearUnit.METERS, '0.123 Meters'),
    (TimeUnitValue, -10, TimeUnit.HOURS, '-10 Hours'),
])
def test_unit_value_repr(cls, value, unit, expected):
    """
    Test unit value repr
    """
    assert repr(cls(value, unit)) == expected
# End test_unit_value_repr function


def test_unit_value_hash_support():
    """
    Test unit value hash implementation
    """
    value = BaseUnitValue(1, ArealUnit.SQUARE_MILES)
    assert value == BaseUnitValue(1, ArealUnit.SQUARE_MILES)
    assert value != (1, ArealUnit.SQUARE_MILES)
    assert value.as_tuple() == (1, ArealUnit.SQUARE_MILES)
    assert len({value, value}) == 1
# End test_unit_value_hash_support function


if __name__ == '__main__':  # pragma: no cover
    pass
