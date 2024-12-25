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
    'AnalysisCellSizeParameter', 'MapDocumentParameter', 'ArealUnitParameter',
    'BooleanParameter', 'CadDrawingDatasetParameter',
    'CalculatorExpressionParameter', 'CatalogLayerParameter',
    'SACellSizeParameter', 'CellSizeXYParameter', 'CoordinateSystemParameter',
    'CoverageParameter', 'CoverageFeatureClassParameter',
    'DataElementParameter', 'DatasetTypeParameter', 'DateParameter',
    'DbaseTableParameter', 'DoubleParameter', 'EncryptedStringParameter',
    'EnvelopeParameter', 'ExtentParameter', 'FeatureClassParameter',
    'FeatureDatasetParameter', 'FeatureLayerParameter', 'FieldParameter',
    'FileParameter', 'FolderParameter', 'GroupLayerParameter',
    'LasDatasetParameter', 'LasDatasetLayerParameter', 'GPLayerParameter',
    'LayerFileParameter', 'LinearUnitParameter', 'LongParameter',
    'MapParameter', 'MosaicDatasetParameter', 'MosaicLayerParameter',
    'NetworkDatasetParameter', 'PointParameter', 'PrjFileParameter',
    'RasterBandParameter', 'RasterCalculatorExpressionParameter',
    'RasterDataLayerParameter', 'RasterDatasetParameter',
    'RasterLayerParameter', 'RelationshipClassParameter', 'ShapeFileParameter',
    'SpatialReferenceParameter', 'SQLExpressionParameter', 'StringParameter',
    'StringHiddenParameter', 'TableParameter', 'TableViewParameter',
    'TextfileParameter', 'TinParameter', 'TinLayerParameter',
    'TopologyParameter', 'WorkspaceParameter',
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

    def serialize(self, categories: dict[str, int]) \
            -> tuple[dict[str, dict], dict[str, str]]:
        """
        Serialize Parameter to a content dictionary and a resource dictionary.
        """
        return self._serialize(categories)
    # End serialize method
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


class AnalysisCellSizeParameter(InputParameter):
    """
    The cell size used by raster tools.
    """
    keyword: ClassVar[str] = 'analysis_cell_size'
# End AnalysisCellSizeParameter class


class MapDocumentParameter(InputParameter):
    """
    A file that contains one map, its layout, and its associated layers,
    tables, charts, and reports.
    """
    keyword: ClassVar[str] = 'DEMapDocument'
# End MapDocumentParameter class


class ArealUnitParameter(InputParameter):
    """
    An areal unit type and value, such as square meter or acre.
    """
    keyword: ClassVar[str] = 'GPArealUnit'
# End ArealUnitParameter class


class BooleanParameter(InputParameter):
    """
    A Boolean value.
    """
    keyword: ClassVar[str] = 'GPBoolean'
# End BooleanParameter class


class CadDrawingDatasetParameter(InputOutputParameter):
    """
    A vector data source combined with feature types and symbology. The
    dataset cannot be used for feature class-based queries or analysis.
    """
    keyword: ClassVar[str] = 'DECadDrawingDataset'
# End CadDrawingDatasetParameter class


class CalculatorExpressionParameter(InputParameter):
    """
    A calculator expression.
    """
    keyword: ClassVar[str] = 'GPCalculatorExpression'
# End CalculatorExpressionParameter class


class CatalogLayerParameter(InputParameter):
    """
    A collection of references to different data types. The data types can
    be from different locations and are managed and visualized dynamically
    as layers based on location, time, and other attributes.
    """
    keyword: ClassVar[str] = 'GPCatalogLayer'
# End CatalogLayerParameter class


class SACellSizeParameter(InputParameter):
    """
    The cell size used by the ArcGIS Spatial Analyst extension.
    """
    keyword: ClassVar[str] = 'GPSACellSize'
# End SACellSizeParameter class


class CellSizeXYParameter(InputParameter):
    """
    The size that defines the two sides of a raster cell.
    """
    keyword: ClassVar[str] = 'GPCellSizeXY'
# End CellSizeXYParameter class


class CoordinateSystemParameter(InputOutputParameter):
    """
    A reference framework, such as the UTM system consisting of a set of
    points, lines, or surfaces, and a set of rules used to define the
    positions of points in two- and three-dimensional space.
    """
    keyword: ClassVar[str] = 'GPCoordinateSystem'
# End CoordinateSystemParameter class


class CoverageParameter(InputParameter):
    """
    A coverage dataset, a proprietary data model for storing geographic
    features as points, arcs, and polygons with associated feature
    attribute tables.
    """
    keyword: ClassVar[str] = 'DECoverage'
# End CoverageParameter class


class CoverageFeatureClassParameter(InputParameter):
    """
    A coverage feature class, such as point, arc, node, route, route
    system, section, polygon, and region.
    """
    keyword: ClassVar[str] = 'DECoverageFeatureClasses'
