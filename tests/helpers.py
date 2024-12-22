# -*- coding: utf-8 -*-
"""
Helper Utilities
"""


from json import load
from pathlib import Path
from re import compile as recompile
from typing import Pattern
from zipfile import ZipFile


DATETIME_PATTERN: Pattern = recompile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')


DEFAULT_EXECUTION_CODE: str = '''"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy


def script_tool(param0, param1):
    """Script code goes below"""

    return


if __name__ == "__main__":

    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)

    script_tool(param0, param1)
    arcpy.SetParameterAsText(2, "Result")
'''


def read_from_zip(path: Path, name: str, as_json: bool) -> dict | str:
    """
    Read file content from a zip, optionally as json
    """
    with ZipFile(path) as zin:
        with zin.open(name) as fin:
            if as_json:
                return load(fin)
            else:
                return fin.read().decode('utf-8')
# End read_from_zip function


if __name__ == '__main__':  # pragma: no cover
    pass
