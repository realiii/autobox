# -*- coding: utf-8 -*-
"""
Parameter Test
"""


from pytest import mark, raises
from stoolbox.parameter import (
    DoubleParameter, InputOutputParameter, InputParameter, LongParameter,
    StringParameter)


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


def test_parameter_simple_string():
    """
    Test Parameter Simple String
    """
    name = "Simple_String_Name"
    expected_content = {
        name: {
            "displayname": "$rc:simple_string_name.title",
            "category": "$rc:params.category1",
            "datatype": {"type": "GPString"},
            "value": "the quick brown fox",
            "description": "$rc:simple_string_name.descr"}
    }
    expected_resource = {
        "simple_string_name.descr": "plain text description",
        "simple_string_name.title": "Simple String Label",
    }
    category = 'cat 1'
    param = StringParameter(
        label='Simple String Label', name=name, category=category,
        description='plain text description',
        default_value='the quick brown fox')
    categories = {category: 1}
    content, resource = param.serialize(categories)
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_simple_string function


def test_parameter_derived_string():
    """
    Test Parameter derived string
    """
    name = "DerivedStringName"
    expected_content = {
        name: {
            "type": "derived",
            "direction": "out",
            "displayname": "$rc:derivedstringname.title",
            "category": "$rc:params.category2",
            "datatype": {"type": "GPString"},
            "value": "lazy dog",
            "description": "$rc:derivedstringname.descr"
        }
    }
    expected_resource = {
        "derivedstringname.descr": "<xdoc><p><span style=\"text-decoration:underline;\">underline </span><span>and </span><i>emphasis</i></p></xdoc>",
        "derivedstringname.title": "Derived String Label",
    }
    category = 'cat 2'
    param = StringParameter(
        label='Derived String Label', name=name, category=category,
        description='<p><span style=\"text-decoration:underline;\">underline </span><span>and </span><i>emphasis</i></p>',
        default_value='lazy dog')
    param.set_derived()
    categories = {category: 2}
    content, resource = param.serialize(categories)
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_derived_string function


def test_parameter_multi_string():
    """
    Test Parameter Multi String
    """
    name = "multi_string_name"
    expected_content = {
        name: {
            "type": "optional",
            "displayname": "$rc:multi_string_name.title",
            "category": "$rc:params.category1",
            "datatype": {
                "type": "GPMultiValue",
                "datatype": {
                    "type": "GPString"
                }
            },
            "value": "'jumps over the';'second line';'includes \"double quote\" characters';\"includes 'single quote' characters\"",
            "description": "$rc:multi_string_name.descr"
        },
    }
    expected_resource = {
        "multi_string_name.descr": "<xdoc><p><b>all bold</b></p></xdoc>",
        "multi_string_name.title": "Multi String Label",
    }
    category = 'cat 1'
    defaults = ('jumps over the', 'second line',
                'includes "double quote" characters',
                "includes 'single quote' characters")
    param = StringParameter(
        label='Multi String Label', name=name, category=category,
        description='<p><b>all bold</b></p>',
        default_value=defaults, is_required=False, is_multi=True)
    categories = {category: 1}
    content, resource = param.serialize(categories)
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_multi_string function


def test_parameter_long():
    """
    Test parameter long
    """
    name = "long_name"
    expected_content = {
        name: {
            "displayname": "$rc:long_name.title",
            "datatype": {"type": "GPLong"},
            "value": "123"
        },
    }
    expected_resource = {
        "long_name.title": "Long",
    }
    param = LongParameter(label='Long', name=name, default_value=123)
    content, resource = param.serialize({})
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_long function


def test_parameter_double():
    """
    Test parameter long multi
    """
    name = "double_name"
    expected_content = {
        name: {
            "displayname": "$rc:double_name.title",
            "datatype": {
                "type": "GPDouble"
            },
            "value": "123.456"
        },
    }
    expected_resource = {
        "double_name.title": "Double",
    }
    param = DoubleParameter(
        label='Double', name=name, default_value=123.456)
    content, resource = param.serialize({})
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_double function


def test_parameter_long_multi():
    """
    Test parameter long multi
    """
    name = "long_multi_name"
    expected_content = {
        name: {
            "displayname": "$rc:long_multi_name.title",
            "datatype": {
                "type": "GPMultiValue",
                "datatype": {
                    "type": "GPLong"
                }
            },
            "value": "12;34;56"
        },
    }
    expected_resource = {
        "long_multi_name.title": "Long Multi",
    }
    param = LongParameter(
        label='Long Multi', name=name, default_value=(12, 34, 56),
        is_multi=True)
    content, resource = param.serialize({})
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_long_multi function


def test_parameter_double_multi():
    """
    Test parameter long multi
    """
    name = "double_multi_name"
    expected_content = {
        name: {
            "displayname": "$rc:double_multi_name.title",
            "datatype": {
                "type": "GPMultiValue",
                "datatype": {
                    "type": "GPDouble"
                }
            },
            "value": "23.456;789.1"
        },
    }
    expected_resource = {
        "double_multi_name.title": "Double Multi",
    }
    param = DoubleParameter(
        label='Double Multi', name=name, default_value=(23.456, 789.1),
        is_multi=True)
    content, resource = param.serialize({})
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_double_multi function


if __name__ == '__main__':  # pragma: no cover
    pass
