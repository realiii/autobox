# -*- coding: utf-8 -*-
"""
Parameters
"""


from typing import Any, ClassVar, NoReturn

from stoolbox.types import BOOL, STRING
from stoolbox.util import (
    make_parameter_name, validate_parameter_label,
    validate_parameter_name)


__all__ = [
    'AnalysisCellSize', 'MapDocument', 'ArealUnit', 'Boolean',
    'CadDrawingDataset', 'CalculatorExpression', 'CatalogLayer', 'SACellSize',
    'CellSizeXY', 'CoordinateSystem', 'Coverage', 'CoverageFeatureClass',
    'DataElement', 'DatasetType', 'Date', 'DbaseTable', 'Double',
    'EncryptedString', 'Envelope', 'Extent', 'FeatureClass', 'FeatureDataset',
    'FeatureLayer', 'Field', 'File', 'Folder', 'GroupLayer', 'LasDataset',
    'LasDatasetLayer', 'GPLayer', 'LayerFile', 'LinearUnit', 'Long', 'Map',
    'MosaicDataset', 'MosaicLayer', 'NetworkDataset', 'Point', 'PrjFile',
    'RasterBand', 'RasterCalculatorExpression', 'RasterDataLayer',
    'RasterDataset', 'RasterLayer', 'RelationshipClass', 'ShapeFile',
    'SpatialReference', 'SQLExpression', 'String', 'StringHidden', 'Table',
    'TableView', 'Textfile', 'Tin', 'TinLayer', 'Topology', 'Workspace',
]


