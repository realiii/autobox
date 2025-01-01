# -*- coding: utf-8 -*-
"""
Test Default Value Classes
"""


from pytest import mark, raises

from autobox.default import (
    ArealUnitValue, BaseRangeDomain, BaseUnitValue, CellSizeXY, Envelope,
    Extent, LinearUnitValue, Point, TimeUnitValue, XDomain, XYDomain, YDomain)
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


@mark.parametrize('cls, x, y, exception', [
    (Extent, '', '', TypeError),
    (Envelope, 0, 0, TypeError),
])
def test_bounding_box_raise(cls, x, y, exception):
    """
    Test bounding box domain exceptions
    """
    with raises(exception):
        cls(x, y)
# End test_bounding_box_raise function


@mark.parametrize('cls', [
    Extent, Envelope
])
def test_bounding_box_repr(cls):
    """
    Test xy domain exceptions
    """
    xy = cls(XDomain(0, 100), YDomain(1000, 2000))
    assert repr(xy) == '0 1000 100 2000'
# End test_bounding_box_repr function


@mark.parametrize('cls', [
    Extent, Envelope
])
def test_bounding_box_hash_support(cls):
    """
    Test XY domain hash implementation
    """
    domain = cls(XDomain(0, 100), YDomain(1000, 2000))
    assert domain == cls(XDomain(0, 100), YDomain(1000, 2000))
    assert domain != (0, 1000, 100, 2000)
    assert domain.as_tuple()[:4] == (0, 1000, 100, 2000)
    assert len({domain, domain}) == 1
# End test_bounding_box_hash_support function


def test_extent_specialization():
    """
    Test Default Value Extent specialization
    """
    with raises(TypeError):
        Extent(0, 100, crs=Ellipsis)
    with raises(TypeError):
        Extent(XDomain(0, 100), YDomain(1000, 2000), crs=Ellipsis)
    e = Extent(XDomain(0, 100), YDomain(1000, 2000), crs='')
    assert e._crs is None

    crs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
    e = Extent(XDomain(0, 100), YDomain(1000, 2000), crs=crs)
    assert repr(e) == f'0 1000 100 2000 {crs}'
# End test_extent_specialization function


@mark.parametrize('x, y, exception', [
    (None, None, TypeError),
])
def test_point_raises(x, y, exception):
    """
    Test Cell Size XY exceptions
    """
    with raises(exception):
        Point(x=x, y=y)
# End test_point_raises function


@mark.parametrize('x, y, expected', [
    (1, 2, '1 2'),
    (1.11, 2.22, '1.11 2.22'),
])
def test_point_repr(x, y, expected):
    """
    Test Cell Size XY repr
    """
    assert repr(Point(x=x, y=y)) == expected
# End test_point_repr function


def test_point_hash_support():
    """
    Test Cell Size XY hash implementation
    """
    xy = Point(1, 2)
    assert xy == Point(1, 2)
    assert xy != (1, 2)
    assert xy.as_tuple() == (1, 2)
    assert len({xy, xy}) == 1
# End test_point_hash_support function


if __name__ == '__main__':  # pragma: no cover
    pass
