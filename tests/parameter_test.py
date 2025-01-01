# -*- coding: utf-8 -*-
"""
Parameter Test
"""


from pathlib import Path

from pytest import approx, mark, raises

from autobox.constant import ParameterContentKeys
from autobox.default import (
    CellSizeXY, MDomain, XDomain, XYDomain, YDomain,
    ZDomain)
from autobox.enum import (
    ArealUnit, SACellSize, FieldType, GeometryType, LinearUnit, WorkspaceType)
from autobox.filter import (
    ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, WorkspaceTypeFilter)
from autobox.parameter import (
    AnalysisCellSizeParameter, ArealUnitParameter, BooleanParameter,
    CalculatorExpressionParameter, CellSizeXYParameter, DoubleParameter,
    EncryptedStringParameter, FeatureClassParameter, FeatureDatasetParameter,
    FeatureLayerParameter, FieldParameter, FileParameter, FolderParameter,
    InputOutputParameter, InputParameter, LinearUnitParameter, LongParameter,
    MDomainParameter, RasterDatasetParameter, SACellSizeParameter,
    SQLExpressionParameter, StringHiddenParameter, StringParameter,
    TableParameter, TinParameter, WorkspaceParameter, XYDomainParameter,
    ZDomainParameter)


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
    content, resource = param.serialize(categories, target=None)
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
    content, resource = param.serialize(categories, target=None)
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
    content, resource = param.serialize(categories, target=None)
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
    content, resource = param.serialize({}, target=None)
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
    content, resource = param.serialize({}, target=None)
    assert content == expected_content
    assert resource == expected_resource
# End test_parameter_workspace_multi function


def test_parameter_dependency():
    """
    Test parameter dependency
    """
    param1 = FeatureClassParameter(name='FeatureClassName', label='Feature Class Name')
    param2 = FieldParameter(name='FieldName', label='Field Name')
    key = ParameterContentKeys.depends
    content, _ = param1.serialize({}, target=None)
    assert key not in content
    content, _ = param2.serialize({}, target=None)
    assert key not in content

    param1.dependency = param2
    assert param1.dependency is None

    with raises(TypeError):
        param2.dependency = Ellipsis

    param2.dependency = param1
    assert param2.dependency is not None
    content, _ = param2.serialize({}, target=None)
    assert key in content
    assert content[key] == ['FeatureClassName']
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
    param = ArealUnitParameter(label='Areal Unit', name='Areal_Unit')
    param.filter = ArealUnitFilter(list(ArealUnit))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = LinearUnitParameter(label='Linear Unit', name='Linear_Unit')
    param.filter = LinearUnitFilter(list(LinearUnit))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = FeatureClassParameter(label='Feature Type', name='Feature_Type')
    param.filter = FeatureClassTypeFilter(list(GeometryType))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = FieldParameter(label='Field Type', name='Field_Type')
    param.filter = FieldTypeFilter(list(FieldType))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = FileParameter(label='File Type', name='File_Type')
    param.filter = FileTypeFilter(('txt', 'csv ', 'shp'))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = WorkspaceParameter(label='Workspace', name='Workspace')
    param.filter = WorkspaceTypeFilter(list(WorkspaceType))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = LongParameter(label='Long Range', name='Long_Range')
    param.filter = LongRangeFilter(-1, 9876543210)
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
                "min": "-999.99900000000002",
                "max": "9876.5429999999997"
            }
        }
    }
    expected_resource = {
        "double_range.title": "Double Range",
    }
    values = -999.999, 9876.543
    param = DoubleParameter(label='Double Range', name='Double_Range')
    param.filter = DoubleRangeFilter(*values)
    content, resource = param.serialize({}, target=None)
    domain = content['domain']
    assert domain['type'] == 'GPRangeDomain'
    min_value = float(domain['min'])
    max_value = float(domain['max'])
    assert approx(values, abs=0.001) == (min_value, max_value)
    assert resource == expected_resource
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
    param = LongParameter(label='Long Value', name='Long_Value')
    param.filter = LongValueFilter((-999, 0, 1, 2, 3, 4, 5, 1234567890))
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = DoubleParameter(label='Double Value', name='Double_Value')
    param.filter = DoubleValueFilter(values)
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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
    param = StringParameter(label='String Value', name='String_Value')
    param.filter = StringValueFilter(values)
    content, resource = param.serialize({}, target=None)
    assert content == expected_content[param.name]
    assert resource == expected_resource
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

    fc = FeatureClassParameter(label='Feature Class')
    assert fc.symbology is None
    fc.symbology = None
    assert fc.symbology is None

    with raises(TypeError):
        fc.symbology = script
    assert fc.symbology is None

    with raises(FileNotFoundError):
        fc.symbology = lyr_legacy
    assert fc.symbology is None

    fc = FeatureClassParameter(label='Feature Class', is_input=False)
    fc.symbology = lyr
    assert fc.symbology is not None

    content, resources = fc.serialize({}, target=tmp_path)
    assert ParameterContentKeys.symbology in content
    value = content[ParameterContentKeys.symbology]
    assert lyr.name in value
    assert resources == {'feature_class.title': 'Feature Class'}
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
    b = BooleanParameter(label='Boolean', name='Boolean')
    assert b.default_value is True
    with raises(TypeError):
        b.default_value = 'True'