class BaseParameter:
    """
    Base Parameter
    """
    def __init__(self, label: str, name: STRING = None, category: STRING = None,
                 description: STRING = None, default_value: Any = None,
                 is_input: bool = True, is_required: BOOL = True,
                 is_multi: bool = False, is_enabled: bool = True) -> None:
        """
        Initialize the BaseParameter class.

        :param label: The display name for the parameter.
        :param name: The optional name of the parameter, when not specified
            a name is generated based on the label.  Some characters are
            not allowed
        :param category: The optional parameter category, used for
            grouping parameters.
        :param description: An optional description of the parameter.
        :param default_value: Any optional default value of the parameter.
        :param is_input: Set to True for Input and False for Output.
        :param is_required: Set to True for Required, False for Optional.
        :param is_multi: Indicates if the parameter can have multiple values.
        :param is_enabled: Determines if the parameter is enabled, not used in
            parameter definition but useful for on tool validation.
        """
        super().__init__()
        self._label: str = self._validate_label(label)
        self._name: str = self._validate_name(name, self._label)
        self._category: STRING = category
        self._description: STRING = description
        self._default: Any = default_value
        self._is_input: bool = is_input
        self._is_required: bool = is_required
        self._is_multi: bool = is_multi
        self._is_enabled: bool = is_enabled
    # End init built-in

    @staticmethod
    def _validate_label(label: str) -> str | NoReturn:
        """
        Validate label
        """
        if not (validated_label := validate_parameter_label(label)):
            raise ValueError(f'Invalid parameter label: {label}')
        return validated_label
    # End _validate_label method

    @staticmethod
    def _validate_name(name: STRING, label: str) -> str:
        """
        Validate Name
        """
        if not (validated_name := validate_parameter_name(name)):
            if not (validated_name := make_parameter_name(label)):
                raise ValueError(f'Invalid parameter name: {name}')
        return validated_name
    # End _validate_name method

    @property
    def name(self) -> str:
        """
        Name
        """
        return self._name
    # End name property

    @property
    def label(self) -> str:
        """
        Label
        """
        return self._label
    # End label property

    @property
    def category(self) -> STRING:
        """
        Category
        """
        return self._category

    @category.setter
    def category(self, value: STRING) -> None:
        self._category = value
    # End category property

    @property
    def description(self) -> STRING:
        """
        Description / Documentation
        """
        return self._description

    @description.setter
    def description(self, value: STRING) -> None:
        self._description = value
    # End description property

    @property
    def default_value(self) -> Any:
        """
        Default Value
        """
        return self._default

    @default_value.setter
    def default_value(self, value: Any) -> None:
        self._default = value
    # End default_value property

    @property
    def is_input(self) -> bool:
        """
        Is Input
        """
        return self._is_input
    # End is_input property

    @property
    def is_required(self) -> BOOL:
        """
        Is Required (True), Optional (False), or Derived (None)
        """
        return self._is_required
    # End is_required property

    @property
    def is_multi(self) -> bool:
        """
        Is Multi Value
        """
        return self._is_multi
    # End is_multi property

    @property
    def is_enabled(self) -> bool:
        """
        Is Enabled
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value: bool) -> None:
        self._is_enabled = value
    # End is_enabled property
# End BaseParameter class


class InputParameter(BaseParameter):
    """
    Input Parameter
    """
    def __init__(self, label: str, name: STRING = None, category: STRING = None,
                 description: STRING = None, default_value: Any = None,
                 is_required: BOOL = True, is_multi: bool = False,
                 is_enabled: bool = True) -> None:
        """
        Initialize the InputParameter class

        :param label: The display name for the parameter.
        :param name: The optional name of the parameter, when not specified
            a name is generated based on the label.
        :param category: The optional parameter category, used for
            grouping parameters.
        :param description: An optional description of the parameter.
        :param default_value: Any optional default value of the parameter.
        :param is_required: Set to True for Required, False for Optional.
        :param is_multi: Indicates if the parameter can have multiple values.
        :param is_enabled: Determines if the parameter is enabled, not used in
            parameter definition but useful for on tool validation.
        """
        # noinspection PyArgumentEqualDefault
        super().__init__(
            label=label, name=name, category=category, description=description,
            default_value=default_value, is_input=True, is_required=is_required,
            is_multi=is_multi, is_enabled=is_enabled)
    # End init built-in
# End InputParameter class


class InputOutputParameter(BaseParameter):
    """
    Input and Output Parameter
    """
    def set_derived(self) -> None:
        """
        Set Parameter Type to Derived
        """
        self._is_input = False
        self._is_required = None
        self._is_enabled = True
    # End set_derived method
# End InputOutputParameter class


class AnalysisCellSize(InputParameter):
    """
    The cell size used by raster tools.
    """
    keyword: ClassVar[str] = 'analysis_cell_size'
# End AnalysisCellSize class


class MapDocument(InputParameter):
    """
    A file that contains one map, its layout, and its associated layers,
    tables, charts, and reports.
    """
    keyword: ClassVar[str] = 'DEMapDocument'
# End MapDocument class


class ArealUnit(InputParameter):
    """
    An areal unit type and value, such as square meter or acre.
    """
    keyword: ClassVar[str] = 'GPArealUnit'
# End ArealUnit class


class Boolean(InputParameter):
    """
    A Boolean value.
    """
    keyword: ClassVar[str] = 'GPBoolean'
# End Boolean class


class CadDrawingDataset(InputOutputParameter):
    """
    A vector data source combined with feature types and symbology. The
    dataset cannot be used for feature class-based queries or analysis.
    """
    keyword: ClassVar[str] = 'DECadDrawingDataset'
# End CadDrawingDataset class


class CalculatorExpression(InputParameter):
    """
    A calculator expression.
    """
    keyword: ClassVar[str] = 'GPCalculatorExpression'
# End CalculatorExpression class


class CatalogLayer(InputParameter):
    """
    A collection of references to different data types. The data types can
    be from different locations and are managed and visualized dynamically
    as layers based on location, time, and other attributes.
    """
    keyword: ClassVar[str] = 'GPCatalogLayer'
# End CatalogLayer class


class SACellSize(InputParameter):
    """
    The cell size used by the ArcGIS Spatial Analyst extension.
    """
    keyword: ClassVar[str] = 'GPSACellSize'
# End SACellSize class


class CellSizeXY(InputParameter):
    """
    The size that defines the two sides of a raster cell.
    """
    keyword: ClassVar[str] = 'GPCellSizeXY'
# End CellSizeXY class


class CoordinateSystem(InputOutputParameter):
    """
    A reference framework, such as the UTM system consisting of a set of
    points, lines, or surfaces, and a set of rules used to define the
    positions of points in two- and three-dimensional space.
    """
    keyword: ClassVar[str] = 'GPCoordinateSystem'
# End CoordinateSystem class


class Coverage(InputParameter):
    """
    A coverage dataset, a proprietary data model for storing geographic
    features as points, arcs, and polygons with associated feature
    attribute tables.
    """
    keyword: ClassVar[str] = 'DECoverage'
# End Coverage class


class CoverageFeatureClass(InputParameter):
    """
    A coverage feature class, such as point, arc, node, route, route
    system, section, polygon, and region.
    """
    keyword: ClassVar[str] = 'DECoverageFeatureClasses'
# End CoverageFeatureClass class


class DataElement(InputOutputParameter):
    """
    A dataset visible in ArcCatalog.
    """
    keyword: ClassVar[str] = 'DEType'
# End DataElement class


class DatasetType(InputParameter):
    """
    A collection of related data, usually grouped or stored together.
    """
    keyword: ClassVar[str] = 'DEDatasetType'
# End DatasetType class


class Date(InputParameter):
    """
    A date value.
    """
    keyword: ClassVar[str] = 'GPDate'
# End Date class


class DbaseTable(InputOutputParameter):
    """
    Attribute data stored in dBASE format.
    """
    keyword: ClassVar[str] = 'DEDbaseTable'
# End DbaseTable class


class Double(InputParameter):
    """
    Any floating-point number stored as a double precision, 64-bit value.
    """
    keyword: ClassVar[str] = 'GPDouble'
# End Double class


class EncryptedString(InputParameter):
    """
    An encrypted string for passwords.
    """
    keyword: ClassVar[str] = 'GPEncryptedString'
# End EncryptedString class


class Envelope(InputParameter):
    """
    The coordinate pairs that define the minimum bounding rectangle in
    which the data source resides.
    """
    keyword: ClassVar[str] = 'GPEnvelope'
# End Envelope class


class Extent(InputParameter):
    """
    The coordinate pairs that define the minimum bounding rectangle
    (x-minimum, y-minimum and x-maximum, y-maximum) of a data source. All
    coordinates for the data source are within this boundary.
    """
    keyword: ClassVar[str] = 'GPExtent'
# End Extent class


class FeatureClass(InputOutputParameter):
    """
    A collection of spatial data with the same shape type: point,
    multipoint, polyline, and polygon.
    """
    keyword: ClassVar[str] = 'DEFeatureClass'
# End FeatureClass class


class FeatureDataset(InputOutputParameter):
    """
    A collection of feature classes that share a common geographic area
    and the same spatial reference system.
    """
    keyword: ClassVar[str] = 'DEFeatureDataset'
# End FeatureDataset class


class FeatureLayer(InputOutputParameter):
    """
    A reference to a feature class, including symbology and rendering
    properties.
    """
    keyword: ClassVar[str] = 'GPFeatureLayer'
# End FeatureLayer class


class Field(InputParameter):
    """
    A column in a table that stores the values for a single attribute.
    """
    keyword: ClassVar[str] = 'Field'
# End Field class


class File(InputOutputParameter):
    """
    A file on disk.
    """
    keyword: ClassVar[str] = 'DEFile'
# End File class


class Folder(InputOutputParameter):
    """
    A location on disk where data is stored.
    """
    keyword: ClassVar[str] = 'DEFolder'
# End Folder class


class GroupLayer(InputOutputParameter):
    """
    A collection of layers that appear and act as a single layer. Group
    layers make it easier to organize a map, assign advanced drawing order
    options, and share layers for use in other maps.
    """
    keyword: ClassVar[str] = 'GPGroupLayer'
# End GroupLayer class


class LasDataset(InputOutputParameter):
    """
    A LAS dataset stores reference to one or more LAS files on disk as
    well as to additional surface features. A LAS file is a binary file
    that stores airborne lidar data.
    """
    keyword: ClassVar[str] = 'DELasDataset'
# End LasDataset class


class LasDatasetLayer(InputOutputParameter):
    """
    A layer that references a LAS dataset on disk. This layer can apply
    filters on lidar files and surface constraints referenced by a LAS
    dataset.
    """
    keyword: ClassVar[str] = 'GPLasDatasetLayer'
# End LasDatasetLayer class


class GPLayer(InputOutputParameter):
    """
    A reference to a data source, such as a shapefile, coverage,
    geodatabase feature class, or raster, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'GPLayer'
