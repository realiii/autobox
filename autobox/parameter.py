# -*- coding: utf-8 -*-
"""
Parameters
"""


from datetime import date, datetime, time
from pathlib import Path
from typing import Any, ClassVar, NoReturn, Self

from autobox.constant import (
    CSV, DATETIME_FORMAT, DATE_FORMAT, DBF, DERIVED, DOLLAR_RC, DOT, FILTER,
    GP_AREAL_UNIT, GP_FEATURE_SCHEMA, GP_LINEAR_UNIT, GP_MULTI_VALUE,
    GP_TABLE_SCHEMA, GP_TIME_UNIT, LYR, LYRX, MXD, OPTIONAL, OUT, PARAMETER,
    PRJ, ParameterContentKeys, ParameterContentResourceKeys, RELATIVE,
    SEMI_COLON, SHP, SchemaContentKeys, ScriptToolContentKeys,
    ScriptToolContentResourceKeys, TAB, TIME_FORMAT, TRUE, TXT)
from autobox.default import (
    ArealUnitValue, CellSizeXY, Envelope, Extent, LinearUnitValue, MDomain,
    Point, TimeUnitValue, XYDomain, ZDomain)
from autobox.enum import SACellSize
from autobox.filter import (
    AbstractFilter, ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, TimeUnitFilter,
    TravelModeUnitTypeFilter, WorkspaceTypeFilter)
from autobox.type import (
    BOOL, DATETIME, MAP_STR, NUMBER, PATH, STRING, STRINGS, TYPES, TYPE_FILTERS,
    TYPE_PARAMS)
from autobox.util import (
    make_parameter_name, quote, resolve_layer_path, unique,
    validate_parameter_label, validate_parameter_name, validate_path,
    wrap_markup)


__all__ = [
    'AnalysisCellSizeParameter', 'ArealUnitParameter', 'BooleanParameter',
    'CadDrawingDatasetParameter', 'CalculatorExpressionParameter',
    'CatalogLayerParameter', 'CellSizeXYParameter', 'CoordinateSystemParameter',
    'CoverageFeatureClassParameter', 'CoverageParameter',
    'DataElementParameter', 'DataFileParameter', 'DatasetTypeParameter',
    'DateParameter', 'DbaseTableParameter', 'DiagramLayerParameter',
    'DoubleParameter', 'EncryptedStringParameter', 'EnvelopeParameter',
    'ExtentParameter', 'FeatureClassParameter', 'FeatureDatasetParameter',
    'FeatureLayerParameter', 'FeatureRecordSetLayerParameter',
    'FieldInfoParameter', 'FieldMappingParameter', 'FieldParameter',
    'FileParameter', 'FolderParameter', 'GALayerParameter',
    'GASearchNeighborhoodParameter', 'GAValueTableParameter',
    'GPLayerParameter', 'GeodatasetTypeParameter', 'GeometricNetworkParameter',
    'GroupLayerParameter', 'KMLLayerParameter', 'LasDatasetLayerParameter',
    'LasDatasetParameter', 'LayerFileParameter', 'LinearUnitParameter',
    'LongParameter', 'MDomainParameter', 'MapDocumentParameter', 'MapParameter',
    'MosaicDatasetParameter', 'MosaicLayerParameter',
    'NAClassFieldMapParameter', 'NAHierarchySettingsParameter',
    'NALayerParameter', 'NetworkDataSourceParameter',
    'NetworkDatasetLayerParameter', 'NetworkDatasetParameter',
    'NetworkTravelModeParameter', 'PointParameter', 'PrjFileParameter',
    'RandomNumberGeneratorParameter', 'RasterBandParameter',
    'RasterBuilderParameter', 'RasterCalculatorExpressionParameter',
    'RasterDataLayerParameter', 'RasterDatasetParameter',
    'RasterLayerParameter', 'RecordSetParameter', 'RelationshipClassParameter',
    'SACellSizeParameter', 'SAExtractValuesParameter',
    'SAFuzzyFunctionParameter', 'SAGDBEnvCompressionParameter',
    'SAGDBEnvPyramidParameter', 'SAGDBEnvStatisticsParameter',
    'SAGDBEnvTileSizeParameter', 'SAHorizontalFactorParameter',
    'SANeighborhoodParameter', 'SARadiusParameter', 'SARemapParameter',
    'SASemiVariogramParameter', 'SATimeConfigurationParameter',
    'SATopoFeaturesParameter', 'SATransformationFunctionParameter',
    'SAVerticalFactorParameter', 'SAWeightedOverlayTableParameter',
    'SAWeightedSumParameter', 'SQLExpressionParameter',
    'SchematicDatasetParameter', 'SchematicDiagramClassParameter',
    'SchematicDiagramParameter', 'SchematicFolderParameter',
    'SchematicLayerParameter', 'ShapeFileParameter',
    'SpatialReferenceParameter', 'StringHiddenParameter', 'StringParameter',
    'TableParameter', 'TableViewParameter', 'TerrainLayerParameter',
    'TextfileParameter', 'TimeUnitParameter', 'TinLayerParameter',
    'TinParameter', 'TopologyLayerParameter', 'TopologyParameter',
    'ValueTableParameter', 'VectorLayerParameter', 'WorkspaceParameter',
    'XYDomainParameter', 'ZDomainParameter',
]


