# -*- coding: utf-8 -*-
"""
Types and Aliases
"""


from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING, TypeAlias, Union


if TYPE_CHECKING:  # pragma: no cover
    # noinspection PyProtectedMember
    from stoolbox.parameter import InputOutputParameter, InputParameter


PATH: TypeAlias = Path | None
BOOL: TypeAlias = bool | None
STRING: TypeAlias = str | None
TOOLS_MAP: TypeAlias = dict[str, dict[str, list[str]]]
PARAMETER: TypeAlias = Union['InputOutputParameter', 'InputParameter']


class ToolAttributes(NamedTuple):
    """
    Tool Attributes
    """
    show_modifies_input: bool = False
    do_not_add_to_map: bool = False
    show_enable_undo: bool = False
    show_consumes_credits: bool = False
# End ToolAttributes class


if __name__ == '__main__':  # pragma: no cover
    pass
