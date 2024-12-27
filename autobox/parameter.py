# -*- coding: utf-8 -*-
"""
Parameters
"""


from typing import Any, ClassVar, NoReturn, Self, Type

from autobox.constant import (
    DERIVED, DOLLAR_RC, DOT, FILTER, GP_AREAL_UNIT, GP_FEATURE_SCHEMA,
    GP_LINEAR_UNIT,
    GP_MULTI_VALUE, GP_TABLE_SCHEMA, OPTIONAL, OUT, PARAMETER,
    ParameterContentKeys,
    ParameterContentResourceKeys, SEMI_COLON, SchemaContentKeys,
    ScriptToolContentKeys, ScriptToolContentResourceKeys, TRUE)
from autobox.filter import (
    AbstractFilter, ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, WorkspaceTypeFilter)
from autobox.type import BOOL, MAP_STR, STRING, TYPE_FILTERS, TYPE_PARAMS
from autobox.util import (
    make_parameter_name, validate_parameter_label, validate_parameter_name,
    wrap_markup)


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
    keyword: ClassVar[str] = ''
    dependency_types: ClassVar[TYPE_PARAMS] = ()
    filter_types: ClassVar[TYPE_FILTERS] = ()

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
        self._is_required: BOOL = is_required
        self._is_multi: bool = is_multi
        self._is_enabled: bool = is_enabled
        self._dependency: InputOutputParameter | None = None
        self._filter: AbstractFilter | None = None
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

    @staticmethod
    def _validate_type(value: Any, types: tuple[Type, ...], text: str) -> Any:
        """
        Validate Type
        """
        if value is None or not types:
            return
        if not isinstance(value, types):
            raise TypeError(f'Invalid {text} type: {value}')
        return value
    # End _validate_type method

    def _build_parameter_type(self) -> dict[str, STRING]:
        """
        Build Parameter Type
        """
        if self.is_required:
            value = None
        elif self.is_required is None:
            value = DERIVED
        else:
            value = OPTIONAL
        return {ParameterContentKeys.parameter_type: value}
    # End _build_parameter_type method

    def _build_direction(self) -> dict[str, STRING]:
        """
        Build Direction
        """
        if self.is_input:
            value = None
        else:
            value = OUT
        return {ParameterContentKeys.direction: value}
    # End _build_direction method

    def _build_display_name(self) -> tuple[MAP_STR, MAP_STR]:
        """
        Build Display Name
        """
        suffix = ScriptToolContentResourceKeys.title
        key = f'{self.name.casefold()}{DOT}{suffix}'
        content = {ParameterContentKeys.display_name: f'{DOLLAR_RC}{key}'}
        return content, {key: self.label}
    # End _build_display_name method

    def _build_category(self, categories: dict[str, int]) -> dict[str, STRING]:
        """
        Build Category
        """
        key = ParameterContentKeys.category
        if self.category not in categories:
            value = None
        else:
            id_ = categories[self.category]
            value = f'{DOLLAR_RC}{ScriptToolContentKeys.parameters}.{key}{id_}'
        return {key: value}
    # End _build_category method

    def _build_data_type(self) -> dict[str, str | MAP_STR]:
        """
        Build Data Type with Schema
        """
        key = ParameterContentKeys.data_type
        data_type = {ParameterContentKeys.type: self.keyword}
        if not self.is_multi:
            return {key: data_type}
        return {key: {
            key: data_type,
            ParameterContentKeys.type: GP_MULTI_VALUE}}
    # End _build_data_type method

    def _build_filter(self) -> tuple[dict, MAP_STR]:
        """
        Build Filter
        """
        if self.filter is None:
            return {}, {}
        return self.filter.serialize(), {}
    # End _build_filter method

    def _build_dependency(self) -> MAP_STR:
        """
        Build Dependency
        """
        if not self.dependency:
            return {}
        return {ParameterContentKeys.depends: [self.dependency.name]}
    # End _build_dependency method

    # noinspection PyMethodMayBeStatic
    def _build_schema(self) -> MAP_STR:
        """
        Build Schema
        """
        return {}
    # End _build_schema method

    def _build_default_value(self) -> dict[str, Any]:
        """
        Build Default Value
        """
        value = self.default_value
        if self.is_multi:
            if value is None:
                value = ()
            elif not isinstance(value, (list, tuple)):  # pragma: no cover
                value = value,
            value = SEMI_COLON.join(repr(v) for v in value)
        else:
            if value is not None:
                value = str(value)
        return {ParameterContentKeys.value: value}
    # End _build_default_value method

    def _build_description(self) -> tuple[MAP_STR, MAP_STR]:
        """
        Build Description
        """
        if not self.description:
            return {}, {}
        suffix = ParameterContentResourceKeys.description
        key = f'{self.name.casefold()}{DOT}{suffix}'
        content = {ParameterContentKeys.description: f'{DOLLAR_RC}{key}'}
        return content, {key: self.description}
    # End _build_description method

    def _serialize(self, categories: dict[str, int]) \
            -> tuple[dict[str, dict], MAP_STR]:
        """
        Serialize Parameter to a content dictionary and a resource dictionary.
        """
        parameter_type = self._build_parameter_type()
        direction = self._build_direction()
        display_name_content, display_name_resource = self._build_display_name()
        category = self._build_category(categories)
        data_type = self._build_data_type()
        filter_content, filter_resource = self._build_filter()
        dependency = self._build_dependency()
        schema = self._build_schema()
        default_value = self._build_default_value()
        description_content, description_resource = self._build_description()
        content = {**parameter_type, **direction, **display_name_content,
                   **category, **data_type, **filter_content, **dependency,
                   **schema, **default_value, **description_content}
        content = {k: v for k, v in content.items() if v}
        resource = {**filter_resource, **description_resource,
                    **display_name_resource}
        resource = {k: v for k, v in resource.items() if v}
        return content, resource
    # End _serialize method

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
        return wrap_markup(self._description)

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

    @property
    def dependency(self) -> Self | None:
        """
        Dependency Parameter
        """
        return self._dependency

    @dependency.setter
    def dependency(self, value: Self | None) -> None:
        self._dependency = self._validate_type(
            value, types=self.dependency_types, text=PARAMETER)
    # End dependency property

    @property
    def filter(self) -> AbstractFilter | None:
        """
        Filter Parameter
        """
        return self._filter

    @filter.setter
    def filter(self, value: AbstractFilter | None) -> None:
        self._filter = self._validate_type(
            value, types=self.filter_types, text=FILTER)
    # End dependency property

    def serialize(self, categories: dict[str, int]) \
            -> tuple[dict[str, dict], MAP_STR]:
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


