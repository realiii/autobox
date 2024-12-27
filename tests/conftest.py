# -*- coding: utf-8 -*-
"""
Test Fixtures
"""


from pathlib import Path
from typing import Generator

from pytest import fixture


@fixture(scope='session')
def data_path() -> Generator[Path, None, None]:
    """
    Data Path
    """
    yield Path(__file__).parent.parent.joinpath('data')
# End data_path function


if __name__ == '__main__':  # pragma: no cover
    pass
