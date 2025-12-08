# -*- coding: utf-8 -*-
"""
Parameter Test
"""


from copy import deepcopy
from datetime import datetime
from pathlib import Path
from sys import platform

from pytest import approx, mark, raises

from autobox.constant import ParameterContentKeys
from autobox.default import (
    ArealUnitValue, CellSizeXY, Envelope, Extent, LinearUnitValue, MDomain,
    Point, TimeUnitValue, XDomain, XYDomain, YDomain, ZDomain)
from autobox.enum import (
    ArealUnit, SACellSize, FieldType, GeometryType, LinearUnit, TimeUnit,
    WorkspaceType)
from autobox.filter import (
    ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, WorkspaceTypeFilter)
from autobox.parameter import (
    AnalysisCellSizeParameter, ArealUnitParameter, BooleanParameter,
    CalculatorExpressionParameter, CellSizeXYParameter,
    CoordinateSystemParameter, DateParameter, DbaseTableParameter,
    DoubleParameter, EncryptedStringParameter, EnvelopeParameter,
    ExtentParameter, FeatureClassParameter, FeatureDatasetParameter,
    FeatureLayerParameter, FieldParameter, FileParameter, FolderParameter,
    InputOutputParameter, InputParameter, LinearUnitParameter, LongParameter,
    MDomainParameter, MapDocumentParameter, PointParameter, PrjFileParameter,
    RasterDatasetParameter, SACellSizeParameter, SQLExpressionParameter,
    ShapeFileParameter, SpatialReferenceParameter, StringHiddenParameter,
    StringParameter, TableParameter, TextfileParameter, TimeUnitParameter,
    TinParameter, WorkspaceParameter, XYDomainParameter, ZDomainParameter)


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

    assert repr(param) == "InputOutputParameter(label='param', name='param', category='cat', description='desc', default_value='asdf', is_enabled=False)"
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


@mark.parametrize('is_required, is_input, is_enabled, expected', [
    (True, True, True, "InputOutputParameter(label='param', name='param')"),
    (True, True, False, "InputOutputParameter(label='param', name='param', is_enabled=False)"),
    (True, False, True, "InputOutputParameter(label='param', name='param', is_input=False)"),
    (True, False, False, "InputOutputParameter(label='param', name='param', is_input=False, is_enabled=False)"),
    (False, True, True, "InputOutputParameter(label='param', name='param', is_required=False)"),
    (False, True, False, "InputOutputParameter(label='param', name='param', is_required=False, is_enabled=False)"),
    (False, False, True, "InputOutputParameter(label='param', name='param', is_input=False, is_required=False)"),
    (False, False, False, "InputOutputParameter(label='param', name='param', is_input=False, is_required=False, is_enabled=False)"),
])
def test_parameter_set_derived(is_required, is_input, is_enabled, expected):
    """
    Test Parameter set derived
    """
    param = InputOutputParameter(
        label='param', is_required=is_required, is_input=is_input,
        is_enabled=is_enabled)
    assert param.is_required is is_required
    assert param.is_input is is_input
    assert param.is_enabled is is_enabled
    assert repr(param) == expected
    param.set_derived()
    assert param.is_required is None
    assert not param.is_input
    assert 'is_required=None' in repr(param)
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
    content, resource = param.serialize(categories, target=None)
    assert content == expected_content[name]
    assert resource == expected_resource
    assert repr(param) == "StringParameter(label='Simple String Label', name='Simple_String_Name', category='cat 1', description='plain text description', default_value='the quick brown fox')"
# End test_parameter_simple_string function


def test_parameter_simple_string_hash():
    """
    Test Parameter Simple String hash
    """
    name = "Simple_String_Name"
    category = 'cat 1'
    label = 'Simple String Label'
    description = 'plain text description'
    default = 'the quick brown fox'
    a = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=default)
    b = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=default)
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_simple_string_hash function


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
    content, resource = param.serialize(categories, target=None)
    assert content == expected_content[name]
    assert resource == expected_resource
    assert repr(param) == """StringParameter(label='Derived String Label', name='DerivedStringName', category='cat 2', description='<xdoc><p><span style="text-decoration:underline;">underline </span><span>and </span><i>emphasis</i></p></xdoc>', default_value='lazy dog', is_input=False, is_required=None)"""
# End test_parameter_derived_string function


def test_parameter_derived_string_hash():
    """
    Test Parameter derived string hash
    """
    name = "DerivedStringName"
    category = 'cat 2'
    description = '<p><span style=\"text-decoration:underline;\">underline </span><span>and </span><i>emphasis</i></p>'
    default = 'lazy dog'
    label = 'Derived String Label'
    a = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=default)
    a.set_derived()
    b = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=default)
    b.set_derived()
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_derived_string_hash function


def test_parameter_derived_deepcopy():
    """
    Test Parameter derived string deepcopy hash
    """
    name = "DerivedStringName"
    category = 'cat 2'
    description = '<p><span style=\"text-decoration:underline;\">underline </span><span>and </span><i>emphasis</i></p>'
    default = 'lazy dog'
    label = 'Derived String Label'
    a = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=default)
    a.set_derived()
    assert a.is_derived
    b = deepcopy(a)
    assert b.is_derived
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_derived_deepcopy function


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
    content, resource = param.serialize(categories, target=None)
    assert content == expected_content[name]
    assert resource == expected_resource
# End test_parameter_multi_string function


def test_parameter_multi_string_hash():
    """
    Test Parameter Multi String hash
    """
    name = "multi_string_name"
    category = 'cat 1'
    defaults = ('jumps over the', 'second line',
                'includes "double quote" characters',
                "includes 'single quote' characters")
    label = 'Multi String Label'
    description = '<p><b>all bold</b></p>'
    a = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=defaults,
        is_required=False, is_multi=True)
    b = StringParameter(
        label=label, name=name, category=category,
        description=description, default_value=defaults,
        is_required=False, is_multi=True)
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_multi_string_hash function


