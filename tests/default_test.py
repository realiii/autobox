# -*- coding: utf-8 -*-
"""
Test Default Value Classes
"""


from pytest import mark, raises

from autobox.default import (
    BaseRangeDomain, CellSizeXY, XDomain, XYDomain,
    YDomain)


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


def test_cell_size_xy():
    """
    Test Cell Size XY
    """
    with raises(TypeError):
        CellSizeXY(x=None, y=None)
    with raises(ValueError):
        CellSizeXY(x=-1, y=-2)
    xy = CellSizeXY(x=1, y=2)
    assert repr(xy) == '1 2'
    xy = CellSizeXY(x=1.11, y=2.22)
    assert repr(xy) == '1.11 2.22'
# End test_cell_size_xy function


if __name__ == '__main__':  # pragma: no cover
    pass