class BaseParameter:
    """
    Base Parameter
    """
    keyword: ClassVar[str] = ''
    dependency_types: ClassVar[TYPE_PARAMS] = ()
    filter_types: ClassVar[TYPE_FILTERS] = ()
    default_types: ClassVar[TYPES] = ()

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
        self._is_input: bool = is_input
        self._is_required: BOOL = self._validate_required(is_required)
        self._is_multi: bool = is_multi
        self._is_enabled: bool = is_enabled
        self._default: Any = self._validate_default(default_value)
        self._dependency: InputOutputParameter | None = None
        self._filter: AbstractFilter | None = None
        self._symbology: PATH = None
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

    def _validate_multi_default(self, value: Any) -> Any:
        """
        Validate Multi Default, filter elements based on type then make unique,
        return a tuple to avoid inplace modification.
        """
        if not isinstance(value, (list, tuple)):
            value = value,
        values = [v for v in value if isinstance(v, self.default_types)]
        if values:
            return tuple(unique(values))
    # End _validate_multi_default method

    def _validate_default(self, value: Any) -> Any:
        """
        Validate Default, when no default types no validation occurs.
        """
        if not self.default_types or value is None:
            return value
        if self.is_multi:
            if values := self._validate_multi_default(value):
                return values
        else:
            if isinstance(value, self.default_types):
                return value
        raise TypeError(
            f'Invalid default value for {self.__class__.__name__}: {value}')
    # End _validate_default method

    def _validate_required(self, value: BOOL) -> BOOL:
        """
        Validate Required
        """
        if not (isinstance(value, bool) or value is None):
            raise ValueError(f'Invalid is_required value: {value}')
        return value
    # End _validate_required method

    @staticmethod
    def _validate_type(value: Any, types: TYPES, text: str) -> Any:
        """
        Validate Type
        """
        if value is None or not types:
            return
        if not isinstance(value, types):
            raise TypeError(f'Invalid {text} type: {value}')
        return value
    # End _validate_type method

    def _validate_dependency(self, value: Any) -> Any:
        """
        Validate Dependency, for derived parameters allow for the same
        parameter type to be used as a dependency.  Needed in support of
        multithreaded background processing and parameter memory approach.
        """
        if self.is_derived and isinstance(value, self.__class__):
            if id(self) != id(value):
                return value
        return self._validate_type(
            value, types=self.dependency_types, text=PARAMETER)
    # End _validate_dependency method

    @staticmethod
    def _validate_layer_file(path: PATH) -> PATH:
        """
        Validate Layer File
        """
        if not path:
            return
        text = 'layer file'
        path = validate_path(path, text=text)
        if path.suffix.casefold() not in (LYRX, LYR):
            raise TypeError(f'Invalid {text} type: {path.suffix}')
        return path
    # End _validate_layer_file method

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

    def _build_symbology(self, target: Path) -> MAP_STR:
        """
        Build Symbology
        """
        if self.is_input or not target or not self.symbology:
            return {}
        if not self.symbology.is_file():  # pragma: no cover
            return {}
        path = resolve_layer_path(
            layer_file=self.symbology, toolbox_folder=target)
        if not path or path == RELATIVE:  # pragma: no cover
            return {}
        return {ParameterContentKeys.symbology: path}
    # End _build_symbology method

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
            value = self._make_flattened_value(value)
        else:
            if value is not None:
                value = str(value)
        return {ParameterContentKeys.value: value}
    # End _build_default_value method

    @staticmethod
    def _make_flattened_value(value: list | tuple) -> str:
        """
        Make Flattened Value
        """
        values = []
        for v in value:
            if isinstance(v, Path):
                func = str
            else:
                func = repr
            values.append(quote(func(v)))
        value = SEMI_COLON.join(values)
        return value
    # End _make_flattened_value method

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

    def _serialize(self, categories: dict[str, int], target: Path) \
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
        symbology = self._build_symbology(target)
        schema = self._build_schema()
        default_value = self._build_default_value()
        description_content, description_resource = self._build_description()
        content = {**parameter_type, **direction, **display_name_content,
                   **category, **data_type, **filter_content, **dependency,
                   **symbology, **schema, **default_value,
                   **description_content}
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
        self._default = self._validate_default(value)
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
    def is_derived(self) -> bool:
        """
        True if parameter is configured as derived, purposely verbose checks
        to parallel what is done in set_derived.
        """
        return (self.is_input is False and
                self.is_required is None and
                self.is_enabled is True)
    # End is_derived property

    @property
    def dependency(self) -> Self | None:
        """
        Dependency Parameter
        """
        return self._dependency

    @dependency.setter
    def dependency(self, value: Self | None) -> None:
        self._dependency = self._validate_dependency(value)
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

    @property
    def symbology(self) -> PATH:
        """
        Symbology (path to layer file)
        """
        return self._symbology

    @symbology.setter
    def symbology(self, value: PATH) -> None:
        self._symbology = self._validate_layer_file(value)
    # End symbology property

    def serialize(self, categories: dict[str, int], target: Path) \
            -> tuple[dict[str, dict], MAP_STR]:
        """
        Serialize Parameter to a content dictionary and a resource dictionary.
        """
        return self._serialize(categories, target=target)
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
        self.is_enabled = True
    # End set_derived method