@mark.parametrize('cls, label, name, default_value, expected_content, expected_resource, expected_repr', [
    (LongParameter, 'Long', 'long_name', 123,
     {"displayname": "$rc:long_name.title", "datatype": {"type": "GPLong"}, "value": "123"},
     {"long_name.title": "Long"}, "LongParameter(label='Long', name='long_name', default_value=123)"),
    (LongParameter, 'Long Multi', 'long_multi_name', (12, 34, 56),
     {"displayname": "$rc:long_multi_name.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "GPLong"}}, "value": "12;34;56"},
     {"long_multi_name.title": "Long Multi"}, "LongParameter(label='Long Multi', name='long_multi_name', default_value=(12, 34, 56), is_multi=True)"),
    (DoubleParameter, 'Double', 'double_name', 123.456,
     {"displayname": "$rc:double_name.title", "datatype": {"type": "GPDouble"}, "value": "123.456"},
     {"double_name.title": "Double"}, "DoubleParameter(label='Double', name='double_name', default_value=123.456)"),
    (DoubleParameter, 'Double Multi', 'double_multi_name', (23.456, 789.1),
     {"displayname": "$rc:double_multi_name.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "GPDouble"}}, "value": "23.456;789.1"},
     {"double_multi_name.title": "Double Multi"}, "DoubleParameter(label='Double Multi', name='double_multi_name', default_value=(23.456, 789.1), is_multi=True)"),
])
def test_parameter_numeric(cls, label, name, default_value, expected_content, expected_resource, expected_repr):
    """
    Test parameter numeric
    """
    a = cls(label=label, name=name, default_value=default_value,
            is_multi=isinstance(default_value, tuple))
    b = cls(label=label, name=name, default_value=default_value,
            is_multi=isinstance(default_value, tuple))
    content, resource = a.serialize({}, target=None)
    assert content == expected_content
    assert resource == expected_resource
    assert repr(a) == expected_repr
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_numeric function


@mark.parametrize('cls, label, name, description, is_input, is_required, expected_content, expected_resource, expected_repr', [
    (WorkspaceParameter, 'Workspaces', 'workspaces', 'Allow for multiple workspaces', True, True,
     {"displayname": "$rc:workspaces.title", "datatype": {"type": "GPMultiValue", "datatype": {"type": "DEWorkspace"}}, "description": "$rc:workspaces.descr"},
     {"workspaces.descr": "Allow for multiple workspaces", "workspaces.title": "Workspaces"},
     "WorkspaceParameter(label='Workspaces', name='workspaces', description='Allow for multiple workspaces', is_multi=True)"),
    (WorkspaceParameter, 'Output Workspace', 'output_workspace_name', None, False, True,
     {"direction": "out", "displayname": "$rc:output_workspace_name.title", "datatype": {"type": "DEWorkspace"}},
     {"output_workspace_name.title": "Output Workspace"},
     "WorkspaceParameter(label='Output Workspace', name='output_workspace_name', is_input=False)"),
    (FeatureDatasetParameter, 'A Feature Dataset', 'a_feature_dataset_name', None, False, True,
     {"direction": "out", "displayname": "$rc:a_feature_dataset_name.title", "datatype": {"type": "DEFeatureDataset"}},
     {"a_feature_dataset_name.title": "A Feature Dataset"},
     "FeatureDatasetParameter(label='A Feature Dataset', name='a_feature_dataset_name', is_input=False)"),
    (FeatureClassParameter, 'Main Feature Class', 'main_feature_class_name', None, False, False,
     {"type": "optional", "direction": "out", "displayname": "$rc:main_feature_class_name.title", "datatype": {"type": "DEFeatureClass"}, "schema": {"type": "GPFeatureSchema", "generateoutputcatalogpath": "true"}},
     {"main_feature_class_name.title": "Main Feature Class"},
     "FeatureClassParameter(label='Main Feature Class', name='main_feature_class_name', is_input=False, is_required=False)"),
    (FeatureClassParameter, 'Feature Class Input', 'feature_class_input_name', None, True, True,
     {"displayname": "$rc:feature_class_input_name.title", "datatype": {"type": "DEFeatureClass"}},
     {"feature_class_input_name.title": "Feature Class Input"},
     "FeatureClassParameter(label='Feature Class Input', name='feature_class_input_name')"),
    (FeatureLayerParameter, 'Feature Layer Example', 'feature_layer_example', None, True, True,
     {"displayname": "$rc:feature_layer_example.title", "datatype": {"type": "GPFeatureLayer"}},
     {"feature_layer_example.title": "Feature Layer Example"},
     "FeatureLayerParameter(label='Feature Layer Example', name='feature_layer_example')"),
    (RasterDatasetParameter, 'Raster Dataset Input', 'raster_dataset_input_name', None, True, True,
     {"displayname": "$rc:raster_dataset_input_name.title", "datatype": {"type": "DERasterDataset"}},
     {"raster_dataset_input_name.title": "Raster Dataset Input"},
     "RasterDatasetParameter(label='Raster Dataset Input', name='raster_dataset_input_name')"),
    (RasterDatasetParameter, 'Raster Dataset Output', 'raster_dataset_output_name', None, False, True,
     {"direction": "out", "displayname": "$rc:raster_dataset_output_name.title", "datatype": {"type": "DERasterDataset"}},
     {"raster_dataset_output_name.title": "Raster Dataset Output"},
     "RasterDatasetParameter(label='Raster Dataset Output', name='raster_dataset_output_name', is_input=False)"),
    (TinParameter, 'Tin Man', 'tin_man_name', None, True, True,
     {"displayname": "$rc:tin_man_name.title", "datatype": {"type": "DETin"}},
     {"tin_man_name.title": "Tin Man"}, "TinParameter(label='Tin Man', name='tin_man_name')"),
    (TableParameter, 'Table Input', 'table_input_name', None, True, True,
     {"displayname": "$rc:table_input_name.title", "datatype": {"type": "DETable"}},
     {"table_input_name.title": "Table Input"}, "TableParameter(label='Table Input', name='table_input_name')"),
    (TableParameter, 'Table Output', 'table_output_name', None, False, True,
     {"direction": "out", "displayname": "$rc:table_output_name.title", "datatype": {"type": "DETable"}, "schema": {"type": "GPTableSchema", "generateoutputcatalogpath": "true"}},
     {"table_output_name.title": "Table Output"}, "TableParameter(label='Table Output', name='table_output_name', is_input=False)"),
])
def test_parameter_data_element(cls, label, name, description, is_input, is_required, expected_content, expected_resource, expected_repr):
    """
    Test parameter data elements
    """
    a = cls(label=label, name=name, description=description,
            is_required=is_required, is_input=is_input,
            is_multi=name.endswith('s'))
    b = cls(label=label, name=name, description=description,
            is_required=is_required, is_input=is_input,
            is_multi=name.endswith('s'))
    content, resource = a.serialize({}, target=None)
    assert content == expected_content
    assert resource == expected_resource
    assert repr(a) == expected_repr
    assert a == b
    assert hash(a) == hash(b)
# End test_parameter_workspace_multi function


def test_parameter_dependency():
    """
    Test parameter dependency
    """
    name = 'FeatureClassName'
    label = 'Feature Class Name'
    a = FeatureClassParameter(name=name, label=label)
    field_a = FieldParameter(name='FieldName', label='Field Name')
    key = ParameterContentKeys.depends
    content, _ = a.serialize({}, target=None)
    assert key not in content
    content, _ = field_a.serialize({}, target=None)
    assert key not in content

    a.dependency = field_a
    assert a.dependency is None

    with raises(TypeError):
        field_a.dependency = Ellipsis

    field_a.dependency = a
    assert field_a.dependency is not None
    content, _ = field_a.serialize({}, target=None)
    assert key in content
    assert content[key] == [name]

    assert repr(a) == "FeatureClassParameter(label='Feature Class Name', name='FeatureClassName')"
    assert repr(field_a) == "FieldParameter(label='Field Name', name='FieldName')"

    b = FeatureClassParameter(name=name, label=label)
    field_b = FieldParameter(name='FieldName', label='Field Name')
    field_b.dependency = b

    assert a == b
    assert hash(a) == hash(b)
    assert field_a == field_b
    assert hash(field_a) == hash(field_b)
# End test_parameter_dependency function


def test_areal_unit_parameter_filter():
    """
    Test Areal Unit Parameter Filter
    """
    expected_content = {
        "Areal_Unit": {
            "displayname": "$rc:areal_unit.title",
            "datatype": {"type": "GPArealUnit"},
            "domain": {"type": "GPCodedValueDomain", "items": [
                {"type": "GPArealUnit", "value": "Unknown", "code": "Unknown"},
                {"type": "GPArealUnit", "value": "SquareInches",
                 "code": "SquareInches"},
                {"type": "GPArealUnit", "value": "SquareFeet",
                 "code": "SquareFeet"},
                {"type": "GPArealUnit", "value": "SquareYards",
                 "code": "SquareYards"},
                {"type": "GPArealUnit", "value": "Acres", "code": "Acres"},
                {"type": "GPArealUnit", "value": "SquareMiles",
                 "code": "SquareMiles"},
                {"type": "GPArealUnit", "value": "SquareMillimeters",
                 "code": "SquareMillimeters"},
                {"type": "GPArealUnit", "value": "SquareCentimeters",
                 "code": "SquareCentimeters"},
                {"type": "GPArealUnit", "value": "SquareDecimeters",
                 "code": "SquareDecimeters"},
                {"type": "GPArealUnit", "value": "SquareMeters",
                 "code": "SquareMeters"},
                {"type": "GPArealUnit", "value": "Ares", "code": "Ares"},
                {"type": "GPArealUnit", "value": "Hectares",
                 "code": "Hectares"},
                {"type": "GPArealUnit", "value": "SquareKilometers",
                 "code": "SquareKilometers"},
                {"type": "GPArealUnit", "value": "SquareMilesUS",
                 "code": "SquareMilesUS"},
                {"type": "GPArealUnit", "value": "AcresUS", "code": "AcresUS"},
                {"type": "GPArealUnit", "value": "SquareYardsUS",
                 "code": "SquareYardsUS"},
                {"type": "GPArealUnit", "value": "SquareFeetUS",
                 "code": "SquareFeetUS"},
                {"type": "GPArealUnit", "value": "SquareInchesUS",
                 "code": "SquareInchesUS"}]}}
    }
    expected_resource = {
        "areal_unit.title": "Areal Unit",
    }
    a = ArealUnitParameter(label='Areal Unit', name='Areal_Unit')
    a.filter = ArealUnitFilter(list(ArealUnit))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "ArealUnitParameter(label='Areal Unit', name='Areal_Unit')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_areal_unit_parameter_filter function


def test_linear_unit_parameter_filter():
    """
    Test Linear Unit Parameter Filter
    """
    expected_content = {
        "Linear_Unit": {
            "displayname": "$rc:linear_unit.title",
            "datatype": {"type": "GPLinearUnit"},
            "domain": {"type": "GPCodedValueDomain", "items": [
                {"type": "GPLinearUnit", "value": "Unknown", "code": "Unknown"},
                {"type": "GPLinearUnit", "value": "Inches", "code": "Inches"},
                {"type": "GPLinearUnit", "value": "InchesInt",
                 "code": "InchesInt"},
                {"type": "GPLinearUnit", "value": "Points", "code": "Points"},
                {"type": "GPLinearUnit", "value": "Feet", "code": "Feet"},
                {"type": "GPLinearUnit", "value": "FeetInt", "code": "FeetInt"},
                {"type": "GPLinearUnit", "value": "Yards", "code": "Yards"},
                {"type": "GPLinearUnit", "value": "Miles", "code": "Miles"},
                {"type": "GPLinearUnit", "value": "NauticalMiles",
                 "code": "NauticalMiles"},
                {"type": "GPLinearUnit", "value": "NauticalMilesInt",
                 "code": "NauticalMilesInt"},
                {"type": "GPLinearUnit", "value": "MilesInt",
                 "code": "MilesInt"},
                {"type": "GPLinearUnit", "value": "YardsInt",
                 "code": "YardsInt"},
                {"type": "GPLinearUnit", "value": "Millimeters",
                 "code": "Millimeters"},
                {"type": "GPLinearUnit", "value": "Centimeters",
                 "code": "Centimeters"},
                {"type": "GPLinearUnit", "value": "Meters", "code": "Meters"},
                {"type": "GPLinearUnit", "value": "Kilometers",
                 "code": "Kilometers"},
                {"type": "GPLinearUnit", "value": "DecimalDegrees",
                 "code": "DecimalDegrees"},
                {"type": "GPLinearUnit", "value": "Decimeters",
                 "code": "Decimeters"}]}}}
    expected_resource = {
        "linear_unit.title": "Linear Unit",
    }
    a = LinearUnitParameter(label='Linear Unit', name='Linear_Unit')
    a.filter = LinearUnitFilter(list(LinearUnit))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "LinearUnitParameter(label='Linear Unit', name='Linear_Unit')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_linear_unit_parameter_filter function


def test_feature_class_parameter_filter():
    """
    Test Feature Class Parameter Filter
    """
    expected_content = {
        "Feature_Type": {
            "displayname": "$rc:feature_type.title",
            "datatype": {
                "type": "DEFeatureClass"
            },
            "domain": {
                "type": "GPFeatureClassDomain",
                "geometrytype": [
                    "Point",
                    "Multipoint",
                    "Polygon",
                    "Polyline",
                    "MultiPatch"
                ],
                "featuretype": [
                    "Annotation",
                    "Dimension"
                ]
            }
        }
    }
    expected_resource = {
        "feature_type.title": "Feature Type",
    }
    a = FeatureClassParameter(label='Feature Type', name='Feature_Type')
    a.filter = FeatureClassTypeFilter(list(GeometryType))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "FeatureClassParameter(label='Feature Type', name='Feature_Type')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_feature_class_parameter_filter function


def test_field_parameter_filter():
    """
    Test Field Parameter Filter
    """
    expected_content = {
        "Field_Type": {"displayname": "$rc:field_type.title",
                       "datatype": {"type": "Field"},
                       "domain": {"type": "GPFieldDomain",
                                  "fieldtype": ["Short", "Long", "Float",
                                                "BigInteger", "Double", "Text",
                                                "Date", "OID", "TimeOnly",
                                                "DateOnly", "TimestampOffset",
                                                "Geometry", "Blob", "Raster",
                                                "GUID", "GlobalID", "XML"]}}}
    expected_resource = {
        "field_type.title": "Field Type",
    }
    a = FieldParameter(label='Field Type', name='Field_Type')
    a.filter = FieldTypeFilter(list(FieldType))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "FieldParameter(label='Field Type', name='Field_Type')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_field_parameter_filter function


def test_file_parameter_filter():
    """
    Test File Parameter Filter
    """
    expected_content = {
        "File_Type": {"displayname": "$rc:file_type.title",
                      "datatype": {"type": "DEFile"},
                      "domain": {"type": "GPFileDomain",
                                 "filetypes": ["txt", "csv", "shp"]}}}
    expected_resource = {
        "file_type.title": "File Type",
    }
    a = FileParameter(label='File Type', name='File_Type')
    a.filter = FileTypeFilter(('txt', 'csv ', 'shp'))
    b = deepcopy(a)

    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "FileParameter(label='File Type', name='File_Type')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_file_parameter_filter function


def test_workspace_parameter_filter():
    """
    Test Workspace Parameter Filter
    """
    expected_content = {
        "Workspace": {
            "displayname": "$rc:workspace.title",
            "datatype": {
                "type": "DEWorkspace"
            },
            "domain": {
                "type": "GPWorkspaceDomain",
                "workspacetype": [
                    "File System",
                    "Local Database",
                    "Remote Database"
                ]
            }
        }
    }
    expected_resource = {
        "workspace.title": "Workspace",
    }
    a = WorkspaceParameter(label='Workspace', name='Workspace')
    a.filter = WorkspaceTypeFilter(list(WorkspaceType))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "WorkspaceParameter(label='Workspace', name='Workspace')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_workspace_parameter_filter function


def test_long_parameter_range_filter():
    """
    Test Long Parameter Range Filter
    """
    expected_content = {
        "Long_Range": {
            "displayname": "$rc:long_range.title",
            "datatype": {
                "type": "GPLong"
            },
            "domain": {
                "type": "GPRangeDomain",
                "min": "-1",
                "max": "9876543210"
            }
        }
    }
    expected_resource = {
        "long_range.title": "Long Range",
    }
    a = LongParameter(label='Long Range', name='Long_Range')
    a.filter = LongRangeFilter(-1, 9876543210)
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "LongParameter(label='Long Range', name='Long_Range')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_long_parameter_range_filter function


def test_double_parameter_range_filter():
    """
    Test Double Parameter Range Filter
    """
    expected_content = {
        "Double_Range": {
            "displayname": "$rc:double_range.title",
            "datatype": {
                "type": "GPDouble"
            },
            "domain": {
                "type": "GPRangeDomain",
                "min": "-999.999",
                "max": "9876.543"
            }
        }
    }
    expected_resource = {
        "double_range.title": "Double Range",
    }
    values = -999.999, 9876.543
    a = DoubleParameter(label='Double Range', name='Double_Range')
    a.filter = DoubleRangeFilter(*values)
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    domain = content['domain']
    assert domain['type'] == 'GPRangeDomain'
    min_value = float(domain['min'])
    max_value = float(domain['max'])
    assert approx(values, abs=0.001) == (min_value, max_value)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "DoubleParameter(label='Double Range', name='Double_Range')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_double_parameter_range_filter function


def test_long_parameter_value_filter():
    """
    Test Long Parameter Value Filter
    """
    expected_content = {
        "Long_Value": {
            "displayname": "$rc:long_value.title",
            "datatype": {"type": "GPLong"},
            "domain": {"type": "GPCodedValueDomain", "items": [
                {"type": "GPLong", "value": "-999", "code": "-999"},
                {"type": "GPLong", "value": "0", "code": "0"},
                {"type": "GPLong", "value": "1", "code": "1"},
                {"type": "GPLong", "value": "2", "code": "2"},
                {"type": "GPLong", "value": "3", "code": "3"},
                {"type": "GPLong", "value": "4", "code": "4"},
                {"type": "GPLong", "value": "5", "code": "5"},
                {"type": "GPLong", "value": "1234567890",
                 "code": "1234567890"}]}}}
    expected_resource = {
        "long_value.title": "Long Value",
    }
    a = LongParameter(label='Long Value', name='Long_Value')
    a.filter = LongValueFilter((-999, 0, 1, 2, 3, 4, 5, 1234567890))
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "LongParameter(label='Long Value', name='Long_Value')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_long_parameter_value_filter function


def test_double_parameter_value_filter():
    """
    Test Double Parameter Value Filter
    """
    expected_content = {
        "Double_Value": {
            "displayname": "$rc:double_value.title",
            "datatype": {"type": "GPDouble"},
            "domain": {"type": "GPCodedValueDomain", "items": [
                {"type": "GPDouble", "value": "-999.999", "code": "-999.999"},
                {"type": "GPDouble", "value": "1.1", "code": "1.1"},
                {"type": "GPDouble", "value": "2.22", "code": "2.22"},
                {"type": "GPDouble", "value": "3.333", "code": "3.333"},
                {"type": "GPDouble", "value": "4.4444", "code": "4.4444"},
                {"type": "GPDouble", "value": "5.55555", "code": "5.55555"},
                {"type": "GPDouble", "value": "123.456", "code": "123.456"}]}}}
    expected_resource = {
        "double_value.title": "Double Value",
    }
    values = -999.999, 1.1, 2.22, 3.333, 4.4444, 5.55555, 123.456
    a = DoubleParameter(label='Double Value', name='Double_Value')
    a.filter = DoubleValueFilter(values)
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "DoubleParameter(label='Double Value', name='Double_Value')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_double_parameter_value_filter function


def test_string_parameter_value_filter():
    """
    Test String Parameter Value Filter
    """
    expected_content = {
        "String_Value": {
            "displayname": "$rc:string_value.title",
            "datatype": {"type": "GPString"},
            "domain": {"type": "GPCodedValueDomain", "items": [
                {"value": "A", "code": "$rc:string_value.domain.A"},
                {"value": "BB", "code": "$rc:string_value.domain.BB"},
                {"value": "CCC", "code": "$rc:string_value.domain.CCC"},
                {"value": "DDDD", "code": "$rc:string_value.domain.DDDD"}]}}}
    expected_resource = {
        "string_value.domain.A": "A",
        "string_value.domain.BB": "BB",
        "string_value.domain.CCC": "CCC",
        "string_value.domain.DDDD": "DDDD",
        "string_value.title": "String Value",

    }
    values = "A", "BB", "CCC", "DDDD"
    a = StringParameter(label='String Value', name='String_Value')
    a.filter = StringValueFilter(values)
    b = deepcopy(a)
    content, resource = a.serialize({}, target=None)
    assert content == expected_content[a.name]
    assert resource == expected_resource
    assert repr(a) == "StringParameter(label='String Value', name='String_Value')"

    assert id(a) != id(b)
    assert id(a.filter) != id(b.filter)
    assert a == b
    assert hash(a) == hash(b)
# End test_string_parameter_value_filter function


def test_parameter_symbology(tmp_path, data_path):
    """
    Test parameter symbology
    """
    script = data_path / 'scripts' / 'example.py'
    assert script.is_file()
    lyr = data_path / 'boxbox.lyrx'
    assert lyr.is_file()
    lyr_legacy = data_path / 'boxbox.lyr'
    assert not lyr_legacy.is_file()

    a = FeatureClassParameter(label='Feature Class')
    assert a.symbology is None
    a.symbology = None
    assert a.symbology is None

    with raises(TypeError):
        a.symbology = script
    assert a.symbology is None

    with raises(FileNotFoundError):
        a.symbology = lyr_legacy
    assert a.symbology is None

    a = FeatureClassParameter(label='Feature Class', is_input=False)
    a.symbology = lyr
    b = deepcopy(a)
    assert a.symbology is not None
    content, resources = a.serialize({}, target=tmp_path)
    assert ParameterContentKeys.symbology in content
    value = content[ParameterContentKeys.symbology]
    assert lyr.name in value
    assert resources == {'feature_class.title': 'Feature Class'}
    assert repr(a) == "FeatureClassParameter(label='Feature Class', name='feature_class', is_input=False)"

    assert id(a) != id(b)
    assert id(a.symbology) != id(b.symbology)
    assert a == b
    assert hash(a) == hash(b)

# End test_parameter_symbology function


def test_parameter_sans_dep_types_accepts_same():
    """
    Test that a parameter without dependency types accepts the same type
    as a dependency parameter when set to derived
    """
    assert not FolderParameter.dependency_types
    file = FileParameter(label='a file')
    folder = FolderParameter(label='a folder')
    folder.dependency = file
    assert folder.dependency is None
    folder.dependency = folder
    assert folder.dependency is None

    folder.set_derived()
    folder.dependency = file
    assert folder.dependency is None
    folder.dependency = folder
    assert folder.dependency is None

    another = FolderParameter(label='another folder')
    folder.dependency = another
    assert folder.dependency is not None
# End test_parameter_sans_dep_types_accepts_same function


def test_parameter_validate_required():
    """
    Test Parameter _validate_required
    """
    with raises(ValueError):
        FeatureClassParameter(label='Feature Class', is_required=3)
# End test_parameter_validate_required function


def test_boolean_specialization():
    """
    Test Boolean Specialization
    """
    with raises(TypeError):
        BooleanParameter(label='Boolean', name='Boolean', default_value=1)
    with raises(ValueError):
        BooleanParameter(label='Boolean', name='Boolean', is_required=False)
    a = BooleanParameter(label='Boolean', name='Boolean')
    b = deepcopy(a)
    assert a.default_value is True
    with raises(TypeError):
        a.default_value = 'True'
    data, _ = a.serialize({}, target=None)
    assert data['value'] == 'true'
    assert repr(a) == "BooleanParameter(label='Boolean', name='Boolean', default_value=True)"
    assert a == b
    assert hash(a) == hash(b)
# End test_boolean_specialization function


def test_default_value_analysis_cell_size():
    """
    Test default value analysis cell size
    """
    a = AnalysisCellSizeParameter(label='Analysis Cell Size')
    b = deepcopy(a)

    assert a == b
    assert hash(a) == hash(b)

    with raises(TypeError):
        a.default_value = '100'

    with raises(ValueError):
        a.default_value = -10

    a.default_value = 100
    assert a.default_value == 100
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '100'

    assert repr(a) == "AnalysisCellSizeParameter(label='Analysis Cell Size', name='analysis_cell_size', default_value=100)"

    a.default_value = 123.45
    assert a.default_value == 123.45
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '123.45'

    assert repr(a) == "AnalysisCellSizeParameter(label='Analysis Cell Size', name='analysis_cell_size', default_value=123.45)"

    path = Path('c:/temp/test.tif')
    a.default_value = path
    assert a.default_value == path
    data, _ = a.serialize({}, target=None)
    assert data['value'] in ('c:/temp/test.tif', r'c:\temp\test.tif')

    assert repr(a).startswith("AnalysisCellSizeParameter(label='Analysis Cell Size', name='analysis_cell_size', default_value='c:")

    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "AnalysisCellSizeParameter(label='Analysis Cell Size', name='analysis_cell_size')"
# End test_default_value_analysis_cell_size function


def test_default_value_cell_size_xy():
    """
    Test default value cell size xy
    """
    a = CellSizeXYParameter(label='Cell Size XY')
    b = deepcopy(a)
    assert a == b
    assert hash(a) == hash(b)
    with raises(TypeError):
        a.default_value = '100'
    with raises(TypeError):
        a.default_value = 100

    xy = CellSizeXY(100, 200)
    a.default_value = xy
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '100 200'

    assert repr(a) == "CellSizeXYParameter(label='Cell Size XY', name='cell_size_xy', default_value=CellSizeXY(x=100, y=200))"

    xy = CellSizeXY(100.123, 200.456)
    a.default_value = xy
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '100.123 200.456'

    assert repr(a) == "CellSizeXYParameter(label='Cell Size XY', name='cell_size_xy', default_value=CellSizeXY(x=100.123, y=200.456))"

    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "CellSizeXYParameter(label='Cell Size XY', name='cell_size_xy')"
# End test_default_value_cell_size_xy function


def test_default_value_sa_cell_size():
    """
    Test default value sa cell size
    """
    a = SACellSizeParameter(label='SA Cell Size')
    b = deepcopy(a)
    assert a == b
    assert hash(a) == hash(b)
    with raises(TypeError):
        a.default_value = '100'
    with raises(TypeError):
        a.default_value = 100

    path = Path('c:/temp/test.tif')
    a.default_value = path
    assert a.default_value == path
    data, _ = a.serialize({}, target=None)
    assert data['value'] in ('c:/temp/test.tif', r'c:\temp\test.tif')

    assert repr(a).startswith("SACellSizeParameter(label='SA Cell Size', name='sa_cell_size', default_value='c:")

    a.default_value = SACellSize.MAXIMUM
    data, _ = a.serialize({}, target=None)
    assert data['value'] == 'Maximum of Inputs'

    assert repr(a) == "SACellSizeParameter(label='SA Cell Size', name='sa_cell_size', default_value=SACellSize.MAXIMUM)"

    a.default_value = SACellSize.MINIMUM
    data, _ = a.serialize({}, target=None)
    assert data['value'] == 'Minimum of Inputs'

    assert repr(a) == "SACellSizeParameter(label='SA Cell Size', name='sa_cell_size', default_value=SACellSize.MINIMUM)"

    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "SACellSizeParameter(label='SA Cell Size', name='sa_cell_size')"
# End test_default_value_sa_cell_size function


@mark.parametrize('param_cls, default_cls', [
    (MDomainParameter, MDomain),
    (ZDomainParameter, ZDomain)
])
def test_default_value_range_domain(param_cls, default_cls):
    """
    Test Default Value for M Domain and Z Domain
    """
    a = param_cls(label='Domain')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = '100'

    a.default_value = default_cls(-1000, 1000)
    b.default_value = default_cls(-1000, 1000)
    assert a == b
    assert hash(a) == hash(b)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '-1000 1000'
    assert repr(a) == f"{param_cls.__name__}(label='Domain', name='domain', default_value={default_cls.__name__}(minimum=-1000, maximum=1000))"
# End test_default_value_m_domain function


def test_default_value_xy_domain():
    """
    Test Default Value for XY Domain
    """
    a = XYDomainParameter(label='XY Domain')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = '100'

    a.default_value = XYDomain(XDomain(-1000, 1000), YDomain(-2000, 2000))
    b.default_value = XYDomain(XDomain(-1000, 1000), YDomain(-2000, 2000))
    assert a == b
    assert hash(a) == hash(b)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '-1000 -2000 1000 2000'
    assert repr(a) == "XYDomainParameter(label='XY Domain', name='xy_domain', default_value=XYDomain(x=XDomain(minimum=-1000, maximum=1000), y=YDomain(minimum=-2000, maximum=2000)))"
# End test_default_value_xy_domain function


@mark.parametrize('cls', [
    StringHiddenParameter,
    EncryptedStringParameter
])
def test_default_value_string_hidden_encrypted(cls):
    """
    Test Default Value for Hidden and Encrypted Strings
    """
    with raises(ValueError):
        cls(label='String', default_value='abc')
    a = cls(label='String')
    b = deepcopy(a)
    with raises(ValueError):
        a.default_value = 'abc'
    assert a == b
    assert hash(a) == hash(b)
    assert a.default_value is None
    assert repr(a) == f"{cls.__name__}(label='String', name='string')"
# End test_default_value_string_hidden_encrypted function


@mark.parametrize('cls', [
    CalculatorExpressionParameter,
    StringParameter,
    SQLExpressionParameter
])
def test_default_value_string_calc_sql(cls):
    """
    Test Default Value String, Calculator Expression, and SQL Expression
    """
    a = cls(label='String')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 12345
    assert a.default_value is None
    value = 'abcdefg'
    a.default_value = value
    b.default_value = value
    assert a.default_value == value
    assert a == b
    assert hash(a) == hash(b)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == value
    assert repr(a) == f"{cls.__name__}(label='String', name='string', default_value='abcdefg')"
# End test_default_value_string_calc_sql function


@mark.parametrize('value, expected', [
    ('100', ('100',)),
    (['100'], ('100',)),
    (['100', '100'], ('100',)),
])
def test_default_value_string_multi(value, expected):
    """
    Test Default Value String Multi
    """
    a = StringParameter(label='String', is_multi=True, default_value=value)
    b = deepcopy(a)
    assert a.default_value == expected
    assert repr(a) == "StringParameter(label='String', name='string', default_value=('100',), is_multi=True)"
    assert a == b
    assert hash(a) == hash(b)
# End test_default_value_string_multi function


@mark.parametrize('param_cls, default_cls, value, unit, expected, expected_repr', [
    (ArealUnitParameter, ArealUnitValue, 10, ArealUnit.HECTARES, '10 Hectares', "ArealUnitParameter(label='Unit', name='unit', default_value=ArealUnitValue(value=10, unit=ArealUnit.HECTARES))"),
    (LinearUnitParameter, LinearUnitValue, 123.45, LinearUnit.METERS, '123.45 Meters', "LinearUnitParameter(label='Unit', name='unit', default_value=LinearUnitValue(value=123.45, unit=LinearUnit.METERS))"),
    (TimeUnitParameter, TimeUnitValue, 31, TimeUnit.DAYS, '31 Days', "TimeUnitParameter(label='Unit', name='unit', default_value=TimeUnitValue(value=31, unit=TimeUnit.DAYS))"),
])
def test_default_value_unit(param_cls, default_cls, value, unit, expected, expected_repr):
    """
    Test Default Value Unit
    """
    a = param_cls(label='Unit')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 12345
    assert a.default_value is None

    u = default_cls(value, unit)
    a.default_value = u
    b.default_value = default_cls(value, unit)
    assert a.default_value == u
    data, _ = a.serialize({}, target=None)
    assert data['value'] == expected

    assert repr(a) == expected_repr

    assert a == b
    assert hash(a) == hash(b)
# End test_default_value_unit function


@mark.parametrize('param_cls, default_cls, args, expected, expected_repr', [
    (ArealUnitParameter, ArealUnitValue, ((10, ArealUnit.HECTARES), (5, ArealUnit.SQUARE_MILES)), "'10 Hectares';'5 SquareMiles'",
     "ArealUnitParameter(label='Unit', name='unit', default_value=(ArealUnitValue(value=10, unit=ArealUnit.HECTARES), ArealUnitValue(value=5, unit=ArealUnit.SQUARE_MILES)), is_multi=True)"),
    (LinearUnitParameter, LinearUnitValue, ((123.45, LinearUnit.METERS), (100, LinearUnit.FEET)), "'123.45 Meters';'100 Feet'",
     "LinearUnitParameter(label='Unit', name='unit', default_value=(LinearUnitValue(value=123.45, unit=LinearUnit.METERS), LinearUnitValue(value=100, unit=LinearUnit.FEET)), is_multi=True)"),
    (TimeUnitParameter, TimeUnitValue, (( 31, TimeUnit.DAYS), (2, TimeUnit.HOURS)), "'31 Days';'2 Hours'",
     "TimeUnitParameter(label='Unit', name='unit', default_value=(TimeUnitValue(value=31, unit=TimeUnit.DAYS), TimeUnitValue(value=2, unit=TimeUnit.HOURS)), is_multi=True)"),
])
def test_default_value_multi_unit(param_cls, default_cls, args, expected, expected_repr):
    """
    Test Default Value Unit
    """
    a = param_cls(label='Unit', is_multi=True)
    b = deepcopy(a)
    assert a.default_value is None
    units = [default_cls(*arg) for arg in args]
    a.default_value = units
    b.default_value = units
    assert a.default_value == tuple(units)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == expected
    assert repr(a) == expected_repr
    assert a == b
    assert hash(a) == hash(b)
# End test_default_value_unit function


@mark.parametrize('value, expected', [
    (123, '123'),
    (123., None),
])
def test_default_value_long(value, expected):
    """
    Test Default Value for Long
    """
    if expected is None:
        with raises(TypeError):
            LongParameter(label='Long', default_value=value)
    else:
        a = LongParameter(label='Long', default_value=value)
        b = deepcopy(a)
        data, _ = a.serialize({}, target=None)
        assert data['value'] == expected
        assert repr(a) == "LongParameter(label='Long', name='long', default_value=123)"
        assert a == b
        assert hash(a) == hash(b)
# End test_default_value_long function


@mark.parametrize('value, expected', [
    ((123, 456), '123;456'),
])
def test_default_value_long(value, expected):
    """
    Test Default Value for Long
    """
    a = LongParameter(label='Long', default_value=value, is_multi=True)
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == expected
    assert repr(a) == "LongParameter(label='Long', name='long', default_value=(123, 456), is_multi=True)"
    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)
# End test_default_value_long function


@mark.parametrize('value, expected', [
    (123, '123'),
    (123., '123.0'),
    (123.45, '123.45'),
    ('123.45', None),
])
def test_default_value_double(value, expected):
    """
    Test Default Value for Double
    """
    if expected is None:
        with raises(TypeError):
            DoubleParameter(label='Double', default_value=value)
    else:
        a = DoubleParameter(label='Double', default_value=value)
        b = deepcopy(a)
        data, _ = a.serialize({}, target=None)
        assert data['value'] == expected
        assert repr(a) == f"DoubleParameter(label='Double', name='double', default_value={value!r})"
        assert a == b
        assert hash(a) == hash(b)
# End test_default_value_double function


@mark.parametrize('value, expected', [
    ((123, 456), '123;456'),
    ((123., 456.), '123.0;456.0'),
    ((123.45, 456.78), '123.45;456.78'),
])
def test_default_value_double_multi(value, expected):
    """
    Test Default Value for Double
    """
    a = DoubleParameter(label='Double', default_value=value, is_multi=True)
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == expected
    assert repr(a) == f"DoubleParameter(label='Double', name='double', default_value={value!r}, is_multi=True)"
    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)