# End test_boolean_specialization function


def test_default_value_analysis_cell_size():
    """
    Test default value analysis cell size
    """
    p = AnalysisCellSizeParameter(label='Analysis Cell Size')
    with raises(TypeError):
        p.default_value = '100'

    with raises(ValueError):
        p.default_value = -10

    p.default_value = 100
    assert p.default_value == 100
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '100'

    p.default_value = 123.45
    assert p.default_value == 123.45
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '123.45'

    path = Path('c:/temp/test.tif')
    p.default_value = path
    assert p.default_value == path
    data, _ = p.serialize({}, target=None)
    assert data['value'] == 'c:/temp/test.tif'

    p.default_value = None
    assert p.default_value is None
# End test_default_value_analysis_cell_size function


def test_default_value_cell_size_xy():
    """
    Test default value cell size xy
    """
    p = CellSizeXYParameter(label='Cell Size XY')
    with raises(TypeError):
        p.default_value = '100'
    with raises(TypeError):
        p.default_value = 100

    xy = CellSizeXY(100, 200)
    p.default_value = xy
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '100 200'

    xy = CellSizeXY(100.123, 200.456)
    p.default_value = xy
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '100.123 200.456'

    p.default_value = None
    assert p.default_value is None
# End test_default_value_cell_size_xy function


def test_default_value_sa_cell_size():
    """
    Test default value sa cell size
    """
    p = SACellSizeParameter(label='SA Cell Size')
    with raises(TypeError):
        p.default_value = '100'
    with raises(TypeError):
        p.default_value = 100

    path = Path('c:/temp/test.tif')
    p.default_value = path
    assert p.default_value == path
    data, _ = p.serialize({}, target=None)
    assert data['value'] == 'c:/temp/test.tif'

    p.default_value = SACellSize.MAXIMUM
    data, _ = p.serialize({}, target=None)
    assert data['value'] == 'Maximum of Inputs'

    p.default_value = SACellSize.MINIMUM
    data, _ = p.serialize({}, target=None)
    assert data['value'] == 'Minimum of Inputs'

    p.default_value = None
    assert p.default_value is None
# End test_default_value_sa_cell_size function


@mark.parametrize('param_cls, default_cls', [
    (MDomainParameter, MDomain),
    (ZDomainParameter, ZDomain)
])
def test_default_value_range_domain(param_cls, default_cls):
    """
    Test Default Value for M Domain and Z Domain
    """
    p = param_cls(label='Domain')
    with raises(TypeError):
        p.default_value = '100'

    p.default_value = default_cls(-1000, 1000)
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '-1000 1000'
# End test_default_value_m_domain function


def test_default_value_xy_domain():
    """
    Test Default Value for XY Domain
    """
    p = XYDomainParameter(label='XY Domain')
    with raises(TypeError):
        p.default_value = '100'

    p.default_value = XYDomain(XDomain(-1000, 1000), YDomain(-2000, 2000))
    data, _ = p.serialize({}, target=None)
    assert data['value'] == '-1000 -2000 1000 2000'
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
    p = cls(label='String')
    with raises(ValueError):
        p.default_value = 'abc'
    assert p.default_value is None
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
    p = cls(label='String')
    with raises(TypeError):
        p.default_value = 12345
    assert p.default_value is None
    value = 'abcdefg'
    p.default_value = value
    assert p.default_value == value
    data, _ = p.serialize({}, target=None)
    assert data['value'] == value
# End test_default_value_string_calc_sql function


if __name__ == '__main__':  # pragma: no cover
    pass
