# -*- coding: utf-8 -*-
"""
Test Default Value Classes
"""


from pytest import raises

from autobox.default import CellSizeXY


def test_cell_size_xy():
    """
    Test Cell Size XY
    """
    with raises(TypeError):
        CellSizeXY(x=None, y=None)
    xy = CellSizeXY(x=1, y=2)
    assert repr(xy) == '1 2'
    xy = CellSizeXY(x=1.11, y=2.22)
    assert repr(xy) == '1.11 2.22'
# End test_cell_size_xy function


if __name__ == '__main__':  # pragma: no cover
    pass