# End test_default_value_double_multi function


@mark.parametrize('value, expected', [
    ('12/12/12', None),
    ('12:12:12', None),
    ('12/12/12 12:12:12', None),
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56), '01/05/2025 12:34:56'),
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56).date(), '01/05/2025'),
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56).time(), '12:34:56'),
])
def test_default_value_date(value, expected):
    """
    Test Default Value for Date
    """
    if expected is None:
        with raises(TypeError):
            DateParameter(label='Date', default_value=value)
    else:
        a = DateParameter(label='Date', default_value=value)
        b = deepcopy(a)
        data, _ = a.serialize({}, target=None)
        assert data['value'] == expected
        assert repr(a) == f"DateParameter(label='Date', name='date', default_value={value!r})"
        assert a == b
        assert hash(a) == hash(b)
# End test_default_value_date function


@mark.parametrize('value, expected', [
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56), "'01/05/2025 12:34:56'"),
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56).date(), '01/05/2025'),
    (datetime(year=2025, month=1, day=5, hour=12, minute=34, second=56).time(), '12:34:56'),
    (None, '12:34:56'),
])
def test_default_value_date_multi(value, expected):
    """
    Test Default Value for Date
    """
    a = DateParameter(label='Date', default_value=value, is_multi=True)
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    if value is None:
        assert 'value' not in data
    else:
        assert data['value'] == expected
        assert repr(a) == f"DateParameter(label='Date', name='date', default_value=({value!r},), is_multi=True)"
        assert a == b
        assert hash(a) == hash(b)
        assert id(a) != id(b)
        assert id(a.default_value) != id(b.default_value)