# End CoverageFeatureClassParameter class


class DataElementParameter(InputOutputParameter):
    """
    A dataset visible in ArcCatalog.
    """
    keyword: ClassVar[str] = 'DEType'
# End DataElementParameter class


class DatasetTypeParameter(InputParameter):
    """
    A collection of related data, usually grouped or stored together.
    """
    keyword: ClassVar[str] = 'DEDatasetType'
# End DatasetTypeParameter class


class DateParameter(InputParameter):
    """
    A date value.
    """
    keyword: ClassVar[str] = 'GPDate'
# End DateParameter class


class DbaseTableParameter(InputOutputParameter):
    """
    Attribute data stored in dBASE format.
    """
    keyword: ClassVar[str] = 'DEDbaseTable'
# End DbaseTableParameter class


class DoubleParameter(InputParameter):
    """
    Any floating-point number stored as a double precision, 64-bit value.
    """
    keyword: ClassVar[str] = 'GPDouble'
# End DoubleParameter class


class EncryptedStringParameter(InputParameter):
    """
    An encrypted string for passwords.
    """
    keyword: ClassVar[str] = 'GPEncryptedString'
# End EncryptedStringParameter class


class EnvelopeParameter(InputParameter):
    """
    The coordinate pairs that define the minimum bounding rectangle in
    which the data source resides.
    """
    keyword: ClassVar[str] = 'GPEnvelope'
# End EnvelopeParameter class


class ExtentParameter(InputParameter):
    """
    The coordinate pairs that define the minimum bounding rectangle
    (x-minimum, y-minimum and x-maximum, y-maximum) of a data source. All
    coordinates for the data source are within this boundary.
    """
    keyword: ClassVar[str] = 'GPExtent'
# End ExtentParameter class


class FeatureClassParameter(InputOutputParameter):
    """
    A collection of spatial data with the same shape type: point,
    multipoint, polyline, and polygon.
    """
    keyword: ClassVar[str] = 'DEFeatureClass'
# End FeatureClassParameter class


class FeatureDatasetParameter(InputOutputParameter):
    """
    A collection of feature classes that share a common geographic area
    and the same spatial reference system.
    """
    keyword: ClassVar[str] = 'DEFeatureDataset'
# End FeatureDatasetParameter class


class FeatureLayerParameter(InputOutputParameter):
    """
    A reference to a feature class, including symbology and rendering
    properties.
    """
    keyword: ClassVar[str] = 'GPFeatureLayer'
# End FeatureLayerParameter class


class FieldParameter(InputParameter):
    """
    A column in a table that stores the values for a single attribute.
    """
    keyword: ClassVar[str] = 'Field'
# End FieldParameter class


class FileParameter(InputOutputParameter):
    """
    A file on disk.
    """
    keyword: ClassVar[str] = 'DEFile'
# End FileParameter class


class FolderParameter(InputOutputParameter):
    """
    A location on disk where data is stored.
    """
    keyword: ClassVar[str] = 'DEFolder'
# End FolderParameter class


class GroupLayerParameter(InputOutputParameter):
    """
    A collection of layers that appear and act as a single layer. Group
    layers make it easier to organize a map, assign advanced drawing order
    options, and share layers for use in other maps.
    """
    keyword: ClassVar[str] = 'GPGroupLayer'
# End GroupLayerParameter class


class LasDatasetParameter(InputOutputParameter):
    """
    A LAS dataset stores reference to one or more LAS files on disk as
    well as to additional surface features. A LAS file is a binary file
    that stores airborne lidar data.
    """
    keyword: ClassVar[str] = 'DELasDataset'
# End LasDatasetParameter class


class LasDatasetLayerParameter(InputOutputParameter):
    """
    A layer that references a LAS dataset on disk. This layer can apply
    filters on lidar files and surface constraints referenced by a LAS
    dataset.
    """
    keyword: ClassVar[str] = 'GPLasDatasetLayer'
# End LasDatasetLayerParameter class


class GPLayerParameter(InputOutputParameter):
    """
    A reference to a data source, such as a shapefile, coverage,
    geodatabase feature class, or raster, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'GPLayer'
# End GPLayerParameter class


class LayerFileParameter(InputOutputParameter):
    """
    A layer file stores a layer definition, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'DELayer'
# End LayerFileParameter class


class LinearUnitParameter(InputParameter):
    """
    A linear unit type and value such as meter or feet.
    """
    keyword: ClassVar[str] = 'GPLinearUnit'
# End LinearUnitParameter class


class LongParameter(InputParameter):
    """
    An integer number value.
    """
    keyword: ClassVar[str] = 'GPLong'
# End LongParameter class


class MapParameter(InputOutputParameter):
    """
    An ArcGIS Pro map.
    """
    keyword: ClassVar[str] = 'GPMap'
# End MapParameter class


