# -*- coding: utf-8 -*-
"""
Enumerations for Filters
"""


from enum import StrEnum


__all__ = [
    'ArealUnit', 'FieldType', 'GeometryType', 'LinearUnit', 'SACellSize',
    'TimeUnit', 'TravelModeUnitType', 'WorkspaceType',
    'RATIONAL_FIELD_TYPES', 'INTEGER_FIELD_TYPES', 'NUMERIC_FIELD_TYPES',
    'STRING_FIELD_TYPES', 'IDENTIFIER_FIELD_TYPES',
]


class ArealUnit(StrEnum):
    """
    Area Unit Enumeration
    """
    UNKNOWN = 'Unknown'
    SQUARE_INCHES = 'SquareInches'
    SQUARE_FEET = 'SquareFeet'
    SQUARE_YARDS = 'SquareYards'
    ACRES = 'Acres'
    SQUARE_MILES = 'SquareMiles'
    SQUARE_MILLIMETERS = 'SquareMillimeters'
    SQUARE_CENTIMETERS = 'SquareCentimeters'
    SQUARE_DECIMETERS = 'SquareDecimeters'
    SQUARE_METERS = 'SquareMeters'
    ARES = 'Ares'
    HECTARES = 'Hectares'
    SQUARE_KILOMETERS = 'SquareKilometers'
    SQUARE_MILES_US = 'SquareMilesUS'
    ACRES_US = 'AcresUS'
    SQUARE_YARDS_US = 'SquareYardsUS'
    SQUARE_FEET_US = 'SquareFeetUS'
    SQUARE_INCHES_US = 'SquareInchesUS'
# End ArealUnitEnum class


class FieldType(StrEnum):
    """
    Field Type Enumeration
    """
    SHORT = 'Short'
    LONG = 'Long'
    FLOAT = 'Float'
    BIG_INTEGER = 'BigInteger'
    DOUBLE = 'Double'
    TEXT = 'Text'
    DATE = 'Date'
    OID = 'OID'
    TIME_ONLY = 'TimeOnly'
    DATE_ONLY = 'DateOnly'
    TIMESTAMP_OFFSET = 'TimestampOffset'
    GEOMETRY = 'Geometry'
    BLOB = 'Blob'
    RASTER = 'Raster'
    GUID = 'GUID'
    GLOBAL_ID = 'GlobalID'
    XML = 'XML'
# End FieldType class


class GeometryType(StrEnum):
    """
    Geometry Type Enumeration
    """
    POINT = 'Point'
    MULTIPOINT = 'Multipoint'
    POLYGON = 'Polygon'
    POLYLINE = 'Polyline'
    MULTIPATCH = 'MultiPatch'

    ANNOTATION = 'Annotation'
    DIMENSION = 'Dimension'
# End GeometryType class


class LinearUnit(StrEnum):
    """
    Linear Unit Enumeration
    """
    UNKNOWN = 'Unknown'
    INCHES = 'Inches'
    INCHES_INTERNATIONAL = 'InchesInt'
    POINTS = 'Points'
    FEET = 'Feet'
    FEET_INTERNATIONAL = 'FeetInt'
    YARDS = 'Yards'
    MILES = 'Miles'
    NAUTICAL_MILES = 'NauticalMiles'
    NAUTICAL_MILES_INTERNATIONAL = 'NauticalMilesInt'
    MILES_INTERNATIONAL = 'MilesInt'
    YARDS_INTERNATIONAL = 'YardsInt'
    MILLIMETERS = 'Millimeters'
    CENTIMETERS = 'Centimeters'
    METERS = 'Meters'
    KILOMETERS = 'Kilometers'
    DECIMAL_DEGREES = 'DecimalDegrees'
    DECIMETERS = 'Decimeters'
# End LinearUnit class


class SACellSize(StrEnum):
    """
    Spatial Analyst Cell Size
    """
    MAXIMUM = 'Maximum of Inputs'
    MINIMUM = 'Minimum of Inputs'
# End SACellSize class


class TimeUnit(StrEnum):
    """
    Time Unit Enumeration
    """
    UNKNOWN = 'Unknown'
    MILLISECONDS = 'Milliseconds'
    SECONDS = 'Seconds'
    MINUTES = 'Minutes'
    HOURS = 'Hours'
    DAYS = 'Days'
    WEEKS = 'Weeks'
    MONTHS = 'Months'
    YEARS = 'Years'
    DECADES = 'Decades'
    CENTURIES = 'Centuries'
# End TimeUnit class


class TravelModeUnitType(StrEnum):
    """
    Travel Mode Unit Type
    """
    TIME = 'esriNetworkTravelModeUnitsDomainTypeTime'
    DISTANCE = 'esriNetworkTravelModeUnitsDomainTypeDistance'
    OTHER = 'esriNetworkTravelModeUnitsDomainTypeOther'
# End TravelModeUnitType class


class WorkspaceType(StrEnum):
    """
    Workspace Type Enumeration
    """
    FILE_SYSTEM = 'File System'
    LOCAL_DATABASE = 'Local Database'
    REMOTE_DATABASE = 'Remote Database'
# End WorkspaceType class


RATIONAL_FIELD_TYPES: tuple[FieldType, ...] = FieldType.DOUBLE, FieldType.FLOAT
INTEGER_FIELD_TYPES: tuple[FieldType, ...] = (
    FieldType.SHORT, FieldType.LONG, FieldType.BIG_INTEGER)
NUMERIC_FIELD_TYPES: tuple[FieldType, ...] = (
    *RATIONAL_FIELD_TYPES, *INTEGER_FIELD_TYPES)
STRING_FIELD_TYPES: tuple[FieldType, ...] = FieldType.TEXT,
IDENTIFIER_FIELD_TYPES: tuple[FieldType, ...] = (
    FieldType.OID, FieldType.GUID, FieldType.GLOBAL_ID)


if __name__ == '__main__':  # pragma: no cover
    pass