# End test_default_value_date_multi function


def test_default_value_coordinate_system():
    """
    Test Default Value Coordinate System
    """
    a = CoordinateSystemParameter(label='Coordinate System')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 100
    crs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
    a.default_value = crs
    b.default_value = crs
    data, _ = a.serialize({}, target=None)
    assert data['value'] == crs
    assert repr(a) == f"CoordinateSystemParameter(label='Coordinate System', name='coordinate_system', default_value={crs!r})"
    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
# End test_default_value_coordinate_system function


def test_default_value_coordinate_system_multi():
    """
    Test Default Value Coordinate System
    """
    a = CoordinateSystemParameter(label='Coordinate System', is_multi=True)
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 100
    crs1 = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
    crs2 = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    a.default_value = (crs1, crs2)
    b.default_value = (crs1, crs2)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == "'{}';'{}'".format(crs1, crs2)
    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)
# End test_default_value_coordinate_system function


def test_default_value_spatial_reference():
    """
    Test Default Value Spatial Reference
    """
    a = SpatialReferenceParameter(label='Spatial Reference')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 100
    srs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision'
    a.default_value = srs
    b.default_value = srs
    data, _ = a.serialize({}, target=None)
    assert data['value'] == srs
    assert repr(a) == f"SpatialReferenceParameter(label='Spatial Reference', name='spatial_reference', default_value={srs!r})"
    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
