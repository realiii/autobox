# -*- coding: utf-8 -*-
"""
Parameter Test
"""


from pytest import mark, raises
from stoolbox.parameter import InputOutputParameter, InputParameter


def test_parameter_instantiate():
    """
    Test Parameter instantiation
    """
    param = InputOutputParameter(label='param')
    assert param.label == 'param'
    assert param.name == 'param'
    assert param.category is None
    assert param.description is None
    assert param.default_value is None
    assert not param.is_multi

    value = 'cat'
    param.category = value
    assert param.category == value
    value = 'desc'
    param.description = value
    assert param.description == value
    value = 'asdf'
    param.default_value = value
    assert param.default_value == value

    param.is_enabled = False
    assert not param.is_enabled
# End test_parameter_instantiate function


@mark.parametrize('cls, label, expected', [
    (InputOutputParameter, None, None),
    (InputOutputParameter, ' ', None),
    (InputOutputParameter, 'asdf', 'asdf'),
    (InputOutputParameter, '123', None),
    (InputParameter, None, None),
    (InputParameter, ' ', None),
    (InputParameter, 'asdf', 'asdf'),
    (InputParameter, '123', None),
])
def test_parameter_label(cls, label, expected):
    """
    Test Parameter label
    """
    if not expected:
        with raises(ValueError):
            cls(label=label)
    else:
        assert cls(label=label).label == expected
# End test_parameter_label function


@mark.parametrize('is_required, is_input, is_enabled', [
    (True, True, True),
    (True, True, False),
    (True, False, True),
    (True, False, False),
    (False, True, True),
    (False, True, False),
    (False, False, True),
    (False, False, False),
])
def test_parameter_set_derived(is_required, is_input, is_enabled):
    """
    Test Parameter set derived
    """
    param = InputOutputParameter(
        label='param', is_required=is_required, is_input=is_input,
        is_enabled=is_enabled)
    assert param.is_required is is_required
    assert param.is_input is is_input
    assert param.is_enabled is is_enabled
    param.set_derived()
    assert param.is_required is None
    assert not param.is_input
    assert param.is_enabled
# End test_parameter_set_derived function


if __name__ == '__main__':  # pragma: no cover
    pass
