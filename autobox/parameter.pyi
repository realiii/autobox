# -*- coding: utf-8 -*-
"""
Parameter Stubs
"""


from pathlib import Path
from typing import Any, ClassVar, NoReturn, Self, Type, TypeAlias

from autobox.filter import (
    AbstractFilter, ArealUnitFilter, DoubleRangeFilter, DoubleValueFilter,
    FeatureClassTypeFilter, FieldTypeFilter, FileTypeFilter, LinearUnitFilter,
    LongRangeFilter, LongValueFilter, StringValueFilter, TimeUnitFilter,
    TravelModeUnitTypeFilter, WorkspaceTypeFilter)
from autobox.type import BOOL, MAP_STR, PATH, STRING, TYPE_FILTERS, TYPE_PARAMS


class BaseParameter:
    """
    Base Parameter
    """
    keyword: ClassVar[str]
    dependency_types: ClassVar[TYPE_PARAMS]
    filter_types: ClassVar[TYPE_FILTERS]

    _label: str
    _name: str
    _category: STRING
    _description: STRING
    _default: Any
    _is_input: bool
    _is_required: BOOL
    _is_multi: bool
    _is_enabled: bool
    _dependency: InputOutputParameter | None
    _filter: AbstractFilter | None
    _symbology: PATH

    def __init__(self, label: str, name: STRING = None, category: STRING = None,
                 description: STRING = None, default_value: Any = None,
                 is_input: bool = True, is_required: BOOL = True,
                 is_multi: bool = False, is_enabled: bool = True) -> None: ...
    @staticmethod
    def _validate_label(label: str) -> str | NoReturn: ...
    @staticmethod
    def _validate_name(name: STRING, label: str) -> str: ...
    @staticmethod
    def _validate_type(value: Any, types: tuple[Type, ...], text: str) -> Any: ...
    def _validate_dependency(self, value: Any) -> Any: ...
    @staticmethod
    def _validate_layer_file(path: PATH) -> PATH: ...
    def _build_parameter_type(self) -> dict[str, STRING]: ...
    def _build_direction(self) -> dict[str, STRING]: ...
    def _build_display_name(self) -> tuple[MAP_STR, MAP_STR]: ...
    def _build_category(self, categories: dict[str, int]) -> dict[str, STRING]: ...
    def _build_data_type(self) -> dict[str, str | MAP_STR]: ...
    def _build_filter(self) -> tuple[dict, MAP_STR]: ...
    def _build_dependency(self) -> MAP_STR: ...
    def _build_schema(self) -> MAP_STR: ...
    def _build_symbology(self, target: PATH) -> MAP_STR: ...
    def _build_default_value(self) -> dict[str, Any]: ...
    def _build_description(self) -> tuple[MAP_STR, MAP_STR]: ...
    def _serialize(self, categories: dict[str, int], target: Path) -> tuple[dict[str, dict], MAP_STR]: ...
    @property
    def name(self) -> str: ...
    @property
    def label(self) -> str: ...
    @property
    def category(self) -> STRING: ...
    # noinspection PyUnresolvedReferences
    @category.setter
    def category(self, value: STRING) -> None: ...
    @property
    def description(self) -> STRING: ...
    # noinspection PyUnresolvedReferences
    @description.setter
    def description(self, value: STRING) -> None: ...
    @property
    def default_value(self) -> Any: ...
    # noinspection PyUnresolvedReferences
    @default_value.setter
    def default_value(self, value: Any) -> None: ...
    @property
    def is_input(self) -> bool: ...
    @property
    def is_required(self) -> BOOL: ...
    @property
    def is_multi(self) -> bool: ...
    @property
    def is_enabled(self) -> bool: ...
    # noinspection PyUnresolvedReferences
    @is_enabled.setter
    def is_enabled(self, value: bool) -> None: ...
    @property
    def is_derived(self) -> bool: ...
    @property
    def dependency(self) -> Self | None: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: Self | None) -> None: ...
    @property
    def filter(self) -> AbstractFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: AbstractFilter | None) -> None: ...
    @property
    def symbology(self) -> PATH: ...
    # noinspection PyUnresolvedReferences
    @symbology.setter
    def symbology(self, value: PATH) -> None: ...
    def serialize(self, categories: dict[str, int], target: Path) -> tuple[dict[str, dict], MAP_STR]: ...