# End test_default_value_spatial_reference function


def test_default_value_envelope():
    """
    Test Default Value Envelope
    """
    a = EnvelopeParameter(label='Envelope')
    b = deepcopy(a)
    with raises(TypeError):
        a.default_value = 100
    a.default_value = Envelope(XDomain(100, 200), YDomain(1000, 2000))
    b.default_value = Envelope(XDomain(100, 200), YDomain(1000, 2000))
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '100 1000 200 2000'

    assert repr(a) == "EnvelopeParameter(label='Envelope', name='envelope', default_value=Envelope(x=XDomain(minimum=100, maximum=200), y=YDomain(minimum=1000, maximum=2000)))"

    assert a == b
    assert hash(a) == hash(b)

    a.default_value = None
    assert a.default_value is None
    assert repr(a) == "EnvelopeParameter(label='Envelope', name='envelope')"
    assert id(a) != id(b)
# End test_default_value_envelope function


def test_default_value_envelope_multi():
    """
    Test Default Value Envelope Multi
    """
    a = EnvelopeParameter(label='Envelope', is_multi=True)
    envelopes = (Envelope(XDomain(100, 200), YDomain(1000, 2000)),
                 Envelope(XDomain(111, 222), YDomain(3333, 4444)))
    a.default_value = envelopes
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == "'100 1000 200 2000';'111 3333 222 4444'"

    assert repr(a) == "EnvelopeParameter(label='Envelope', name='envelope', default_value=(Envelope(x=XDomain(minimum=100, maximum=200), y=YDomain(minimum=1000, maximum=2000)), Envelope(x=XDomain(minimum=111, maximum=222), y=YDomain(minimum=3333, maximum=4444))), is_multi=True)"

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "EnvelopeParameter(label='Envelope', name='envelope', is_multi=True)"
# End test_default_value_envelope_multi function


