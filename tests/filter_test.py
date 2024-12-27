# -*- coding: utf-8 -*-
"""
Filter Tests
"""

from pytest import approx, mark

from autobox.enum import (
    ArealUnit, FieldType, GeometryType, LinearUnit, WorkspaceType)
from autobox.filter import (
    AbstractNumberValueFilter, AbstractRangeFilter, ArealUnitFilter,
    DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter,
    FileTypeFilter, LinearUnitFilter, LongRangeFilter, LongValueFilter,
    StringValueFilter, WorkspaceTypeFilter)


def test_areal_unit_filter():
    """
    Test Areal Unit Filter
    """
    expected = {
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
            {"type": "GPArealUnit", "value": "Hectares", "code": "Hectares"},
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
    ftr = ArealUnitFilter(list(ArealUnit))
    assert ftr.serialize() == expected
# End test_areal_unit_filter function


def test_feature_class_type_filter():
    """
    Test Feature Class Type Filter
    """
    expected = {
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
    ftr = FeatureClassTypeFilter(list(GeometryType))
    assert ftr.serialize() == expected
# End test_feature_class_type_filter function


def test_field_type_filter():
    """
    Test Field Type Filter
    """
    expected = {
        "domain": {"type": "GPFieldDomain",
                   "fieldtype": ["Short", "Long", "Float", "BigInteger",
                                 "Double", "Text", "Date", "OID", "TimeOnly",
                                 "DateOnly", "TimestampOffset", "Geometry",
                                 "Blob", "Raster", "GUID", "GlobalID", "XML"]}}
    ftr = FieldTypeFilter(list(FieldType))
    assert ftr.serialize() == expected
# End test_field_type_filter function


def test_file_type_filter():
    """
    Test File Type Filter
    """
    expected = {
        "domain": {
            "type": "GPFileDomain",
            "filetypes": [
                "txt",
                "csv",
                "shp"
            ]
        }
    }
    ftr = FileTypeFilter(('.txt', '.csv ', None, 'shp'))
    assert ftr.serialize() == expected
# End test_file_type_filter function


def test_linear_unit_filter():
    """
    Test Linear Unit Filter
    """
    expected = {"domain": {"type": "GPCodedValueDomain", "items": [
        {"type": "GPLinearUnit", "value": "Unknown", "code": "Unknown"},
        {"type": "GPLinearUnit", "value": "Inches", "code": "Inches"},
        {"type": "GPLinearUnit", "value": "InchesInt", "code": "InchesInt"},
        {"type": "GPLinearUnit", "value": "Points", "code": "Points"},
        {"type": "GPLinearUnit", "value": "Feet", "code": "Feet"},
        {"type": "GPLinearUnit", "value": "FeetInt", "code": "FeetInt"},
        {"type": "GPLinearUnit", "value": "Yards", "code": "Yards"},
        {"type": "GPLinearUnit", "value": "Miles", "code": "Miles"},
        {"type": "GPLinearUnit", "value": "NauticalMiles",
         "code": "NauticalMiles"},
        {"type": "GPLinearUnit", "value": "NauticalMilesInt",
         "code": "NauticalMilesInt"},
        {"type": "GPLinearUnit", "value": "MilesInt", "code": "MilesInt"},
        {"type": "GPLinearUnit", "value": "YardsInt", "code": "YardsInt"},
        {"type": "GPLinearUnit", "value": "Millimeters", "code": "Millimeters"},
        {"type": "GPLinearUnit", "value": "Centimeters", "code": "Centimeters"},
        {"type": "GPLinearUnit", "value": "Meters", "code": "Meters"},
        {"type": "GPLinearUnit", "value": "Kilometers", "code": "Kilometers"},
        {"type": "GPLinearUnit", "value": "DecimalDegrees",
         "code": "DecimalDegrees"},
        {"type": "GPLinearUnit", "value": "Decimeters", "code": "Decimeters"}]}}
    ftr = LinearUnitFilter(list(LinearUnit))
    assert ftr.serialize() == expected
# End test_linear_unit_filter function


def test_workspace_type_filter():
    """
    Test Workspace Type Filter
    """
    expected = {
        "domain": {"type": "GPWorkspaceDomain",
                   "workspacetype": ["File System", "Local Database",
                                     "Remote Database"]}}
    ftr = WorkspaceTypeFilter(list(WorkspaceType))
    assert ftr.serialize() == expected
# End test_workspace_type_filter function


def test_long_range_filter():
    """
    Test Long Range Filter
    """
    expected = {
        "domain": {
            "type": "GPRangeDomain",
            "min": "-1",
            "max": "9876543210"
        }
    }
    ftr = LongRangeFilter(-1, 9876543210)
    assert ftr.serialize() == expected
# End test_long_range_filter function


def test_double_range_filter():
    """
    Test Double Range Filter
    """
    values = -999.999, 9876.543
    ftr = DoubleRangeFilter(*values)
    data = ftr.serialize()
    domain = data['domain']
    assert domain['type'] == 'GPRangeDomain'
    min_value = float(domain['min'])
    max_value = float(domain['max'])
    assert approx(values, abs=0.001) == (min_value, max_value)
# End test_double_range_filter function


def test_long_value_filter():
    """
    Test Long Value Filter
    """
    expected = {
        "domain": {"type": "GPCodedValueDomain", "items": [
            {"type": "GPLong", "value": "-999", "code": "-999"},
            {"type": "GPLong", "value": "0", "code": "0"},
            {"type": "GPLong", "value": "1", "code": "1"},
            {"type": "GPLong", "value": "2", "code": "2"},
            {"type": "GPLong", "value": "3", "code": "3"},
            {"type": "GPLong", "value": "4", "code": "4"},
            {"type": "GPLong", "value": "5", "code": "5"},
            {"type": "GPLong", "value": "1234567890", "code": "1234567890"}]}
    }
    ftr = LongValueFilter((-999, 0, 1, 2, 3, 4, 5, 1234567890))
    assert ftr.serialize() == expected
# End test_long_value_filter function


def test_double_value_filter():
    """
    Test Double Value Filter
    """
    expected = {
        "domain": {"type": "GPCodedValueDomain", "items": [
            {"type": "GPDouble", "value": "-999.999", "code": "-999.999"},
            {"type": "GPDouble", "value": "1.1", "code": "1.1"},
            {"type": "GPDouble", "value": "2.22", "code": "2.22"},
            {"type": "GPDouble", "value": "3.333", "code": "3.333"},
            {"type": "GPDouble", "value": "4.4444", "code": "4.4444"},
            {"type": "GPDouble", "value": "5.55555", "code": "5.55555"},
            {"type": "GPDouble", "value": "123.456", "code": "123.456"}]}
    }
    ftr = DoubleValueFilter((-999.999, 1.1, 2.22, 3.333, 4.4444, 5.55555, 123.456))
    assert ftr.serialize() == expected
# End test_double_value_filter function


def test_string_value_filter():
    """
    Test String Value Filter
    """
    expected_content = {
        "domain": {"type": "GPCodedValueDomain", "items": [
            {"value": "A", "code": "$rc:string_value.domain.A"},
            {"value": "BB", "code": "$rc:string_value.domain.BB"},
            {"value": "CCC", "code": "$rc:string_value.domain.CCC"},
            {"value": "DDDD", "code": "$rc:string_value.domain.DDDD"}]}}
    expected_resource = {
        "string_value.domain.A": "A",
        "string_value.domain.BB": "BB",
        "string_value.domain.CCC": "CCC",
        "string_value.domain.DDDD": "DDDD",
    }
    param_name = 'string_value'
    ftp = StringValueFilter(('A', 'BB', 'CCC', 'DDDD'))
    content, resource = ftp.serialize(param_name)
    assert content == expected_content
    assert resource == expected_resource
# End test_string_value_filter function


@mark.parametrize('values, expected', [
    (None, {}),
    ({}, {}),
    (WorkspaceType.LOCAL_DATABASE, {}),
    (ArealUnit.ACRES_US, {'domain': {'items': [{'code': 'AcresUS', 'type': 'GPArealUnit', 'value': 'AcresUS'}], 'type': 'GPCodedValueDomain'}} ),
    (123, {}),
])
def test_coded_domain(values, expected):
    """
    Test Filter Edge Cases for coded domain
    """
    ftr = ArealUnitFilter(values)
    assert ftr.serialize() == expected
# End test_coded_domain function


@mark.parametrize('values, expected', [
    (None, {}),
    ({}, {}),
    (WorkspaceType.LOCAL_DATABASE, {'domain': {'type': 'GPWorkspaceDomain', 'workspacetype': ['Local Database']}}),
    (ArealUnit.ACRES_US, {}),
    (123, {}),
])
def test_workspace_list_domain(values, expected):
    """
    Test Filter Edge Cases for workspace list domain
    """
    ftr = WorkspaceTypeFilter(values)
    assert ftr.serialize() == expected
# End test_workspace_list_domain function


@mark.parametrize('values, expected', [
    (None, {}),
    ({}, {}),
    (GeometryType.POLYGON, {'domain': {'geometrytype': ['Polygon'], 'type': 'GPFeatureClassDomain'}}),
    (ArealUnit.ACRES_US, {}),
    (123, {}),
])
def test_feature_class_list_domain(values, expected):
    """
    Test Filter Edge Cases for feature class list domain
    """
    ftr = FeatureClassTypeFilter(values)
    assert ftr.serialize() == expected
# End test_feature_class_list_domain function


@mark.parametrize('values, expected', [
    (None, {}),
    ({}, {}),
    (123, {}),
])
def test_file_type_domain(values, expected):
    """
    Test Filter Edge Cases for File Type Domain
    """
    ftr = FileTypeFilter(values)
    assert ftr.serialize() == expected
# End test_file_type_domain function


@mark.parametrize('values, expected', [
    ([], []),
    (None, []),
    ((), []),
    ((1, 1, 1), []),
    ((1, None, 1), []),
    ((2, None, 1), [1, 2]),
    ((float('nan'), None, 1), []),
    ((float('nan'), 2, 1), [1, 2]),
])
def test_range_filter_edge_cases(values, expected):
    """
    Test Range Filter Edge Cases
    """
    a = AbstractRangeFilter(0, 0)
    assert a._validate_and_convert(values, type_=int) == expected
    assert a.serialize() == {}
# End test_range_filter_edge_cases function


@mark.parametrize('values, expected', [
    ([], []),
    (None, []),
    ((), []),
    ((1, 1, 1), [1]),
    ((1, None, 1), [1]),
    ((2, None, 1), [2, 1]),
    ((float('nan'), None, 1), [1]),
    ((float('nan'), 2, 1), [2, 1]),
])
def test_number_value_filter_edge_cases(values, expected):
    """
    Test Number Value Filter Edge Cases
    """
    ftr = AbstractNumberValueFilter([])
    assert ftr._validate_and_convert(values, type_=int) == expected
    assert ftr.serialize() == {}
# End test_number_value_filter_edge_cases function


def test_string_value_filter_edge_cases():
    """
    Test String Value Filter Edge Cases
    """
    ftr = StringValueFilter([])
    assert ftr.serialize('string_value') == ({}, {})
    assert ftr._validate_values(None) == []
# End test_string_value_filter_edge_cases function


if __name__ == '__main__':  # pragma: no cover
    pass