# End BaseParameter class



class InputParameter(BaseParameter):
    """
    Input Parameter
    """
    def __init__(self, label: str, name: STRING = None, category: STRING = None,
                 description: STRING = None, default_value: Any = None,
                 is_required: BOOL = True, is_multi: bool = False,
                 is_enabled: bool = True) -> None: ...
# End InputParameter class


class InputOutputParameter(BaseParameter):
    """
    Input and Output Parameter
    """
    def set_derived(self) -> None: ...
# End InputOutputParameter class


class SchemaMixin:
    """
    Schema Mixin
    """
    schema_type: ClassVar[str]

    def _build_schema(self) -> MAP_STR: ...
# End SchemaMixin class


class AnalysisCellSizeParameter(InputParameter): ...
class BooleanParameter(InputOutputParameter): ...
class CadDrawingDatasetParameter(InputOutputParameter): ...
class CalculatorExpressionParameter(InputParameter): ...
class CatalogLayerParameter(InputParameter): ...
class CellSizeXYParameter(InputParameter): ...
class CoordinateSystemParameter(InputOutputParameter): ...
class CoverageFeatureClassParameter(InputParameter): ...
class CoverageParameter(InputParameter): ...
class DataElementParameter(InputOutputParameter): ...
class DataFileParameter(InputOutputParameter): ...
class DatasetTypeParameter(InputOutputParameter): ...
class DateParameter(InputOutputParameter): ...
class DbaseTableParameter(InputOutputParameter): ...
class DiagramLayerParameter(InputOutputParameter): ...
class EncryptedStringParameter(InputParameter): ...
class EnvelopeParameter(InputParameter): ...
class ExtentParameter(InputParameter): ...
class FeatureDatasetParameter(InputOutputParameter): ...
class FieldInfoParameter(InputParameter): ...
class FolderParameter(InputOutputParameter): ...
class GALayerParameter(InputOutputParameter): ...
class GASearchNeighborhoodParameter(InputParameter): ...
class GPLayerParameter(InputOutputParameter): ...
class GeodatasetTypeParameter(InputParameter): ...
class GeometricNetworkParameter(InputOutputParameter): ...
class GroupLayerParameter(InputOutputParameter): ...
class KMLLayerParameter(InputOutputParameter): ...
class LasDatasetLayerParameter(InputOutputParameter): ...
class LasDatasetParameter(InputOutputParameter): ...
class LayerFileParameter(InputOutputParameter): ...
class MDomainParameter(InputParameter): ...
class MapDocumentParameter(InputParameter): ...
class MapParameter(InputOutputParameter): ...
class MosaicDatasetParameter(InputOutputParameter): ...
class MosaicLayerParameter(InputOutputParameter): ...
class NAClassFieldMapParameter(InputParameter): ...
class NALayerParameter(InputOutputParameter): ...
class NetworkDatasetLayerParameter(InputOutputParameter): ...
class NetworkDatasetParameter(InputOutputParameter): ...
class NetworkDataSourceParameter(InputOutputParameter): ...
class PointParameter(InputParameter): ...
class PrjFileParameter(InputOutputParameter): ...
class RandomNumberGeneratorParameter(InputParameter): ...
class RasterBandParameter(InputOutputParameter): ...
class RasterBuilderParameter(InputParameter): ...
class RasterCalculatorExpressionParameter(InputParameter): ...
class RasterDataLayerParameter(InputOutputParameter): ...
class RasterDatasetParameter(InputOutputParameter): ...
class RasterLayerParameter(InputOutputParameter): ...
class RelationshipClassParameter(InputOutputParameter): ...
class SACellSizeParameter(InputParameter): ...
class SAExtractValuesParameter(InputParameter): ...
class SAFuzzyFunctionParameter(InputParameter): ...
class SAGDBEnvCompressionParameter(InputParameter): ...
class SAGDBEnvPyramidParameter(InputParameter): ...
class SAGDBEnvStatisticsParameter(InputParameter): ...
class SAGDBEnvTileSizeParameter(InputParameter): ...
class SAHorizontalFactorParameter(InputParameter): ...
class SANeighborhoodParameter(InputParameter): ...
class SARadiusParameter(InputParameter): ...
class SARemapParameter(InputParameter): ...
class SASemiVariogramParameter(InputParameter): ...
class SATimeConfigurationParameter(InputParameter): ...
class SATopoFeaturesParameter(InputParameter): ...
class SATransformationFunctionParameter(InputParameter): ...
class SAVerticalFactorParameter(InputParameter): ...
class SAWeightedOverlayTableParameter(InputParameter): ...
class SAWeightedSumParameter(InputParameter): ...
class SchematicDatasetParameter(InputOutputParameter): ...
class SchematicDiagramClassParameter(InputOutputParameter): ...
class SchematicDiagramParameter(InputOutputParameter): ...
class SchematicFolderParameter(InputOutputParameter): ...
class SchematicLayerParameter(InputOutputParameter): ...
class ShapeFileParameter(InputOutputParameter): ...
class SpatialReferenceParameter(InputOutputParameter): ...
class StringHiddenParameter(InputParameter): ...
class TableViewParameter(InputOutputParameter): ...
class TerrainLayerParameter(InputOutputParameter): ...
class TextfileParameter(InputOutputParameter): ...
class TinLayerParameter(InputOutputParameter): ...
class TinParameter(InputOutputParameter): ...
class TopologyLayerParameter(InputOutputParameter): ...
class TopologyParameter(InputOutputParameter): ...
class ValueTableParameter(InputParameter): ...
class VectorLayerParameter(InputOutputParameter): ...
class XYDomainParameter(InputParameter): ...
class ZDomainParameter(InputParameter): ...


