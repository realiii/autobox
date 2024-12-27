# -*- coding: utf-8 -*-
"""
Enumerations for Filters
"""


from enum import StrEnum


__all__ = [
    'ArealUnit', 'FieldType', 'GeometryType', 'LinearUnit', 'WorkspaceType'
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


class WorkspaceType(StrEnum):
    """
    Workspace Type Enumeration
    """
    FILE_SYSTEM = 'File System'
    LOCAL_DATABASE = 'Local Database'
    REMOTE_DATABASE = 'Remote Database'
# End WorkspaceType class


if __name__ == '__main__':  # pragma: no cover
    pass