class SchemaMixin:
    """
    Schema Mixin
    """
    schema_type: ClassVar[str] = ''

    def _build_schema(self) -> MAP_STR:
        """
        Build Schema
        """
        # noinspection PyUnresolvedReferences
        if self.is_input:
            return {}
        # noinspection PyUnresolvedReferences
        if self.is_required is None:  # pragma: no cover
            return {}
        return {ParameterContentKeys.schema: {
            SchemaContentKeys.type: self.schema_type,
            SchemaContentKeys.generate_output_catalog_path: TRUE}}
    # End _build_schema method
# End SchemaMixin class


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
    filter_types: ClassVar[TYPE_FILTERS] = DoubleRangeFilter, DoubleValueFilter
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


class FeatureClassParameter(SchemaMixin, InputOutputParameter):
    """
    A collection of spatial data with the same shape type: point,
    multipoint, polyline, and polygon.
    """
    keyword: ClassVar[str] = 'DEFeatureClass'
    schema_type: ClassVar[str] = GP_FEATURE_SCHEMA
    filter_types: ClassVar[TYPE_FILTERS] = FeatureClassTypeFilter,
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
    filter_types: ClassVar[TYPE_FILTERS] = FeatureClassTypeFilter,
# End FeatureLayerParameter class


class FileParameter(InputOutputParameter):
    """
    A file on disk.
    """
    keyword: ClassVar[str] = 'DEFile'
    filter_types: ClassVar[TYPE_FILTERS] = FileTypeFilter,
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


class LongParameter(InputParameter):
    """
    An integer number value.
    """
    keyword: ClassVar[str] = 'GPLong'
    filter_types: ClassVar[TYPE_FILTERS] = LongRangeFilter, LongValueFilter
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


class StringParameter(InputOutputParameter):
    """
    A text value.
    """
    keyword: ClassVar[str] = 'GPString'
    filter_types: ClassVar[TYPE_FILTERS] = StringValueFilter,

    def _build_filter(self) -> tuple[dict, MAP_STR]:
        """
        Build Filter
        """
        if self.filter is None:
            return {}, {}
        content, resource = self.filter.serialize(self.name)
        return content, resource
    # End _build_filter method
# End StringParameter class


class StringHiddenParameter(InputParameter):
    """
    A string that is masked by asterisk characters.
    """
    keyword: ClassVar[str] = 'GPStringHidden'
# End StringHiddenParameter class


class TableParameter(SchemaMixin, InputOutputParameter):
    """
    Tabular data.
    """
    keyword: ClassVar[str] = 'DETable'
    schema_type: ClassVar[str] = GP_TABLE_SCHEMA
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


_TABLE_TYPES: TYPE_PARAMS = TableParameter, TableViewParameter
_GEOGRAPHIC_TYPES: TYPE_PARAMS = (
        FeatureClassParameter, FeatureLayerParameter,
        RasterDatasetParameter, RasterLayerParameter
)


class ArealUnitParameter(InputParameter):
    """
    An areal unit type and value, such as square meter or acre.
    """
    keyword: ClassVar[str] = GP_AREAL_UNIT
    dependency_types: ClassVar[TYPE_PARAMS] = _GEOGRAPHIC_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = ArealUnitFilter,
# End ArealUnitParameter class


class FieldParameter(InputParameter):
    """
    A column in a table that stores the values for a single attribute.
    """
    keyword: ClassVar[str] = 'Field'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = FieldTypeFilter,
# End FieldParameter class


class LinearUnitParameter(InputParameter):
    """
    A linear unit type and value such as meter or feet.
    """
    keyword: ClassVar[str] = GP_LINEAR_UNIT
    dependency_types: ClassVar[TYPE_PARAMS] = _GEOGRAPHIC_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = LinearUnitFilter,
# End LinearUnitParameter class


class SQLExpressionParameter(InputParameter):
    """
    A syntax for defining and manipulating data from a relational
    database.
    """
    keyword: ClassVar[str] = 'GPSQLExpression'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
# End SQLExpressionParameter class


class WorkspaceParameter(InputOutputParameter):
    """
    A container such as a geodatabase or folder.
    """
    keyword: ClassVar[str] = 'DEWorkspace'
    filter_types: ClassVar[TYPE_FILTERS] = WorkspaceTypeFilter,
# End WorkspaceParameter class


if __name__ == '__main__':  # pragma: no cover
    pass