class FeatureClassParameter(SchemaMixin, InputOutputParameter):
    """
    A collection of spatial data with the same shape type: point,
    multipoint, polyline, and polygon.
    """
    @property
    def filter(self) -> FeatureClassTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: FeatureClassTypeFilter | None) -> None: ...
# End FeatureClassParameter class


class FeatureLayerParameter(InputOutputParameter):
    """
    A reference to a feature class, including symbology and rendering
    properties.
    """
    @property
    def filter(self) -> FeatureClassTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: FeatureClassTypeFilter | None) -> None: ...
# End FeatureLayerParameter class


class FeatureRecordSetLayerParameter(InputParameter): ...
class RecordSetParameter(InputParameter): ...


class TableParameter(SchemaMixin, InputOutputParameter): ...


_GEOG_TYPES: TypeAlias = (
        FeatureClassParameter | FeatureLayerParameter |
        FeatureRecordSetLayerParameter |
        RasterDatasetParameter | RasterLayerParameter | None
)
_TABLE_AND_GEOGRAPHIC_TYPES: TypeAlias = (
    TableParameter | TableViewParameter | RecordSetParameter |
    FeatureClassParameter | FeatureLayerParameter |
    FeatureRecordSetLayerParameter |
    RasterDatasetParameter | RasterLayerParameter | None
)
_NETWORK_TYPES: TypeAlias = (
    NetworkDatasetParameter | NetworkDatasetLayerParameter |
    NetworkDataSourceParameter | None
)


class ArealUnitParameter(InputParameter):
    """
    An areal unit type and value, such as square meter or acre.
    """
    @property
    def dependency(self) -> _TABLE_AND_GEOGRAPHIC_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _TABLE_AND_GEOGRAPHIC_TYPES) -> None: ...
    def filter(self) -> ArealUnitFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: ArealUnitFilter | None) -> None: ...
# End ArealUnitParameter class


class DoubleParameter(InputOutputParameter):
    """
    Any floating-point number stored as a double precision, 64-bit value.
    """
    @property
    def filter(self) -> DoubleRangeFilter | DoubleValueFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: DoubleRangeFilter | DoubleValueFilter | None) -> None: ...
