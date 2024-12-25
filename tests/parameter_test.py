# -*- coding: utf-8 -*-
"""
Parameter Test
"""


from pytest import mark, raises
from autobox.parameter import (
    DoubleParameter, FeatureClassParameter, FeatureDatasetParameter,
    FeatureLayerParameter, InputOutputParameter, InputParameter, LongParameter,
    RasterDatasetParameter, StringParameter, TableParameter, TinParameter,
    WorkspaceParameter)


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


@mark.parametrize('cls, label, name, default_value, expected_content, expected_resource', [
    (LongParameter, 'Long', 'long_name', 123,
     {"displayname": "$rc:long_name.title", "datatype": {"type": "GPLong"}, "value": "123"},
     {"long_name.title": "Long"}),
    (LongParameter, 'Long Multi', 'long_multi_name', (12, 34, 56),
     {"displayname": "$rc:long_multi_name.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "GPLong"}}, "value": "12;34;56"},
     {"long_multi_name.title": "Long Multi"}),
    (DoubleParameter, 'Double', 'double_name', 123.456,
     {"displayname": "$rc:double_name.title", "datatype": {"type": "GPDouble"}, "value": "123.456"},
     {"double_name.title": "Double"}),
    (DoubleParameter, 'Double Multi', 'double_multi_name', (23.456, 789.1),
     {"displayname": "$rc:double_multi_name.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "GPDouble"}}, "value": "23.456;789.1"},
     {"double_multi_name.title": "Double Multi"}),
])
def test_parameter_numeric(cls, label, name, default_value, expected_content, expected_resource):
    """
    Test parameter numeric
    """
    param = cls(label=label, name=name, default_value=default_value,
                is_multi=isinstance(default_value, tuple))
    content, resource = param.serialize({})
    assert content == expected_content
    assert resource == expected_resource
# End test_parameter_numeric function


@mark.parametrize('cls, label, name, description, is_input, is_required, expected_content, expected_resource', [
    (WorkspaceParameter, 'Workspaces', 'workspaces', 'Allow for multiple workspaces', True, True,
     {"displayname": "$rc:workspaces.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "DEWorkspace"}}, "description": "$rc:workspaces.descr"},
     {"workspaces.descr": "Allow for multiple workspaces", "workspaces.title": "Workspaces"}),
    (WorkspaceParameter, 'Output Workspace', 'output_workspace_name', None, False, True,
     {"direction": "out", "displayname": "$rc:output_workspace_name.title", "datatype": {"type": "DEWorkspace"}},
     {"output_workspace_name.title": "Output Workspace"}),
    (FeatureDatasetParameter, 'A Feature Dataset', 'a_feature_dataset_name', None, False, True,
     {"direction": "out", "displayname": "$rc:a_feature_dataset_name.title", "datatype": {"type": "DEFeatureDataset"}},
     {"a_feature_dataset_name.title": "A Feature Dataset"}),
    (FeatureClassParameter, 'Main Feature Class', 'main_feature_class_name', None, False, False,
     {"type": "optional", "direction": "out", "displayname": "$rc:main_feature_class_name.title", "datatype": {"type": "DEFeatureClass"}, "schema": {"type": "GPFeatureSchema", "generateoutputcatalogpath": "true"}},
     {"main_feature_class_name.title": "Main Feature Class"}),
    (FeatureClassParameter, 'Feature Class Input', 'feature_class_input_name', None, True, True,
     {"displayname": "$rc:feature_class_input_name.title", "datatype": {"type": "DEFeatureClass"}},
     {"feature_class_input_name.title": "Feature Class Input"}),
    (FeatureLayerParameter, 'Feature Layer Example', 'feature_layer_example', None, True, True,
     {"displayname": "$rc:feature_layer_example.title", "datatype": {"type": "GPFeatureLayer"}},
     {"feature_layer_example.title": "Feature Layer Example"}),
    (RasterDatasetParameter, 'Raster Dataset Input', 'raster_dataset_input_name', None, True, True,
     {"displayname": "$rc:raster_dataset_input_name.title", "datatype": {"type": "DERasterDataset"}},
     {"raster_dataset_input_name.title": "Raster Dataset Input"}),
    (RasterDatasetParameter, 'Raster Dataset Output', 'raster_dataset_output_name', None, False, True,
     {"direction": "out", "displayname": "$rc:raster_dataset_output_name.title", "datatype": {"type": "DERasterDataset"}},
     {"raster_dataset_output_name.title": "Raster Dataset Output"}),
    (TinParameter, 'Tin Man', 'tin_man_name', None, True, True,
     {"displayname": "$rc:tin_man_name.title", "datatype": {"type": "DETin"}},
     {"tin_man_name.title": "Tin Man"}),
    (TableParameter, 'Table Input', 'table_input_name', None, True, True,
     {"displayname": "$rc:table_input_name.title", "datatype": {"type": "DETable"}},
     {"table_input_name.title": "Table Input"}),
    (TableParameter, 'Table Output', 'table_output_name', None, False, True,
     {"direction": "out", "displayname": "$rc:table_output_name.title", "datatype": {"type": "DETable"}, "schema": {"type": "GPTableSchema", "generateoutputcatalogpath": "true"}},
     {"table_output_name.title": "Table Output"}),
])
def test_parameter_data_element(cls, label, name, description, is_input, is_required, expected_content, expected_resource):
    """
    Test parameter data elements
    """
    param = cls(label=label, name=name, description=description,
                is_required=is_required, is_input=is_input,
                is_multi=name.endswith('s'))
    content, resource = param.serialize({})
    assert content == expected_content
    assert resource == expected_resource
# End test_parameter_workspace_multi function


if __name__ == '__main__':  # pragma: no cover
    pass