# End InputOutputParameter class


class PathEsqueMixin:
    """
    Path-esque Mixin
    """
    suffixes: STRINGS = ()
    default_types: ClassVar[TYPES] = Path,

    def _validate_default(self, value: Any) -> PATH | tuple[Path, ...] | NoReturn:
        """
        Validate Default, when no default types no validation occurs.
        """
        # noinspection PyProtectedMember,PyUnresolvedReferences
        if not (value := super()._validate_default(value)):
            return value
        if not self.suffixes:
            return value
        # noinspection PyUnresolvedReferences
        if self.is_multi:
            if values := tuple(v for v in value
                               if v.suffix.casefold() in self.suffixes):
                return values
            value = tuple(v for v in value
                          if v.suffix.casefold() not in self.suffixes)
        else:
            if value.suffix.casefold() in self.suffixes:
                return value
        raise ValueError(
            f'Incorrect file extension for {self.__class__.__name__}: {value}')
    # End _validate_default method
# End PathEsqueMixin class


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


class StringNotStoredMixin:
    """
    String Not Stored Mixin
    """
    def _validate_default(self, value: str) -> None | NoReturn:
        """
        Validate Default
        """
        if value is None:
            return
        raise ValueError(
            f'Default value for {self.__class__.__name__} is not stored')
    # End _validate_default method
# End StringNotStoredMixin class


class CadDrawingDatasetParameter(InputOutputParameter):
    """
    A vector data source combined with feature types and symbology. The
    dataset cannot be used for feature class-based queries or analysis.
    """
    keyword: ClassVar[str] = 'DECadDrawingDataset'
# End CadDrawingDatasetParameter class


class CatalogLayerParameter(InputParameter):
    """
    A collection of references to different data types. The data types can
    be from different locations and are managed and visualized dynamically
    as layers based on location, time, and other attributes.
    """
    keyword: ClassVar[str] = 'GPCatalogLayer'
# End CatalogLayerParameter class


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


class DataFileParameter(InputOutputParameter):
    """
    A data file.
    """
    keyword: ClassVar[str] = 'GPDataFile'
# End DataFileParameter class


class DatasetTypeParameter(InputOutputParameter):
    """
    A collection of related data, usually grouped or stored together.
    """
    keyword: ClassVar[str] = 'DEDatasetType'
# End DatasetTypeParameter class


class DiagramLayerParameter(InputOutputParameter):
    """
    A diagram layer.
    """
    keyword: ClassVar[str] = 'GPDiagramLayer'
# End DiagramLayerParameter class


class FeatureDatasetParameter(InputOutputParameter):
    """
    A collection of feature classes that share a common geographic area
    and the same spatial reference system.
    """
    keyword: ClassVar[str] = 'DEFeatureDataset'
# End FeatureDatasetParameter class


class FieldInfoParameter(InputParameter):
    """
    The details about a field in a field map.
    """
    keyword: ClassVar[str] = 'GPFieldInfo'
# End FieldInfoParameter class


class GALayerParameter(InputOutputParameter):
    """
    A reference to a geostatistical data source, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'GPGALayer'
# End GALayerParameter class


class GASearchNeighborhoodParameter(InputParameter):
    """
    The searching neighborhood parameters for a geostatistical layer are
    defined.
    """
    keyword: ClassVar[str] = 'GPGASearchNeighborhood'
# End GASearchNeighborhoodParameter class


class GeodatasetTypeParameter(InputParameter):
    """
    A collection of data with a common theme in a geodatabase.
    """
    keyword: ClassVar[str] = 'DEGeodatasetType'
# End GeodatasetTypeParameter class


class GeometricNetworkParameter(InputOutputParameter):
    """
    A linear network represented by topologically connected edge and
    junction features. Feature connectivity is based on their geometric
    coincidence.
    """
    keyword: ClassVar[str] = 'DEGeometricNetwork'
# End GeometricNetworkParameter class


class GPLayerParameter(InputOutputParameter):
    """
    A reference to a data source, such as a shapefile, coverage,
    geodatabase feature class, or raster, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'GPLayer'