# End DoubleParameter class


class FieldMappingParameter(InputParameter):
    """
    A collection of fields in one or more input tables.
    """
    @property
    def dependency(self) -> _TABLE_AND_GEOGRAPHIC_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _TABLE_AND_GEOGRAPHIC_TYPES) -> None: ...
# End FieldMappingParameter class


class FieldParameter(InputParameter):
    """
    A column in a table that stores the values for a single attribute.
    """
    @property
    def dependency(self) -> _TABLE_AND_GEOGRAPHIC_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _TABLE_AND_GEOGRAPHIC_TYPES) -> None: ...
    def filter(self) -> FieldTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: FieldTypeFilter | None) -> None: ...
# End FieldParameter class


class FileParameter(InputOutputParameter):
    """
    A file on disk.
    """
    @property
    def filter(self) -> FileTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: FileTypeFilter | None) -> None: ...
# End FileParameter class


class GAValueTableParameter(InputParameter):
    """
    A collection of data sources and fields that define a geostatistical
    layer.
    """
    @property
    def dependency(self) -> GALayerParameter | None: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: GALayerParameter | None) -> None: ...
# End GAValueTableParameter class


class LinearUnitParameter(InputParameter):
    """
    A linear unit type and value such as meter or feet.
    """
    @property
    def dependency(self) -> _TABLE_AND_GEOGRAPHIC_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _TABLE_AND_GEOGRAPHIC_TYPES) -> None: ...
    @property
    def filter(self) -> LinearUnitFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: LinearUnitFilter | None) -> None: ...
# End LinearUnitParameter class


class LongParameter(InputOutputParameter):
    """
    An integer number value.
    """
    @property
    def filter(self) -> LongRangeFilter | LongValueFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: LongRangeFilter | LongValueFilter | None) -> None: ...
# End LongParameter class


class NetworkTravelModeParameter(InputParameter):
    """
    A dictionary of travel mode objects.
    """
    @property
    def dependency(self) -> _NETWORK_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _NETWORK_TYPES) -> None: ...
    @property
    def filter(self) -> TravelModeUnitTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: TravelModeUnitTypeFilter | None) -> None: ...
# End NetworkTravelModeParameter class


class NAHierarchySettingsParameter(InputParameter):
    """
    A hierarchy attribute that divides hierarchy values of a network
    dataset into three groups using two integers. The first integer sets
    the ending value of the first group; the second number sets the
    beginning value of the third group.
    """
    @property
    def dependency(self) -> NetworkDatasetParameter | None: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: NetworkDatasetParameter | None) -> None: ...
# End NAHierarchySettingsParameter class


class StringParameter(InputOutputParameter):
    """
    A text value.
    """
    def _build_filter(self) -> tuple[dict, MAP_STR]: ...
    @property
    def filter(self) -> StringValueFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: StringValueFilter | None) -> None: ...
# End StringParameter class


class SQLExpressionParameter(InputParameter):
    """
    A syntax for defining and manipulating data from a relational
    database.
    """
    @property
    def dependency(self) -> _TABLE_AND_GEOGRAPHIC_TYPES: ...
    # noinspection PyUnresolvedReferences
    @dependency.setter
    def dependency(self, value: _TABLE_AND_GEOGRAPHIC_TYPES) -> None: ...
# End SQLExpressionParameter class


class TimeUnitParameter(InputParameter):
    """
    A time unit type and value such as minutes or hours.
    """
    @property
    def filter(self) -> TimeUnitFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: TimeUnitFilter | None) -> None: ...
# End TimeUnitParameter class


class WorkspaceParameter(InputOutputParameter):
    """
    A container such as a geodatabase or folder.
    """
    @property
    def filter(self) -> WorkspaceTypeFilter | None: ...
    # noinspection PyUnresolvedReferences
    @filter.setter
    def filter(self, value: WorkspaceTypeFilter | None) -> None: ...
# End WorkspaceParameter class


if __name__ == '__main__':  # pragma: no cover
    pass
