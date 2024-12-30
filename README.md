# autobox
Automation for ArcGIS Pro toolboxes, script tools, and documentation from 
Python objects.  `autobox` generates the modern ArcGIS Pro Toolbox format (`.atbx`)
and has support for Script Tools, Parameters, Dependencies, Filters, 
Toolsets, and documentation. Pure Python package and cross-platform (no dependencies).


## Installation

`autobox` is available from the [Python Package Index](https://pypi.org/project/autobox/).


## Python Compatibility

The `autobox` library is compatible with Python 3.11 to 3.13.  Developed and 
tested on **macOS** and **Windows**, should be fine on **Linux** too.


## Usage

`autobox` can be used to: 
* Create a `Toolbox` and save to `.atbx` format
* Create a `Toolset` and add to a `Toolbox` or `Toolset`
* Create a `ScriptTool` with `Parameters` and add to a `Toolbox` or `Toolset`
* Add an `ExecutionScript` to a `ScriptTool`
* Add an optional `ValidationScript` to a `ScriptTool`
* Create and add a `Filter` to a `Parameter`
* Add a dependency to a `Parameter`
* Add documentation to `Toolbox`, `ScriptTool`, and`Parameter`


### Create a `Toolbox`

Create an empty `Toolbox` in the home folder:

```python
from pathlib import Path
from autobox import Toolbox

# Creates an empty Toolbox
tbx = Toolbox(name='demonstration', label='Demonstration Toolbox', alias='demo')

# Save the toolbox to disk, overwrite is False by default
tbx_path = tbx.save(Path.home(), overwrite=True)
```

### Create a `ScriptTool`
Create a `ScriptTool` in the root of the `Toolbox` 

```python
from pathlib import Path
from autobox import ScriptTool, Toolbox
from autobox.parameter import FeatureClassParameter, LongParameter

# Create Simple Script Tool
points = FeatureClassParameter(label='Random Points')
sample_size = LongParameter(label='Sample Size', is_required=False)
poly = FeatureClassParameter(label='Bounding Boxes')
out = FeatureClassParameter(label='Output Feature Class', is_input=False)
tool = ScriptTool(name='SimpleScriptTool', label='Simple Script Tool')
for param in points, sample_size, poly, out:
    tool.add_parameter(param)

tbx = Toolbox(name='demonstration')
tbx.add_script_tool(tool)
tbx_path = tbx.save(Path.home(), overwrite=True)
```
This generates a `ScriptTool` that looks like this:

![](https://github.com/realiii/autobox/blob/develop/resources/images/simple_script_tool.png?raw=true)


Or create a `ScriptTool` inside of a `Toolset`:
```python
from pathlib import Path
from autobox import ScriptTool, Toolbox, Toolset
from autobox.parameter import FeatureClassParameter, LongParameter

# Create Simple Script Tool
points = FeatureClassParameter(label='Random Points')
sample_size = LongParameter(label='Sample Size', is_required=False)
poly = FeatureClassParameter(label='Bounding Boxes')
out = FeatureClassParameter(label='Output Feature Class', is_input=False)
tool = ScriptTool(name='SimpleScriptTool', label='Simple Script Tool')
for param in points, sample_size, poly, out:
    tool.add_parameter(param)

# Create a Toolset, add the tool to the Toolset
toolset = Toolset(name='Overlay Tools')
toolset.add_script_tool(tool)

tbx = Toolbox(name='demonstration')
# Add Toolset to the Toolbox
tbx.add_toolset(toolset)
tbx_path = tbx.save(Path.home(), overwrite=True)
```

The `ScriptTool` looks the same but now there is an **Overlay Tools** `Toolset` in the `Toolbox`:

![](https://github.com/realiii/autobox/blob/develop/resources/images/toolset.png?raw=true)

Empty `Toolsets` are not persisted unless the `Toolset` (or a child `Toolset` of 
the `Toolset`) contains a `ScriptTool`.  In this example the `Toolbox` will be empty:

```python
from pathlib import Path
from autobox import Toolbox, Toolset

toolset = Toolset(name='Overlay Tools')
tbx = Toolbox(name='demonstration')
tbx.add_toolset(toolset)
tbx_path = tbx.save(Path.home(), overwrite=True)
```

### Add Documentation
Documentation can be added to a `Toolbox`, `ScriptTool`, or `Parameter`.  On a `Toolbox`:

#### `Toolbox` Documentation
```python
from autobox import Toolbox

tbx = Toolbox(name='demonstration', label='Demonstration Toolbox', alias='demo', 
              description='Here is where a longer description of the Toolbox can be included.')
```

![](https://github.com/realiii/autobox/blob/develop/resources/images/toolbox_doc.png?raw=true)


#### `ScriptTool` Documentation
There are couple ways to document a `ScriptTool` using `description` and / or `summary`:

```python
from autobox import ScriptTool

tool = ScriptTool(
  name='SimpleScriptTool', label='Simple Script Tool',
  description='Use the description for a shorter plain text explanation of the Tool purpose',
  summary='The summary can hold some basic markup, <b>bold example</b>')
```

![](https://github.com/realiii/autobox/blob/develop/resources/images/script_tool_doc.png?raw=true)

An image can also be included to show on the `ScriptTool`, this is done by setting the `illustration` property:
```python
from pathlib import Path
from autobox import ScriptTool

tool = ScriptTool(
  name='SimpleScriptTool', label='Simple Script Tool',
  description='Use the description for a shorter plain text explanation of the Tool purpose',
  summary='The summary can hold some basic markup, <b>bold example</b>')

# NOTE only png and jpg formats are supported
tool.illustration = Path('../data/images/numpy_illustration.png')

# NOTE Icon for the Script Tool can be set too,
#  Technically not documentation but worth mentioning 
tool.icon = Path('../data/images/python_icon.png')

```
![](https://github.com/realiii/autobox/blob/develop/resources/images/illustration_icon.png?raw=true)

#### `Parameter` Documentation
Each individual `Parameter` also supports documentation via `description` which can be plain text or contain basic markup

```python
from autobox.parameter import FeatureClassParameter

points = FeatureClassParameter(
    label='Random Points',
    description='Select a feature class with randomly spaced '
                'points over the area of interest')

```

![](https://github.com/realiii/autobox/blob/develop/resources/images/parameter_doc.png?raw=true)

### Extended Example
This example shows use of `Filters`, setting a dependency `Parameter`, and using a category 
for grouping parameters:

```python
from pathlib import Path
from autobox import ScriptTool, Toolbox, Toolset
from autobox.enum import GeometryType, LinearUnit
from autobox.filter import (
    FeatureClassTypeFilter, LinearUnitFilter, LongRangeFilter)
from autobox.parameter import (
    FeatureClassParameter, LinearUnitParameter, LongParameter)


# NOTE only allow for point and multi point feature classes
points = FeatureClassParameter(
    label='Random Points',
    description='Select a feature class with randomly spaced '
                'points over the area of interest')
points.filter = FeatureClassTypeFilter((GeometryType.POINT, GeometryType.MULTIPOINT))

# NOTE keep the sample size between 100 and 1000
sample_size = LongParameter(
    label='Sample Size', category='Pieces of Flair', is_required=False)
sample_size.filter = LongRangeFilter(minimum=100, maximum=1000)

buffer_units = LinearUnitParameter(
    label='Buffer Units', category='Pieces of Flair', is_required=False)
# NOTE use of dependency
buffer_units.dependency = points
buffer_units.filter = LinearUnitFilter((LinearUnit.METERS, LinearUnit.FEET))

# NOTE only allow for polygon feature classes
poly = FeatureClassParameter(label='Bounding Boxes')
poly.filter = FeatureClassTypeFilter(GeometryType.POLYGON)

out = FeatureClassParameter(label='Output Feature Class', is_input=False)

tool = ScriptTool(
  name='SimpleScriptTool', label='Simple Script Tool',
  description='Use the description for a shorter plain text explanation of the Tool purpose',
  summary='The summary can hold some basic markup, <b>bold example</b>')
for param in points, sample_size, buffer_units, poly, out:
    tool.add_parameter(param)

# Create a Toolset, add the tool to the Toolset
toolset = Toolset(name='Overlay Tools')
toolset.add_script_tool(tool)

tbx = Toolbox(name='demonstration', label='Demonstration Toolbox', alias='demo',
              description='Here is where a longer description of the Toolbox can be included.')
tbx.add_toolset(toolset)
tbx_path = tbx.save(Path.home(), overwrite=True)

```

The result of this snippet is a `ScriptTool` which looks like:

![](https://github.com/realiii/autobox/blob/develop/resources/images/extended.png?raw=true)

Notice the error message because the **Sample Size** is out of range:

![](https://github.com/realiii/autobox/blob/develop/resources/images/extended_error.png?raw=true)


### Execution and Validation Scripts
For completeness, here are a few examples of setting the `ExecutionScript` and `ValidationScript`.  
The `ExecutionScript` will almost always be needed and the `ValidationScript` is likely optional
for most use cases.  Use the class methods `from_code` and `from_file` to construct an instance.

```python
from pathlib import Path
from autobox import ExecutionScript, ScriptTool, ValidationScript

# NOTE example adding from a code snippet
tool = ScriptTool(name='SimpleScriptTool', label='Simple Script Tool')
tool.execution_script = ExecutionScript.from_code('print("Hello World")')

# NOTE example adding from a file and choosing to embed
tool = ScriptTool(name='SimpleScriptTool', label='Simple Script Tool')
tool.execution_script = ExecutionScript.from_file(
  Path('../data/scripts/subfolder/example.py'), embed=True)
# NOTE validator scripts are always embedded
tool.validation_script = ValidationScript.from_file(Path('../data/scripts/validator.py'))
```


## License

[MIT](https://raw.githubusercontent.com/realiii/autobox/refs/heads/develop/LICENSE)


## Release History

### v0.2.0
* Added support for symbology (via layer file) on parameters
* Include type tuples in `enum` for Rational Numbers, Integers, Numbers, Strings, and Identifiers
* Extend dependency types to include `FeatureRecordSetLayerParameter` and `RecordSetParameter` on: 
  * `AreaUnitParameter`
  * `Field`
  * `LinearUnit`
  * `SQLExpression`
* Add dependency types to:
  * `FieldMappingParameter`
  * `GAValueTableParameter`
  * `NAHierarchySettingsParameter`
  * `NetworkTravelModeParameter` 
* Enable following parameters to be used as a derived parameter:
  * `BooleanParameter`
  * `DateParameter`
  * `DatasetParameter`
  * `DoubleParameter`
  * `LongParameter`
  * `SpatialReferenceParameter`
* Added new filters `TimeUnitFilter` and `TravelModeUnitTypeFilter`
* `Parameter` types added in this release:
  * `DataFileParameter`
  * `DiagramLayerParameter`
  * `FeatureRecordSetLayerParameter`
  * `FieldInfoParameter`
  * `FieldMappingParameter`
  * `GALayerParameter`
  * `GASearchNeighborhoodParameter`
  * `GAValueTableParameter`
  * `GeodatasetTypeParameter`
  * `GeometricNetworkParameter`
  * `KMLLayerParameter`
  * `MDomainParameter`
  * `NAClassFieldMapParameter`
  * `NAHierarchySettingsParameter`
  * `NALayerParameter`
  * `NetworkDataSourceParameter`
  * `NetworkDatasetLayerParameter`
  * `RandomNumberGeneratorParameter`
  * `RasterBuilderParameter`
  * `RecordSetParameter`
  * `SAExtractValuesParameter`
  * `SAFuzzyFunctionParameter`
  * `SAGDBEnvCompressionParameter`
  * `SAGDBEnvPyramidParameter`
  * `SAGDBEnvStatisticsParameter`
  * `SAGDBEnvTileSizeParameter`
  * `SAHorizontalFactorParameter`
  * `SANeighborhoodParameter`
  * `SARadiusParameter`
  * `SARemapParameter`
  * `SASemiVariogramParameter`
  * `SATimeConfigurationParameter`
  * `SATopoFeaturesParameter`
  * `SATransformationFunctionParameter`
  * `SAVerticalFactorParameter`
  * `SAWeightedOverlayTableParameter`
  * `SAWeightedSumParameter`
  * `SchematicDatasetParameter`
  * `SchematicDiagramClassParameter`
  * `SchematicDiagramParameter`
  * `SchematicFolderParameter`
  * `SchematicLayerParameter`
  * `TerrainLayerParameter`
  * `TopologyLayerParameter`
  * `ValueTableParameter`
  * `VectorLayerParameter`
  * `XYDomainParameter`
  * `ZDomainParameter`

### v0.1.0
* initial release
* Create a `Toolbox` and save to `.atbx` format
* Create a `Toolset` and add to a `Toolbox` or `Toolset`
* Create a `ScriptTool` with `Parameters` and add to a `Toolbox` or `Toolset`
* Add an `ExecutionScript` to a `ScriptTool`
* Add an optional `ValidationScript` to a `ScriptTool`
* Add a dependency to a `Parameter`
* Add documentation to `Toolbox`, `ScriptTool`, and `Parameter`
* Create and add a `Filter` to a `Parameter`, filters include:
  * `ArealUnitFilter`
  * `DoubleRangeFilter`
  * `DoubleValueFilter`
  * `FeatureClassTypeFilter`
  * `FileTypeFilter`
  * `LinearUnitFilter`
  * `LongRangeFilter`
  * `LongValueFilter`
  * `StringValueFilter`
  * `WorkspaceTypeFilter`
* `Parameter` types added in this release:
  * `AnalysisCellSizeParameter`
  * `ArealUnitParameter`
  * `BooleanParameter`
  * `CadDrawingDatasetParameter`
  * `CalculatorExpressionParameter`
  * `CatalogLayerParameter`
  * `CellSizeXYParameter`
  * `CoordinateSystemParameter`
  * `CoverageFeatureClassParameter`
  * `CoverageParameter`
  * `DataElementParameter`
  * `DatasetTypeParameter`
  * `DateParameter`
  * `DbaseTableParameter`
  * `DoubleParameter`
  * `EncryptedStringParameter`
  * `EnvelopeParameter`
  * `ExtentParameter`
  * `FeatureClassParameter`
  * `FeatureDatasetParameter`
  * `FeatureLayerParameter`
  * `FieldParameter`
  * `FileParameter`
  * `FolderParameter`
  * `GPLayerParameter`
  * `GroupLayerParameter`
  * `LasDatasetLayerParameter`
  * `LasDatasetParameter`
  * `LayerFileParameter`
  * `LinearUnitParameter`
  * `LongParameter`
  * `MapDocumentParameter`
  * `MapParameter`
  * `MosaicDatasetParameter`
  * `MosaicLayerParameter`
  * `NetworkDatasetParameter`
  * `PointParameter`
  * `PrjFileParameter`
  * `RasterBandParameter`
  * `RasterCalculatorExpressionParameter`
  * `RasterDataLayerParameter`
  * `RasterDatasetParameter`
  * `RasterLayerParameter`
  * `RelationshipClassParameter`
  * `SACellSizeParameter`
  * `SQLExpressionParameter`
  * `ShapeFileParameter`
  * `SpatialReferenceParameter`
  * `StringHiddenParameter`
  * `StringParameter`
  * `TableParameter`
  * `TableViewParameter`
  * `TextfileParameter`
  * `TinLayerParameter`
  * `TinParameter`
  * `TopologyParameter`
  * `WorkspaceParameter`