# End GPLayerParameter class


class GroupLayerParameter(InputOutputParameter):
    """
    A collection of layers that appear and act as a single layer. Group
    layers make it easier to organize a map, assign advanced drawing order
    options, and share layers for use in other maps.
    """
    keyword: ClassVar[str] = 'GPGroupLayer'
# End GroupLayerParameter class


class KMLLayerParameter(InputOutputParameter):
    """
    A KML layer.
    """
    keyword: ClassVar[str] = 'GPKMLLayer'
# End KMLLayerParameter class


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


class LayerFileParameter(InputOutputParameter):
    """
    A layer file stores a layer definition, including symbology and
    rendering properties.
    """
    keyword: ClassVar[str] = 'DELayer'
# End LayerFileParameter class


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


class NAClassFieldMapParameter(InputParameter):
    """
    Mapping between location properties in a Network Analyst layer (such
    as stops, facilities, and incidents) and a point feature class.
    """
    keyword: ClassVar[str] = 'NAClassFieldMap'
# End NAClassFieldMapParameter class


class NALayerParameter(InputOutputParameter):
    """
    A group layer used to express and solve network routing problems. Each
    sublayer held in memory in a Network Analyst layer represents some
    aspect of the routing problem and the routing solution.
    """
    keyword: ClassVar[str] = 'GPNALayer'
# End NALayerParameter class


class NetworkDatasetLayerParameter(InputOutputParameter):
    """
    A reference to a network dataset, including symbology and rendering
    properties.
    """
    keyword: ClassVar[str] = 'GPNetworkDatasetLayer'
# End NetworkDatasetLayerParameter class


class NetworkDatasetParameter(InputOutputParameter):
    """
    A collection of topologically connected network elements (edges,
    junctions, and turns), derived from network sources and associated
    with a collection of network attributes.
    """
    keyword: ClassVar[str] = 'DENetworkDataset'
# End NetworkDatasetParameter class


class NetworkDataSourceParameter(InputOutputParameter):
    """
    A network data source can be a local dataset specified either using
    its catalog path or a layer from a map, or it can be a URL to a
    portal.
    """
    keyword: ClassVar[str] = 'GPNetworkDataSource'
# End NetworkDataSourceParameter class


class RandomNumberGeneratorParameter(InputParameter):
    """
    The seed and the generator to use when creating random values.
    """
    keyword: ClassVar[str] = 'GPRandomNumberGenerator'
# End RandomNumberGeneratorParameter class


class RasterBandParameter(InputOutputParameter):
    """
    A layer in a raster dataset.
    """
    keyword: ClassVar[str] = 'DERasterBand'
# End RasterBandParameter class


class RasterBuilderParameter(InputParameter):
    """
    Raster data is added to a mosaic dataset by specifying a raster type.
    The raster type identifies metadata, such as georeferencing,
    acquisition date, and sensor type, with a raster format.
    """
    keyword: ClassVar[str] = 'GPRasterBuilder'
# End RasterBuilderParameter class


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


class SAExtractValuesParameter(InputParameter):
    """
    An extract values parameter.
    """
    keyword: ClassVar[str] = 'GPSAExtractValues'
# End SAExtractValuesParameter class


class SAFuzzyFunctionParameter(InputParameter):
    """
    The algorithm used in fuzzification of an input raster.
    """
    keyword: ClassVar[str] = 'GPSAFuzzyFunction'
# End SAFuzzyFunctionParameter class


class SAGDBEnvCompressionParameter(InputParameter):
    """
    The type of compression used for a raster.
    """
    keyword: ClassVar[str] = 'GPSAGDBEnvCompression'
# End SAGDBEnvCompressionParameter class


class SAGDBEnvPyramidParameter(InputParameter):
    """
    Specifies whether pyramids are built.
    """
    keyword: ClassVar[str] = 'GPSAGDBEnvPyramid'
# End SAGDBEnvPyramidParameter class


class SAGDBEnvStatisticsParameter(InputParameter):
    """
    Specifies whether raster statistics build.
    """
    keyword: ClassVar[str] = 'GPSAGDBEnvStatistics'
# End SAGDBEnvStatisticsParameter class


class SAGDBEnvTileSizeParameter(InputParameter):
    """
    The width and height of data stored in block.
    """
    keyword: ClassVar[str] = 'GPSAGDBEnvTileSize'
# End SAGDBEnvTileSizeParameter class


class SAHorizontalFactorParameter(InputParameter):
    """
    The relationship between the horizontal cost factor and the horizontal
    relative moving angle.
    """
    keyword: ClassVar[str] = 'GPSAHorizontalFactor'
# End SAHorizontalFactorParameter class