def test_default_value_extent():
    """
    Test Default Value Extent
    """
    a = ExtentParameter(label='Extent')
    with raises(TypeError):
        a.default_value = 100
    crs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
    extents = Extent(XDomain(100, 200), YDomain(1000, 2000), crs=crs)
    a.default_value = extents
    b = deepcopy(a)

    assert repr(a) == f"ExtentParameter(label='Extent', name='extent', default_value=Extent(x=XDomain(minimum=100, maximum=200), y=YDomain(minimum=1000, maximum=2000), crs={crs!r}))"

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    data, _ = a.serialize({}, target=None)
    assert data['value'] == f'100 1000 200 2000 {crs}'
    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "ExtentParameter(label='Extent', name='extent')"
# End test_default_value_extent function


def test_default_value_extent_multi():
    """
    Test Default Value Extent Multi
    """
    a = ExtentParameter(label='Extent', is_multi=True)
    crs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
    extents = (Extent(XDomain(100, 200), YDomain(1000, 2000)),
               Extent(XDomain(111, 222), YDomain(3333, 4444), crs=crs))
    a.default_value = extents
    b = deepcopy(a)

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    data, _ = a.serialize({}, target=None)
    assert data['value'] == f"'100 1000 200 2000';'111 3333 222 4444 {crs}'"
    a.default_value = None
    assert a.default_value is None

    assert repr(a) == "ExtentParameter(label='Extent', name='extent', is_multi=True)"
