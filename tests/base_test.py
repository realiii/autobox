# -*- coding: utf-8 -*-
"""
Base Class Tests
"""


from json import load
from pathlib import Path
from zipfile import ZipFile

from pytest import mark, raises

from stoolbox.base import Toolbox
from stoolbox.constants import EXT, TOOLBOX_CONTENT, TOOLBOX_CONTENT_RC


def _read_json(path: Path, name: str) -> dict:
    """
    Read JSON file from a zip
    """
    with ZipFile(path) as zin:
        with zin.open(name) as fin:
            return load(fin)
# End _read_json function


@mark.parametrize('name, label, alias, description, compare_name', [
    ('basic', None, None, None, 'basic'),
    ('empty', 'An Empty Toolbox', 'emptynounderscore', 'We should have included a description too.', 'empty'),
])
def test_toolbox_save(tmp_path, data_path, name, label, alias, description, compare_name):
    """
    Test Toolbox save method, compare with simple toolboxes.
    """
    tbx = Toolbox(name=name, label=label, alias=alias, description=description)
    tbx_path = tbx.save(tmp_path)
    assert tbx_path.is_file()
    compare_path = data_path.joinpath(f'{compare_name}{EXT}')
    assert compare_path.is_file()

    source_content = _read_json(tbx_path, TOOLBOX_CONTENT)
    source_resource = _read_json(tbx_path, TOOLBOX_CONTENT_RC)
    compare_content = _read_json(compare_path, TOOLBOX_CONTENT)
    compare_resource = _read_json(compare_path, TOOLBOX_CONTENT_RC)

    assert source_content == compare_content
    assert source_resource == compare_resource
# End test_toolbox_save function


def test_toolbox_save_bogus_path(tmp_path):
    """
    Test toolbox save when using a bogus path
    """
    tbx = Toolbox(name='bob')
    assert tbx.save(tmp_path / 'loblaw') is None
# End test_toolbox_save_bogus_path function


def test_toolbox_get_toolbox_path(tmp_path):
    """
    Test Toolbox _get_toolbox_path method
    """
    tbx = Toolbox(name='bob')
    expected = tmp_path.joinpath('bob.atbx')
    assert not expected.is_file()
    path = tbx._get_toolbox_path(tmp_path, overwrite=True)
    assert not path.is_file()
    assert path == expected
    tbx.save(tmp_path)
    assert path.is_file()
    with raises(FileExistsError):
        tbx._get_toolbox_path(tmp_path, overwrite=False)
    assert path.is_file()
    tbx._get_toolbox_path(tmp_path, overwrite=True)
    assert not path.is_file()
# End test_toolbox_get_toolbox_path function


@mark.parametrize('name', [
    'example', None
])
def test_toolbox_validate_name(name):
    """
    Test Toolbox validate_name method
    """
    if name:
        assert Toolbox._validate_name(name) == name
    else:
        with raises(ValueError):
            Toolbox._validate_name(name)
# End test_toolbox_validate_name function


def test_toolbox_validate_alias_raise():
    """
    Test Toolbox validate_alias method, exception
    """
    with raises(ValueError):
        Toolbox(name='1234')
# End test_toolbox_validate_alias_raise function


if __name__ == '__main__':  # pragma: no cover
    pass