class SANeighborhoodParameter(InputParameter):
    """
    The shape of the area around each cell used to calculate statistics.
    """
    keyword: ClassVar[str] = 'GPSANeighborhood'
# End SANeighborhoodParameter class


class SARadiusParameter(InputParameter):
    """
    The surrounding points that are used for interpolation.
    """
    keyword: ClassVar[str] = 'GPSARadius'
# End SARadiusParameter class


class SARemapParameter(InputParameter):
    """
    A table that defines how raster cell values are reclassified.
    """
    keyword: ClassVar[str] = 'GPSARemap'
# End SARemapParameter class


class SASemiVariogramParameter(InputParameter):
    """
    The distance and direction representing two locations used to quantify
    autocorrelation.
    """
    keyword: ClassVar[str] = 'GPSASemiVariogram'
# End SASemiVariogramParameter class


class SATimeConfigurationParameter(InputParameter):
    """
    The time periods used for calculating solar radiation at specific
    locations.
    """
    keyword: ClassVar[str] = 'GPSATimeConfiguration'
# End SATimeConfigurationParameter class


class SATopoFeaturesParameter(InputParameter):
    """
    Features that are input to the interpolation.
    """
    keyword: ClassVar[str] = 'GPSATopoFeatures'
# End SATopoFeaturesParameter class


class SATransformationFunctionParameter(InputParameter):
    """
    A Spatial Analyst transformation function.
    """
    keyword: ClassVar[str] = 'GPSATransformationFunction'
# End SATransformationFunctionParameter class


class SAVerticalFactorParameter(InputParameter):
    """
    The relationship between the vertical cost factor and the vertical,
    relative moving angle.
    """
    keyword: ClassVar[str] = 'GPSAVerticalFactor'
# End SAVerticalFactorParameter class


class SAWeightedOverlayTableParameter(InputParameter):
    """
    A table with data to combine multiple rasters by applying a common
    measurement scale of values to each raster, weighing each according to
    its importance.
    """
    keyword: ClassVar[str] = 'GPSAWeightedOverlayTable'
# End SAWeightedOverlayTableParameter class


class SAWeightedSumParameter(InputParameter):
    """
    Data for overlaying several rasters, each multiplied by their given
    weight and summed.
    """
    keyword: ClassVar[str] = 'GPSAWeightedSum'
# End SAWeightedSumParameter class


class SchematicDatasetParameter(InputOutputParameter):
    """
    A collection of schematic diagram templates and schematic feature
    classes that share the same application domain, for example, water or
    electrical.
    """
    keyword: ClassVar[str] = 'DESchematicDataset'
# End SchematicDatasetParameter class


class SchematicDiagramParameter(InputOutputParameter):
    """
    A schematic diagram.
    """
    keyword: ClassVar[str] = 'DESchematicDiagram'
# End SchematicDiagramParameter class


class SchematicDiagramClassParameter(InputOutputParameter):
    """
    A schematic diagram class.
    """
    keyword: ClassVar[str] = 'DESchematicDiagramClass'
# End SchematicDiagramClassParameter class


class SchematicFolderParameter(InputOutputParameter):
    """
    A schematic folder.
    """
    keyword: ClassVar[str] = 'DESchematicFolder'
# End SchematicFolderParameter class


class SchematicLayerParameter(InputOutputParameter):
    """
    A composite layer composed of feature layers based on the schematic
    feature classes associated with the template on which the schematic
    diagram is based.
    """
    keyword: ClassVar[str] = 'GPSchematicLayer'
# End SchematicLayerParameter class


class TableViewParameter(InputOutputParameter):
    """
    A representation of tabular data for viewing and editing purposes
    stored in memory or on disk.
    """
    keyword: ClassVar[str] = 'GPTableView'
# End TableViewParameter class


class TerrainLayerParameter(InputOutputParameter):
    """
    A reference to a terrain, including symbology and rendering
    properties. It’s used to draw a terrain.
    """
    keyword: ClassVar[str] = 'GPTerrainLayer'
# End TerrainLayerParameter class


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


class TopologyLayerParameter(InputOutputParameter):
    """
    A reference to a topology, including symbology and rendering
    properties.
    """
    keyword: ClassVar[str] = 'GPTopologyLayer'
# End TopologyLayerParameter class


class TopologyParameter(InputOutputParameter):
    """
    A topology that defines and enforces data integrity rules for spatial
    data.
    """
    keyword: ClassVar[str] = 'DETopology'
# End TopologyParameter class


class ValueTableParameter(InputParameter):
    """
    A collection of columns of values.
    """
    keyword: ClassVar[str] = 'GPValueTable'
# End ValueTableParameter class


class VectorLayerParameter(InputOutputParameter):
    """
    A vector tile layer.
    """
    keyword: ClassVar[str] = 'GPVectorLayer'
# End VectorLayerParameter class


