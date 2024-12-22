# -*- coding: utf-8 -*-
"""
Types and Aliases
"""


from typing import NamedTuple, Optional, TypeAlias


STRING: TypeAlias = Optional[str]
TOOLS_MAP: TypeAlias = dict[str, dict[str, list[str]]]


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
