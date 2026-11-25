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


class PPDirectiveIndent(Enum):
    """
    Preprocessor directive indentation style
    """
    NONE = 0
    AFTER_HASH = 1
    BEFORE_HASH = 2


@dataclass
class BraceWrapping:
    """
    Individual control of brace wrapping when :attr:`BreakBeforeBraces.CUSTOM` is used.

    Attributes:
        after_case_label: Wrap brace after a ``case`` or ``default`` label.
        after_control_statement: Wrap brace after control statements (``if``, ``else``, ``switch``).
        after_enum: Wrap brace after an ``enum`` declaration.
        after_function: Wrap brace after a function signature.
        after_struct: Wrap brace after a ``struct`` declaration.
        after_union: Wrap brace after a ``union`` declaration.
        after_extern_block: Wrap brace after an ``extern`` block declaration.
        before_else: Place ``else`` and ``else if`` on a new line after the preceding closing brace.
        before_while: Place ``while`` on a new line in a ``do ... while`` loop.
        indent_braces: Indent the opening and closing braces themselves.
        split_empty_funcion: Split empty function body braces across two lines.
    """
    after_case_label: bool = False
    after_control_statement: bool = False
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
        Auto-populates brace wrapping settings based on a :class:`BreakBeforeBraces` preset.

        Do not use this method with :attr:`BreakBeforeBraces.CUSTOM`.

        Args:
            break_before_braces: The brace breaking preset to expand.

        Returns:
            A populated :class:`BraceWrapping` instance.
        """
        if break_before_braces in (BreakBeforeBraces.ALLMAN, BreakBeforeBraces.ALWAYS):
            wrapping = cls(True, True, True, True, True, True, True, True, True, True, True)
        elif break_before_braces in (BreakBeforeBraces.ATTACH, BreakBeforeBraces.NEVER, BreakBeforeBraces.LINUX):
            wrapping = cls()
        else:
            raise NotImplementedError(break_before_braces)
        if break_before_braces == BreakBeforeBraces.LINUX:
            wrapping.after_function = True
        return wrapping


_default_type_qualifier_order = ['const', 'volatile', 'type']
_default_storage_class_order = ['static', 'extern', 'object']


class StyleOptions:  # pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
    """
    Formatting style options for :class:`~cfile.writer.Writer`.

    Args:
        break_before_braces: Preset brace breaking style (defaults to
            :attr:`BreakBeforeBraces.ALLMAN`).
        indent_width: Number of indentation characters per level (defaults to ``4``).
        indent_char: Character used for indentation (defaults to ``" "``).
        brace_wrapping: Custom :class:`BraceWrapping` configuration (only used when
            ``break_before_braces`` is :attr:`BreakBeforeBraces.CUSTOM`).
        pointer_alignment: Placement of ``*`` in pointer declarations
            (:attr:`Alignment.LEFT`, :attr:`Alignment.RIGHT`, or :attr:`Alignment.MIDDLE`).
        space_around_pointer_qualifiers: Placement of spaces around pointer qualifiers
            such as ``* const``.
        type_qualifier_order: Order of type qualifiers relative to ``"type"``
            (defaults to ``['const', 'volatile', 'type']``).
        storage_class_order: Order of storage class specifiers relative to ``"object"``
            (defaults to ``['static', 'extern', 'object']``).
        short_functions_on_single_line: Controls when short or empty functions are
            placed on a single line.
        indent_case_labels: When ``True``, indents ``case`` and ``default`` labels one
            level inside a ``switch`` block (defaults to ``False``).
        indent_case_blocks: When ``True``, indents a ``{ ... }`` block following a
            ``case`` label one level deeper than the label (defaults to ``False``).
        indent_goto_labels: When ``True`` (the default), outdents named ``goto`` labels
            by one level relative to surrounding statements; when ``False``, places them
            at column 0.
        indent_pp_directives: Controls whether nested preprocessor directives are indented
            after ``#`` (:attr:`PPDirectiveIndent.AFTER_HASH`), before ``#``
            (:attr:`PPDirectiveIndent.BEFORE_HASH`), or not at all
            (:attr:`PPDirectiveIndent.NONE`, the default).
        pp_indent_width: Number of spaces per preprocessor nesting level when
            ``indent_pp_directives`` is enabled. When ``-1`` (the default), uses
            ``indent_width``.
    """
    def __init__(self,
                 break_before_braces: BreakBeforeBraces = BreakBeforeBraces.ALLMAN,
                 indent_width: int = 4,
                 indent_char: str = " ",
                 brace_wrapping: BraceWrapping | None = None,  # Only used when break_before_braces is CUSTOM
                 pointer_alignment: Alignment = Alignment.LEFT,
                 space_around_pointer_qualifiers: SpaceLocation = SpaceLocation.DEFAULT,
                 type_qualifier_order: list[str] | tuple[str, ...] | None = None,
                 storage_class_order: list[str] | tuple[str, ...] | None = None,
                 short_functions_on_single_line: ShortFunction = ShortFunction.NEVER,
                 indent_case_labels: bool = False,
                 indent_case_blocks: bool = False,
                 indent_goto_labels: bool = True,
                 indent_pp_directives: PPDirectiveIndent = PPDirectiveIndent.NONE,
                 pp_indent_width: int = -1) -> None:
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
        self.indent_case_labels = indent_case_labels
        self.indent_case_blocks = indent_case_blocks
        self.indent_goto_labels = indent_goto_labels
        self.indent_pp_directives = indent_pp_directives
        self.pp_indent_width = pp_indent_width