class FeatureClassParameter(SchemaMixin, InputOutputParameter):
    """
    A collection of spatial data with the same shape type: point,
    multipoint, polyline, and polygon.
    """
    keyword: ClassVar[str] = 'DEFeatureClass'
    schema_type: ClassVar[str] = GP_FEATURE_SCHEMA
    filter_types: ClassVar[TYPE_FILTERS] = FeatureClassTypeFilter,
# End FeatureClassParameter class


class FeatureLayerParameter(InputOutputParameter):
    """
    A reference to a feature class, including symbology and rendering
    properties.
    """
    keyword: ClassVar[str] = 'GPFeatureLayer'
    filter_types: ClassVar[TYPE_FILTERS] = FeatureClassTypeFilter,
# End FeatureLayerParameter class


class FeatureRecordSetLayerParameter(InputParameter):
    """
    Interactive features that draw the features when the tool is run.
    """
    keyword: ClassVar[str] = 'GPFeatureRecordSetLayer'
# End FeatureRecordSetLayerParameter class


class RecordSetParameter(InputParameter):
    """
    An interactive table. Type the table values when the tool is run.
    """
    keyword: ClassVar[str] = 'GPRecordSet'
# End RecordSetParameter class


class TableParameter(SchemaMixin, InputOutputParameter):
    """
    Tabular data.
    """
    keyword: ClassVar[str] = 'DETable'
    schema_type: ClassVar[str] = GP_TABLE_SCHEMA
# End TableParameter class


_TABLE_TYPES: TYPE_PARAMS = (
    TableParameter, TableViewParameter, RecordSetParameter)
_GEOGRAPHIC_TYPES: TYPE_PARAMS = (
    FeatureClassParameter, FeatureLayerParameter,
    FeatureRecordSetLayerParameter,
    RasterDatasetParameter, RasterLayerParameter, DatasetTypeParameter
)


class AnalysisCellSizeParameter(InputParameter):
    """
    The cell size used by raster tools.
    """
    keyword: ClassVar[str] = 'analysis_cell_size'
    default_types: ClassVar[TYPES] = Path, int, float

    def _validate_default(self, value: Any) -> Path | NUMBER | None:
        """
        Validate Default, when no default types no validation occurs.
        """
        value = super()._validate_default(value)
        if isinstance(value, Path) or value is None:
            return value
        if isinstance(value, (float, int)) and value > 0:
            return value
        raise ValueError(f'Default value for {self.__class__.__name__} '
                         f'must be greater than 0: {value}')
    # End _validate_default method
# End AnalysisCellSizeParameter class


class ArealUnitParameter(InputParameter):
    """
    An areal unit type and value, such as square meter or acre.
    """
    keyword: ClassVar[str] = GP_AREAL_UNIT
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = ArealUnitFilter,
    default_types: ClassVar[TYPES] = ArealUnitValue,
# End ArealUnitParameter class


class BooleanParameter(InputOutputParameter):
    """
    A Boolean value.
    """
    keyword: ClassVar[str] = 'GPBoolean'
    default_types: ClassVar[TYPES] = bool,

    def __init__(self, label: str, name: STRING = None, category: STRING = None,
                 description: STRING = None, default_value: BOOL = True,
                 is_input: bool = True, is_required: BOOL = True,
                 is_multi: bool = False, is_enabled: bool = True) -> None:
        """
        Initialize the BooleanParameter class.
        """
        super().__init__(
            label=label, name=name, category=category, description=description,
            default_value=default_value, is_input=is_input,
            is_required=is_required, is_multi=is_multi, is_enabled=is_enabled)
    # End init built-in

    def _build_default_value(self) -> dict[str, Any]:
        """
        Build Default Value, stored as string version of lowercase.
        """
        value = self.default_value
        if value is not None:
            value = str(value).casefold()
        return {ParameterContentKeys.value: value}
    # End _build_default_value method

    def _validate_required(self, value: BOOL) -> BOOL:
        """
        Validate Required, disallow optional Boolean parameters
        """
        if value not in (True, None):
            raise ValueError(f'Invalid is_required value: {value}, can only '
                             f'be True (Required) or None (Derived)')
        return value
    # End _validate_required method

    def _validate_default(self, value: Any) -> bool | NoReturn:
        """
        Validate Default, specialization since None is considered invalid
        """
        if isinstance(value, bool):
            return value
        raise TypeError(
            f'Invalid default value for {self.__class__.__name__}: {value}')
    # End _validate_default method
# End BooleanParameter class


class CalculatorExpressionParameter(InputParameter):
    """
    A calculator expression.
    """
    keyword: ClassVar[str] = 'GPCalculatorExpression'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    default_types: ClassVar[TYPES] = str,
# End CalculatorExpressionParameter class


