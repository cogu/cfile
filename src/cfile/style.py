"""
cfile style
"""
from enum import Enum
from dataclasses import dataclass


class BreakBeforeBraces(Enum):
    """
    The brace breaking style to use
    """
    ALLMAN = 0  # Always break
    ALWAYS = 0  # same as ALLMAN
    ATTACH = 1  # Always attach braces to surrounding context
    NEVER = 1  # Same as ATTACH
    CUSTOM = 2  # Custom control using BraceWrapping object
    LINUX = 3  # Like ATTACH but break before function


class SpaceLocation(Enum):
    """
    Placement of white-space
    """
    DEFAULT = 0
    BEFORE = 1
    AFTER = 2
    BOTH = 3


class Alignment(Enum):
    """
    Alignment style
    """
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2


class ShortFunction(Enum):
    """
    Short function style
    """
    NEVER = 0
    INLINE_ONLY = 1  # Does not imply empty
    EMPTY = 2
    INLINE = 3  # Implies empty
    ALL = 4


@dataclass
class BraceWrapping:
    """
    Individual control of brace wrapping.
    """
    after_case_label: bool = False
    after_enum: bool = False
    after_function: bool = False
    after_struct: bool = False
    after_union: bool = False
    after_extern_block: bool = False
    before_else: bool = False
    before_while: bool = False
    indent_braces: bool = False
    split_empty_funcion: bool = False

    @classmethod
    def make(cls, break_before_braces: BreakBeforeBraces) -> "BraceWrapping":
        """
        Utility function for auto-populating settings based on BreakBeforeBraces option.
        Don't use it with BreakBeforeBraces.CUSTOM.
        """
        if break_before_braces in (BreakBeforeBraces.ALLMAN, BreakBeforeBraces.ALWAYS):
            wrapping = cls(True, True, True, True, True, True, True, True, True, True)
        elif break_before_braces in (BreakBeforeBraces.ATTACH, BreakBeforeBraces.NEVER, BreakBeforeBraces.LINUX):
            wrapping = cls()
        else:
            raise NotImplementedError(break_before_braces)
        if break_before_braces == BreakBeforeBraces.LINUX:
            wrapping.after_function = True
        return wrapping


_default_type_qualifier_order = ['const', 'volatile', 'type']
_default_storage_class_order = ['static', 'extern', 'object']


class StyleOptions:
    """
    Format style options

    Default format style:
    * Indentation: 4 spaces
    * Always break for spaces (ALLMAN style)
    """
    def __init__(self,
                 break_before_braces: BreakBeforeBraces = BreakBeforeBraces.ALLMAN,
                 indent_width: int = 4,
                 indent_char: str = " ",
                 brace_wrapping: BraceWrapping | None = None,  # Only used when break_before_braces is CUSTOM
                 pointer_alignment: Alignment = Alignment.LEFT,
                 space_around_pointer_qualifiers: SpaceLocation = SpaceLocation.DEFAULT,
                 type_qualifier_order: list[str] | tuple[str] = None,
                 storage_class_order: list[str] | tuple[str] = None,
                 short_functions_on_single_line: ShortFunction = ShortFunction.NEVER) -> None:
        self.break_before_braces = break_before_braces
        self.indent_width = indent_width
        self.indent_char = indent_char
        self.pointer_alignment = pointer_alignment
        self.space_around_pointer_qualifiers = space_around_pointer_qualifiers
        if type_qualifier_order is not None:
            self.type_qualifier_order = list(type_qualifier_order)
        else:
            self.type_qualifier_order = _default_type_qualifier_order
        if storage_class_order is not None:
            self.storage_class_order = list(storage_class_order)
        else:
            self.storage_class_order = _default_storage_class_order
        if break_before_braces == BreakBeforeBraces.CUSTOM:
            assert isinstance(brace_wrapping, BraceWrapping)
            self.brace_wrapping = brace_wrapping
        else:
            self.brace_wrapping = BraceWrapping.make(break_before_braces)
        self.short_functions_on_single_line = short_functions_on_single_line