# End GPLayer class


class LayerFile(InputOutputParameter):
    """
    A layer file stores a layer definition, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'DELayer'
# End LayerFile class


class LinearUnit(InputParameter):
    """
    A linear unit type and value such as meter or feet.
    """
    keyword: ClassVar[str] = 'GPLinearUnit'
# End LinearUnit class


class Long(InputParameter):
    """
    An integer number value.
    """
    keyword: ClassVar[str] = 'GPLong'
# End Long class


class Map(InputOutputParameter):
    """
    An ArcGIS Pro map.
    """
    keyword: ClassVar[str] = 'GPMap'
# End Map class


class MosaicDataset(InputOutputParameter):
    """
    A collection of raster and image data that allows you to store, view,
    and query the data. It is a data model in the geodatabase used to
    manage a collection of raster datasets (images) stored as a catalog
    and viewed as a mosaicked image.
    """
    keyword: ClassVar[str] = 'DEMosaicDataset'
# End MosaicDataset class


class MosaicLayer(InputOutputParameter):
    """
    A layer that references a mosaic dataset.
    """
    keyword: ClassVar[str] = 'GPMosaicLayer'
# End MosaicLayer class


class NetworkDataset(InputOutputParameter):
    """
    A collection of topologically connected network elements (edges,
    junctions, and turns), derived from network sources and associated
    with a collection of network attributes.
    """
    keyword: ClassVar[str] = 'DENetworkDataset'
# End NetworkDataset class


class Point(InputParameter):
    """
    A pair of x,y-coordinates.
    """
    keyword: ClassVar[str] = 'GPPoint'
# End Point class


class PrjFile(InputOutputParameter):
    """
    A file storing coordinate system information for spatial data.
    """
    keyword: ClassVar[str] = 'DEPrjFile'
# End PrjFile class


class RasterBand(InputOutputParameter):
    """
    A layer in a raster dataset.
    """
    keyword: ClassVar[str] = 'DERasterBand'
# End RasterBand class


class RasterCalculatorExpression(InputParameter):
    """
    A raster calculator expression.
    """
    keyword: ClassVar[str] = 'GPRasterCalculatorExpression'
# End RasterCalculatorExpression class


class RasterDataLayer(InputOutputParameter):
    """
    A raster data layer.
    """
    keyword: ClassVar[str] = 'GPRasterDataLayer'
# End RasterDataLayer class


class RasterDataset(InputOutputParameter):
    """
    A single dataset built from one or more rasters.
    """
    keyword: ClassVar[str] = 'DERasterDataset'
# End RasterDataset class


class RasterLayer(InputOutputParameter):
    """
    A reference to a raster, including symbology and rendering properties.
    """
    keyword: ClassVar[str] = 'GPRasterLayer'
# End RasterLayer class


class RelationshipClass(InputOutputParameter):
    """
    The details about the relationship between objects in the geodatabase.
    """
    keyword: ClassVar[str] = 'DERelationshipClass'
# End RelationshipClass class


class ShapeFile(InputOutputParameter):
    """
    Spatial data in shapefile format.
    """
    keyword: ClassVar[str] = 'DEShapeFile'
# End ShapeFile class


class SpatialReference(InputParameter):
    """
    The coordinate system used to store a spatial dataset, including the
    spatial domain.
    """
    keyword: ClassVar[str] = 'GPSpatialReference'
# End SpatialReference class


class SQLExpression(InputParameter):
    """
    A syntax for defining and manipulating data from a relational
    database.
    """
    keyword: ClassVar[str] = 'GPSQLExpression'
# End SQLExpression class


class String(InputParameter):
    """
    A text value.
    """
    keyword: ClassVar[str] = 'GPString'
# End String class


class StringHidden(InputParameter):
    """
    A string that is masked by asterisk characters.
    """
    keyword: ClassVar[str] = 'GPStringHidden'
# End StringHidden class


class Table(InputOutputParameter):
    """
    Tabular data.
    """
    keyword: ClassVar[str] = 'DETable'
# End Table class


class TableView(InputOutputParameter):
    """
    A representation of tabular data for viewing and editing purposes
    stored in memory or on disk.
    """
    keyword: ClassVar[str] = 'GPTableView'
# End TableView class


class Textfile(InputOutputParameter):
    """
    A text file.
    """
    keyword: ClassVar[str] = 'DETextfile'
# End Textfile class


class Tin(InputOutputParameter):
    """
    A vector data structure that partitions geographic space into
    contiguous, nonoverlapping triangles. The vertices of each triangle
    are sample data points with x-, y-, and z-values.
    """
    keyword: ClassVar[str] = 'DETin'
# End Tin class


class TinLayer(InputOutputParameter):
    """
    A reference to a TIN, including topological relationships, symbology,
    and rendering properties.
    """
    keyword: ClassVar[str] = 'GPTinLayer'
# End TinLayer class


class Topology(InputOutputParameter):
    """
    A topology that defines and enforces data integrity rules for spatial
    data.
    """
    keyword: ClassVar[str] = 'DETopology'
# End Topology class


class Workspace(InputOutputParameter):
    """
    A container such as a geodatabase or folder.
    """
    keyword: ClassVar[str] = 'DEWorkspace'
# End Workspace class


if __name__ == '__main__':  # pragma: no cover
    pass