class CellSizeXYParameter(InputParameter):
    """
    The size that defines the two sides of a raster cell.
    """
    keyword: ClassVar[str] = 'GPCellSizeXY'
    default_types: ClassVar[TYPES] = CellSizeXY,
# End CellSizeXYParameter class


class CoordinateSystemParameter(InputOutputParameter):
    """
    A reference framework, such as the UTM system consisting of a set of
    points, lines, or surfaces, and a set of rules used to define the
    positions of points in two- and three-dimensional space.
    """
    keyword: ClassVar[str] = 'GPCoordinateSystem'
    default_types: ClassVar[TYPES] = str,
# End CoordinateSystemParameter class


class DateParameter(InputOutputParameter):
    """
    A date value.
    """
    keyword: ClassVar[str] = 'GPDate'
    default_types: ClassVar[TYPES] = datetime, date, time

    @staticmethod
    def _as_string(value: DATETIME) -> str:
        """
        Value as String
        """
        if isinstance(value, datetime):
            fmt = DATETIME_FORMAT
        elif isinstance(value, date):
            fmt = DATE_FORMAT
        else:
            fmt = TIME_FORMAT
        return value.strftime(fmt)
    # End _as_string method

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
            value = SEMI_COLON.join(quote(self._as_string(v)) for v in value)
        else:
            if value is not None:
                value = self._as_string(value)
        return {ParameterContentKeys.value: value}
    # End _build_default_value method
# End DateParameter class


class DbaseTableParameter(PathEsqueMixin, InputOutputParameter):
    """
    Attribute data stored in dBASE format.
    """
    keyword: ClassVar[str] = 'DEDbaseTable'
    suffixes: STRINGS = DBF, SHP
# End DbaseTableParameter class


class DoubleParameter(InputOutputParameter):
    """
    Any floating-point number stored as a double precision, 64-bit value.
    """
    keyword: ClassVar[str] = 'GPDouble'
    filter_types: ClassVar[TYPE_FILTERS] = DoubleRangeFilter, DoubleValueFilter
    default_types: ClassVar[TYPES] = float, int
# End DoubleParameter class


class EncryptedStringParameter(StringNotStoredMixin, InputParameter):
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
    default_types: ClassVar[TYPES] = Envelope,
# End EnvelopeParameter class


class ExtentParameter(InputParameter):
    """
    The coordinate pairs that define the minimum bounding rectangle
    (x-minimum, y-minimum and x-maximum, y-maximum) of a data source. All
    coordinates for the data source are within this boundary.
    """
    keyword: ClassVar[str] = 'GPExtent'
    default_types: ClassVar[TYPES] = Extent,
# End ExtentParameter class


class FieldMappingParameter(InputParameter):
    """
    A collection of fields in one or more input tables.
    """
    keyword: ClassVar[str] = 'GPFieldMapping'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
# End FieldMappingParameter class


class FieldParameter(InputParameter):
    """
    A column in a table that stores the values for a single attribute.
    """
    keyword: ClassVar[str] = 'Field'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = FieldTypeFilter,
# End FieldParameter class


class FileParameter(PathEsqueMixin, InputOutputParameter):
    """
    A file on disk.
    """
    keyword: ClassVar[str] = 'DEFile'
    filter_types: ClassVar[TYPE_FILTERS] = FileTypeFilter,
# End FileParameter class


class FolderParameter(PathEsqueMixin, InputOutputParameter):
    """
    A location on disk where data is stored.
    """
    keyword: ClassVar[str] = 'DEFolder'
# End FolderParameter class


class GAValueTableParameter(InputParameter):
    """
    A collection of data sources and fields that define a geostatistical
    layer.
    """
    keyword: ClassVar[str] = 'GPGAValueTable'
    dependency_types: ClassVar[TYPE_PARAMS] = GALayerParameter,
# End GAValueTableParameter class


class LinearUnitParameter(InputParameter):
    """
    A linear unit type and value such as meter or feet.
    """
    keyword: ClassVar[str] = GP_LINEAR_UNIT
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    filter_types: ClassVar[TYPE_FILTERS] = LinearUnitFilter,
    default_types: ClassVar[TYPES] = LinearUnitValue,
# End LinearUnitParameter class


class LongParameter(InputOutputParameter):
    """
    An integer number value.
    """
    keyword: ClassVar[str] = 'GPLong'
    filter_types: ClassVar[TYPE_FILTERS] = LongRangeFilter, LongValueFilter
    default_types: ClassVar[TYPES] = int,
# End LongParameter class


class MapDocumentParameter(PathEsqueMixin, InputParameter):
    """
    A file that contains one map, its layout, and its associated layers,
    tables, charts, and reports.
    """
    keyword: ClassVar[str] = 'DEMapDocument'
    suffixes: STRING = MXD,
# End MapDocumentParameter class


class MDomainParameter(InputParameter):
    """
    A range of lowest and highest possible value for m-coordinates.
    """
    keyword: ClassVar[str] = 'GPMDomain'
    default_types: ClassVar[TYPES] = MDomain,