class MosaicDatasetParameter(InputOutputParameter):
    """
    A collection of raster and image data that allows you to store, view,
    and query the data. It is a data model in the geodatabase used to
    manage a collection of raster datasets (images) stored as a catalog
    and viewed as a mosaicked image.
    """
    keyword: ClassVar[str] = 'DEMosaicDataset'
# End MosaicDatasetParameter class


class MosaicLayerParameter(InputOutputParameter):
    """
    A layer that references a mosaic dataset.
    """
    keyword: ClassVar[str] = 'GPMosaicLayer'
# End MosaicLayerParameter class


class NetworkDatasetParameter(InputOutputParameter):
    """
    A collection of topologically connected network elements (edges,
    junctions, and turns), derived from network sources and associated
    with a collection of network attributes.
    """
    keyword: ClassVar[str] = 'DENetworkDataset'
# End NetworkDatasetParameter class


class PointParameter(InputParameter):
    """
    A pair of x,y-coordinates.
    """
    keyword: ClassVar[str] = 'GPPoint'
# End PointParameter class


class PrjFileParameter(InputOutputParameter):
    """
    A file storing coordinate system information for spatial data.
    """
    keyword: ClassVar[str] = 'DEPrjFile'
# End PrjFileParameter class


class RasterBandParameter(InputOutputParameter):
    """
    A layer in a raster dataset.
    """
    keyword: ClassVar[str] = 'DERasterBand'
# End RasterBandParameter class


class RasterCalculatorExpressionParameter(InputParameter):
    """
    A raster calculator expression.
    """
    keyword: ClassVar[str] = 'GPRasterCalculatorExpression'
# End RasterCalculatorExpressionParameter class


class RasterDataLayerParameter(InputOutputParameter):
    """
    A raster data layer.
    """
    keyword: ClassVar[str] = 'GPRasterDataLayer'
# End RasterDataLayerParameter class


class RasterDatasetParameter(InputOutputParameter):
    """
    A single dataset built from one or more rasters.
    """
    keyword: ClassVar[str] = 'DERasterDataset'
# End RasterDatasetParameter class


class RasterLayerParameter(InputOutputParameter):
    """
    A reference to a raster, including symbology and rendering properties.
    """
    keyword: ClassVar[str] = 'GPRasterLayer'
# End RasterLayerParameter class


class RelationshipClassParameter(InputOutputParameter):
    """
    The details about the relationship between objects in the geodatabase.
    """
    keyword: ClassVar[str] = 'DERelationshipClass'
# End RelationshipClassParameter class


class ShapeFileParameter(InputOutputParameter):
    """
    Spatial data in shapefile format.
    """
    keyword: ClassVar[str] = 'DEShapeFile'
# End ShapeFileParameter class


class SpatialReferenceParameter(InputParameter):
    """
    The coordinate system used to store a spatial dataset, including the
    spatial domain.
    """
    keyword: ClassVar[str] = 'GPSpatialReference'
# End SpatialReferenceParameter class


class SQLExpressionParameter(InputParameter):
    """
    A syntax for defining and manipulating data from a relational
    database.
    """
    keyword: ClassVar[str] = 'GPSQLExpression'
# End SQLExpressionParameter class


class StringParameter(InputParameter):
    """
    A text value.
    """
    keyword: ClassVar[str] = 'GPString'
# End StringParameter class


class StringHiddenParameter(InputParameter):
    """
    A string that is masked by asterisk characters.
    """
    keyword: ClassVar[str] = 'GPStringHidden'
# End StringHiddenParameter class


class TableParameter(InputOutputParameter):
    """
    Tabular data.
    """
    keyword: ClassVar[str] = 'DETable'
# End TableParameter class


class TableViewParameter(InputOutputParameter):
    """
    A representation of tabular data for viewing and editing purposes
    stored in memory or on disk.
    """
    keyword: ClassVar[str] = 'GPTableView'
# End TableViewParameter class


class TextfileParameter(InputOutputParameter):
    """
    A text file.
    """
    keyword: ClassVar[str] = 'DETextfile'
# End TextfileParameter class


class TinParameter(InputOutputParameter):
    """
    A vector data structure that partitions geographic space into
    contiguous, nonoverlapping triangles. The vertices of each triangle
    are sample data points with x-, y-, and z-values.
    """
    keyword: ClassVar[str] = 'DETin'
# End TinParameter class


class TinLayerParameter(InputOutputParameter):
    """
    A reference to a TIN, including topological relationships, symbology,
    and rendering properties.
    """
    keyword: ClassVar[str] = 'GPTinLayer'
# End TinLayerParameter class


class TopologyParameter(InputOutputParameter):
    """
    A topology that defines and enforces data integrity rules for spatial
    data.
    """
    keyword: ClassVar[str] = 'DETopology'
# End TopologyParameter class


class WorkspaceParameter(InputOutputParameter):
    """
    A container such as a geodatabase or folder.
    """
    keyword: ClassVar[str] = 'DEWorkspace'
# End WorkspaceParameter class


if __name__ == '__main__':  # pragma: no cover
    pass