# End test_default_value_extent_multi function


def test_default_value_point():
    """
    Test Default Value Point
    """
    a = PointParameter(label='Point')
    with raises(TypeError):
        a.default_value = 100
    a.default_value = Point(100, 200)
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == '100 200'

    assert repr(a) == "PointParameter(label='Point', name='point', default_value=Point(x=100, y=200))"

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    a.default_value = None
    assert a.default_value is None
# End test_default_value_point function


def test_default_value_point_multi():
    """
    Test Default Value Point Multi
    """
    a = PointParameter(label='Point', is_multi=True)
    points = Point(100, 200), Point(123.4, 45.6)
    a.default_value = points
    data, _ = a.serialize({}, target=None)
    assert data['value'] == "'100 200';'123.4 45.6'"
    b = deepcopy(a)

    assert repr(a) == "PointParameter(label='Point', name='point', default_value=(Point(x=100, y=200), Point(x=123.4, y=45.6)), is_multi=True)"

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    a.default_value = None
    assert a.default_value is None
# End test_default_value_point_multi function


@mark.parametrize('cls, expected_value, expected_repr', [
    (DbaseTableParameter, 'file2.dbf;file3.shp;file6.shp', ("DbaseTableParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file2.dbf'), PosixPath('file3.shp'), PosixPath('file6.shp')), is_multi=True)")),
    (FileParameter, 'file1.txt;file2.dbf;file3.shp;file4.mxd;file5.prj;file6.shp;file7.csv;file8.txt;file9.tab', "FileParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file1.txt'), PosixPath('file2.dbf'), PosixPath('file3.shp'), PosixPath('file4.mxd'), PosixPath('file5.prj'), PosixPath('file6.shp'), PosixPath('file7.csv'), PosixPath('file8.txt'), PosixPath('file9.tab')), is_multi=True)"),
    (MapDocumentParameter, 'file4.mxd', "MapDocumentParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file4.mxd'),), is_multi=True)"),
    (PrjFileParameter, 'file5.prj', "PrjFileParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file5.prj'),), is_multi=True)"),
    (ShapeFileParameter, 'file3.shp;file6.shp', "ShapeFileParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file3.shp'), PosixPath('file6.shp')), is_multi=True)"),
    (TextfileParameter, 'file1.txt;file7.csv;file8.txt;file9.tab', "TextfileParameter(label='Path Esque', name='path_esque', default_value=(PosixPath('file1.txt'), PosixPath('file7.csv'), PosixPath('file8.txt'), PosixPath('file9.tab')), is_multi=True)")
])
def test_default_value_path_esque_multi(cls, expected_value, expected_repr):
    """
    Test Default Value Path Esque Multi
    """
    if platform == 'win32':
        expected_repr = expected_repr.replace('PosixPath', 'WindowsPath')
    a = cls(label='Path Esque', is_multi=True)
    with raises(TypeError):
        a.default_value = ('/path/to/file1.txt', '/path/to/file2.txt')
    a.default_value = None
    assert a.default_value is None
    files = ('file1.txt', 'file2.dbf', 'file3.shp', 'file4.mxd', 'file5.prj',
             'file6.shp', 'file7.csv', 'file8.txt', 'file9.tab')
    paths = [Path(f) for f in files]
    a.default_value = paths
    b = deepcopy(a)
    data, _ = a.serialize({}, target=None)
    assert data['value'] == expected_value

    assert repr(a) == expected_repr

    assert a == b
    assert hash(a) == hash(b)
    assert id(a) != id(b)
    assert id(a.default_value) != id(b.default_value)

    paths = a.default_value
    if a.suffixes:
        with raises(ValueError):
            a.default_value = Path.home() / 'file.xyz'
    a = cls(label='Path Esque')
    a.default_value = paths[0]
    if a.suffixes:
        with raises(ValueError):
            a.default_value = Path.home() / 'file.xyz'
# End test_default_value_path_esque_multi function


if __name__ == '__main__':  # pragma: no cover
    pass