# End MDomainParameter class


class NAHierarchySettingsParameter(InputParameter):
    """
    A hierarchy attribute that divides hierarchy values of a network
    dataset into three groups using two integers. The first integer sets
    the ending value of the first group; the second number sets the
    beginning value of the third group.
    """
    keyword: ClassVar[str] = 'GPNAHierarchySettings'
    dependency_types: ClassVar[TYPE_PARAMS] = NetworkDatasetParameter,
# End NAHierarchySettingsParameter class


class NetworkTravelModeParameter(InputParameter):
    """
    A dictionary of travel mode objects.
    """
    keyword: ClassVar[str] = 'NetworkTravelMode'
    dependency_types: ClassVar[TYPE_PARAMS] = (
        NetworkDatasetParameter, NetworkDatasetLayerParameter,
        NetworkDataSourceParameter)
    filter_types: ClassVar[TYPE_FILTERS] = TravelModeUnitTypeFilter,
# End NetworkTravelModeParameter class


class PointParameter(InputParameter):
    """
    A pair of x,y-coordinates.
    """
    keyword: ClassVar[str] = 'GPPoint'
    default_types: ClassVar[TYPES] = Point,
# End PointParameter class


class PrjFileParameter(PathEsqueMixin, InputOutputParameter):
    """
    A file storing coordinate system information for spatial data.
    """
    keyword: ClassVar[str] = 'DEPrjFile'
    suffixes: STRINGS = PRJ,
# End PrjFileParameter class


class SACellSizeParameter(InputParameter):
    """
    The cell size used by the ArcGIS Spatial Analyst extension.
    """
    keyword: ClassVar[str] = 'GPSACellSize'
    default_types: ClassVar[TYPES] = Path, SACellSize
# End SACellSizeParameter class


class SpatialReferenceParameter(InputOutputParameter):
    """
    The coordinate system used to store a spatial dataset, including the
    spatial domain.
    """
    keyword: ClassVar[str] = 'GPSpatialReference'
    default_types: ClassVar[TYPES] = str,
# End SpatialReferenceParameter class


class ShapeFileParameter(PathEsqueMixin, InputOutputParameter):
    """
    Spatial data in shapefile format.
    """
    keyword: ClassVar[str] = 'DEShapeFile'
    suffixes: STRINGS = SHP,
# End ShapeFileParameter class


class SQLExpressionParameter(InputParameter):
    """
    A syntax for defining and manipulating data from a relational
    database.
    """
    keyword: ClassVar[str] = 'GPSQLExpression'
    dependency_types: ClassVar[TYPE_PARAMS] = *_GEOGRAPHIC_TYPES, *_TABLE_TYPES
    default_types: ClassVar[TYPES] = str,
# End SQLExpressionParameter class


class StringParameter(InputOutputParameter):
    """
    A text value.
    """
    keyword: ClassVar[str] = 'GPString'
    filter_types: ClassVar[TYPE_FILTERS] = StringValueFilter,
    default_types: ClassVar[TYPES] = str,

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


class StringHiddenParameter(StringNotStoredMixin, InputParameter):
    """
    A string that is masked by asterisk characters.
    """
    keyword: ClassVar[str] = 'GPStringHidden'
# End StringHiddenParameter class


class TextfileParameter(PathEsqueMixin, InputOutputParameter):
    """
    A text file.
    """
    keyword: ClassVar[str] = 'DETextfile'
    suffixes: STRINGS = CSV, TXT, TAB
# End TextfileParameter class


class TimeUnitParameter(InputParameter):
    """
    A time unit type and value such as minutes or hours.
    """
    keyword: ClassVar[str] = GP_TIME_UNIT
    filter_types: ClassVar[TYPE_FILTERS] = TimeUnitFilter,
    default_types: ClassVar[TYPES] = TimeUnitValue,
# End TimeUnitParameter class


class WorkspaceParameter(InputOutputParameter):
    """
    A container such as a geodatabase or folder.
    """
    keyword: ClassVar[str] = 'DEWorkspace'
    filter_types: ClassVar[TYPE_FILTERS] = WorkspaceTypeFilter,
# End WorkspaceParameter class


class XYDomainParameter(InputParameter):
    """
    A range of lowest and highest possible values for x,y-coordinates.
    """
    keyword: ClassVar[str] = 'GPXYDomain'
    default_types: ClassVar[TYPES] = XYDomain,
# End XYDomainParameter class


class ZDomainParameter(InputParameter):
    """
    A range of lowest and highest possible values for z-coordinates.
    """
    keyword: ClassVar[str] = 'GPZDomain'
    default_types: ClassVar[TYPES] = ZDomain,
# End ZDomainParameter class


if __name__ == '__main__':  # pragma: no cover
    pass
