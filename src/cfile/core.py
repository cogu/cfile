"""
cfile core
"""
from __future__ import annotations
from typing import Any


class Element:
    """
    A code element, for example an expression
    """


class Directive(Element):
    """
    Preprocessor directive base class.

    Args:
        text: Directive text following ``#`` (e.g. ``"pragma once"``).
    """
    def __init__(self, text: str) -> None:
        self.text = text


class IncludeDirective(Directive):
    """
    Preprocessor ``#include`` directive.

    Args:
        path_to_file: Header file path to include.
        sys: When ``True``, wraps the path in ``<...>``; when ``False``, wraps it in ``"..."``.
    """
    def __init__(self, path_to_file: str, sys: bool = False) -> None:
        self.path_to_file = path_to_file
        self.sys = sys
        target = f"<{path_to_file}>" if sys else f'"{path_to_file}"'
        super().__init__(f"include {target}")


class IncludeNextDirective(Directive):
    """
    Preprocessor ``#include_next`` directive (GCC/Clang extension).

    Args:
        path_to_file: Header file path to include.
        sys: When ``True``, wraps the path in ``<...>``; when ``False``, wraps it in ``"..."``.
    """
    def __init__(self, path_to_file: str, sys: bool = False) -> None:
        self.path_to_file = path_to_file
        self.sys = sys
        target = f"<{path_to_file}>" if sys else f'"{path_to_file}"'
        super().__init__(f"include_next {target}")


class EmbedDirective(Directive):
    """
    Preprocessor ``#embed`` directive (C23).

    Args:
        path_to_file: Resource file path to embed.
        sys: When ``True``, wraps the path in ``<...>``; when ``False``, wraps it in ``"..."``.
        params: Optional embed parameter string or list of parameter strings
            (e.g. ``"limit(256)"`` or ``["limit(256)", "if_empty(0)"]``).
    """
    def __init__(self,
                 path_to_file: str,
                 sys: bool = False,
                 params: str | list[str] | None = None) -> None:
        self.path_to_file = path_to_file
        self.sys = sys
        self.params = params
        target = f"<{path_to_file}>" if sys else f'"{path_to_file}"'
        if params is None:
            text = f"embed {target}"
        elif isinstance(params, str):
            text = f"embed {target} {params}"
        elif isinstance(params, list):
            text = f"embed {target} {' '.join(params)}"
        else:
            raise ValueError(f"Unsupported type of params: {str(type(params))}")
        super().__init__(text)


class DefineDirective(Directive):
    """
    Preprocessor ``#define`` directive.

    Args:
        left: Macro identifier or function-like macro signature.
        right: Optional macro expansion value.
    """
    def __init__(self, left: str, right: str | int | float | None = None) -> None:
        self.left = left
        self.right = str(right) if isinstance(right, (int, float)) else right
        if self.right is not None:
            super().__init__(f"define {self.left} {self.right}")
        else:
            super().__init__(f"define {self.left}")


class UndefDirective(Directive):
    """
    Preprocessor ``#undef`` directive.

    Args:
        identifier: Macro identifier to undefine.
    """
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"undef {identifier}")


class IfDirective(Directive):
    """
    Preprocessor ``#if`` conditional directive.

    Args:
        expression: Constant preprocessor expression to evaluate.
    """
    def __init__(self, expression: str) -> None:
        self.expression = expression
        super().__init__(f"if {expression}")


class IfdefDirective(Directive):
    """
    Preprocessor ``#ifdef`` conditional directive.

    Args:
        identifier: Macro identifier to test.
    """
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"ifdef {identifier}")


class IfndefDirective(Directive):
    """
    Preprocessor ``#ifndef`` conditional directive.

    Args:
        identifier: Macro identifier to test.
    """
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"ifndef {identifier}")


class ElifDirective(Directive):
    """
    Preprocessor ``#elif`` conditional directive.

    Args:
        expression: Constant preprocessor expression to evaluate.
    """
    def __init__(self, expression: str) -> None:
        self.expression = expression
        super().__init__(f"elif {expression}")


class ElifdefDirective(Directive):
    """
    Preprocessor ``#elifdef`` conditional directive (C23).

    Args:
        identifier: Macro identifier to test.
    """
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"elifdef {identifier}")


class ElifndefDirective(Directive):
    """
    Preprocessor ``#elifndef`` conditional directive (C23).

    Args:
        identifier: Macro identifier to test.
    """
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"elifndef {identifier}")


class ElseDirective(Directive):
    """
    Preprocessor ``#else`` conditional directive.
    """
    def __init__(self) -> None:
        super().__init__("else")


class EndifDirective(Directive):
    """
    Preprocessor ``#endif`` conditional directive.
    """
    def __init__(self) -> None:
        super().__init__("endif")


class LineDirective(Directive):
    """
    Preprocessor ``#line`` directive.

    Args:
        line_number: Line number to set.
        filename: Optional source filename string.
    """
    def __init__(self, line_number: int | str, filename: str | None = None) -> None:
        self.line_number = line_number
        self.filename = filename
        if filename is not None:
            super().__init__(f'line {line_number} "{filename}"')
        else:
            super().__init__(f"line {line_number}")


class ErrorDirective(Directive):
    """
    Preprocessor ``#error`` diagnostic directive.

    Args:
        message: Optional diagnostic error message text.
    """
    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(f"error {message}" if message else "error")


class WarningDirective(Directive):
    """
    Preprocessor ``#warning`` diagnostic directive (C23 and compiler extension).

    Args:
        message: Optional diagnostic warning message text.
    """
    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(f"warning {message}" if message else "warning")


class PragmaDirective(Directive):
    """
    Preprocessor ``#pragma`` directive.

    Args:
        tokens: Pragma tokens following ``#pragma``.
    """
    def __init__(self, tokens: str = "") -> None:
        self.tokens = tokens
        super().__init__(f"pragma {tokens}" if tokens else "pragma")


class Extern(Element):
    """
    Extern declaration
    """
    def __init__(self, language: str) -> None:
        self.language = language


class Comment(Element):
    """
    Comment base

    Args:
        text: Comment text as a string or list of strings.
        adjust: Adds spaces before comment begins to allow right-adjustment.
    """
    def __init__(self, text: str | list[str], adjust: int = 1) -> None:
        self.text = text
        self.adjust = adjust


class BlockComment(Comment):
    """
    Block Comment

    Args:
        text: Comment text as a string or list of strings.
        adjust: Adds spaces before comment begins to allow right-adjustment.
        width: When > 0, sets the number of asterisks used on first and last line
            and places the text between the first and last line.
        line_start: Combine with width > 0. Puts this string at the beginning of
            each line inside the comment.
    """
    def __init__(self,
                 text: str | list[str],
                 adjust: int = 1, width: int = 0,
                 line_start: str = "", ) -> None:
        super().__init__(text, adjust)
        self.width = width
        self.line_start = line_start


class LineComment(Comment):
    """
    Line Comment
    """


class Whitespace(Element):
    """
    Whitespace
    """
    def __init__(self, width: int) -> None:
        self.width = width


class Blank(Whitespace):
    """
    Blank line
    """
    def __init__(self) -> None:
        super().__init__(0)


class Line(Element):
    """
    Adds a newline once all inner parts have been written
    """
    def __init__(self, parts: str | Element | list[Any]) -> None:
        if isinstance(parts, (str, Element)):
            self.parts = [parts]
        elif isinstance(parts, list):
            self.parts = parts
        else:
            raise TypeError("Invalid type:" + str(type(parts)))


class DataType(Element):
    """
    Base class for all data types
    """
    def __init__(self, name: str | None) -> None:
        self.name = name


class Type(DataType):
    """
    Data type
    """
    def __init__(self,
                 base_type: str | "Type",
                 const: bool = False,
                 pointer: bool = False,
                 volatile: bool = False,
                 array: int | None = None) -> None:  # Only used for typedefs to other array types
        super().__init__(None)
        self.base_type = base_type
        self.const = const
        self.volatile = volatile
        self.pointer = pointer
        self.array = array

    def qualifier(self, name: str) -> bool:
        """
        Returns the status of named qualifier
        """
        if name == "const":
            return self.const
        if name == "volatile":
            return self.volatile
        else:
            raise KeyError(name)


class StructMember(Element):
    """
    A member field of a C ``struct``.

    Similar to :class:`Variable`, but does not support storage class specifiers
    such as ``static`` or ``extern``.

    Args:
        name: Field identifier name.
        data_type: Field data type name, :class:`DataType`, or inline struct/union
            :class:`Declaration`.
        const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
        pointer: When ``True``, declares the field as a pointer to ``data_type``.
        array: Optional array dimension size (emits ``name[array]``).
    """
    def __init__(self,
                 name: str,
                 data_type: DataType | str | "Declaration",
                 const: bool = False,    # Pointer qualifier only
                 pointer: bool = False,
                 array: int | None = None) -> None:
        self.name = name
        self.const = const
        self.pointer = pointer
        self.array = array
        self.data_type: DataType | Declaration
        if isinstance(data_type, DataType):
            self.data_type = data_type
        elif isinstance(data_type, str):
            self.data_type = Type(data_type)
        elif isinstance(data_type, Declaration):
            if not isinstance(data_type.element, DataType):
                raise TypeError(f"data_type: Declaration must declare a DataType, not {str(type(data_type.element))}")
            self.data_type = data_type
        else:
            raise TypeError(str(type(data_type)))

    def __str__(self) -> str:
        return self.name


class Struct(DataType):
    """
    A C ``struct`` type definition or reference.

    Args:
        name: Optional struct tag name (``None`` for an anonymous ``struct``).
        members: Optional single :class:`StructMember` or list of struct members.
    """
    def __init__(self,
                 name: str | None = None,
                 members: StructMember | list[StructMember] | None = None) -> None:
        super().__init__(name)
        self.members: list[StructMember] = []
        if members is not None:
            if isinstance(members, StructMember):
                self.append(members)
            elif isinstance(members, list):
                for member in members:
                    self.append(member)
            else:
                raise TypeError('Invalid argument type for "elements"')

    def append(self, member: StructMember) -> None:
        """
        Appends a new member field to the struct definition.

        Args:
            member: The :class:`StructMember` to append.
        """
        if not isinstance(member, StructMember):
            raise TypeError(f'Invalid type, expected "StructMember", got {str(type(member))}')
        self.members.append(member)

    def make_member(self,
                    name: str,
                    data_type: str | DataType | "Declaration",
                    const: bool = False,  # Pointer qualifier only
                    pointer: bool = False,
                    array: int | None = None) -> StructMember:
        """
        Creates a new :class:`StructMember` and appends it to this struct.

        Args:
            name: Field identifier name.
            data_type: Field data type name, :class:`DataType`, or inline struct/union
                :class:`Declaration`.
            const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
            pointer: When ``True``, declares the field as a pointer to ``data_type``.
            array: Optional array dimension size.

        Returns:
            The newly created :class:`StructMember`.
        """
        member = StructMember(name, data_type, const, pointer, array)
        self.members.append(member)
        return member


class UnionMember(StructMember):
    """
    A member field of a C ``union``.

    Args:
        name: Field identifier name.
        data_type: Field data type name, :class:`DataType`, or inline struct/union
            :class:`Declaration`.
        const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
        pointer: When ``True``, declares the field as a pointer to ``data_type``.
        array: Optional array dimension size (emits ``name[array]``).
    """


class Union(DataType):
    """
    A C ``union`` type definition or reference.

    Args:
        name: Optional union tag name (``None`` for an anonymous ``union``).
        members: Optional single :class:`UnionMember` / :class:`StructMember` or list of members.
    """
    def __init__(self,
                 name: str | None = None,
                 members: StructMember | list[StructMember] | None = None) -> None:
        super().__init__(name)
        self.members: list[StructMember] = []
        if members is not None:
            if isinstance(members, StructMember):
                self.append(members)
            elif isinstance(members, list):
                for member in members:
                    self.append(member)
            else:
                raise TypeError('Invalid argument type for "members"')

    def append(self, member: StructMember) -> None:
        """
        Appends a new member field to the union definition.

        Args:
            member: The :class:`UnionMember` or :class:`StructMember` to append.
        """
        if not isinstance(member, StructMember):
            raise TypeError(f'Invalid type, expected "StructMember" or "UnionMember", got {str(type(member))}')
        self.members.append(member)

    def make_member(self,
                    name: str,
                    data_type: str | DataType | "Declaration",
                    const: bool = False,  # Pointer qualifier only
                    pointer: bool = False,
                    array: int | None = None) -> UnionMember:
        """
        Creates a new :class:`UnionMember` and appends it to this union.

        Args:
            name: Field identifier name.
            data_type: Field data type name, :class:`DataType`, or inline struct/union
                :class:`Declaration`.
            const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
            pointer: When ``True``, declares the field as a pointer to ``data_type``.
            array: Optional array dimension size.

        Returns:
            The newly created :class:`UnionMember`.
        """
        member = UnionMember(name, data_type, const, pointer, array)
        self.members.append(member)
        return member


class EnumMember(Element):
    """
    A member constant of a C ``enum``.

    Args:
        name: Enumerator identifier name (without the parent enum's ``prefix``).
        value: Optional explicit integer, string expression, or :class:`Element` value.
        prefix: Optional prefix prepended to ``name`` when rendered (automatically
            inherited when added to an :class:`Enum`).
    """
    def __init__(self,
                 name: str,
                 value: int | str | Element | None = None,
                 prefix: str = "") -> None:
        self.name = name
        self.prefix = prefix
        self.parent: Enum | None = None
        self.value: str | Element | None
        if value is None:
            self.value = None
        elif isinstance(value, bool):
            raise TypeError('value: Invalid type "bool" for EnumMember')
        elif isinstance(value, int):
            self.value = str(value)
        elif isinstance(value, (str, Element)):
            self.value = value
        else:
            raise TypeError(f'value: Invalid type, expected "int" | "str" | "Element", got {str(type(value))}')

    @property
    def full_name(self) -> str:
        """
        Returns the effective enumerator identifier including any prefix.
        """
        active_prefix = self.parent.prefix if self.parent is not None else self.prefix
        return f"{active_prefix}{self.name}"

    def __str__(self) -> str:
        return self.full_name


EnumMemberInput = EnumMember | str | tuple[str, int | str | Element | None]


class Enum(DataType):
    """
    A C ``enum`` type definition or reference.

    Args:
        name: Optional enum tag name (``None`` for an anonymous ``enum``).
        members: Optional initial enumerator(s). Accepts a single :class:`EnumMember`,
            ``str``, or ``(name, value)`` tuple; a list of any of those; or a ``dict``
            mapping enumerator names to values.
        prefix: Optional prefix string automatically prepended to every member's name
            when declared or referenced.
    """
    def __init__(self,
                 name: str | None = None,
                 members: (
                     EnumMemberInput
                     | list[EnumMemberInput]
                     | dict[str, int | str | Element | None]
                     | None
                 ) = None,
                 prefix: str = "") -> None:
        super().__init__(name)
        self.prefix = prefix
        self.members: list[EnumMember] = []
        if members is not None:
            if isinstance(members, dict):
                for key, val in members.items():
                    self.make_member(key, val)
            elif isinstance(members, list):
                for item in members:
                    self.append(item)
            elif isinstance(members, (EnumMember, str, tuple)):
                self.append(members)
            else:
                raise TypeError('Invalid argument type for "members"')

    def append(self, member: EnumMemberInput) -> "Enum":
        """
        Appends an enumerator to the enum definition.

        Args:
            member: An :class:`EnumMember`, a ``str`` name, or a ``(name, value)`` 2-tuple.

        Returns:
            This :class:`Enum` instance for method chaining.
        """
        if isinstance(member, EnumMember):
            member.parent = self
            self.members.append(member)
        elif isinstance(member, str):
            self.make_member(member)
        elif isinstance(member, tuple) and len(member) == 2:
            name, value = member
            if not isinstance(name, str):
                raise TypeError(f'Expected "str" for tuple member name, got {str(type(name))}')
            self.make_member(name, value)
        else:
            raise TypeError(f'Invalid type for enum member: {str(type(member))}')
        return self

    def make_member(self,
                    name: str,
                    value: int | str | Element | None = None) -> EnumMember:
        """
        Creates a new :class:`EnumMember`, appends it to this enum, and returns it.

        Args:
            name: Enumerator identifier name (without ``prefix``).
            value: Optional explicit integer, string expression, or :class:`Element` value.

        Returns:
            The newly created :class:`EnumMember`.
        """
        member = EnumMember(name, value, prefix=self.prefix)
        member.parent = self
        self.members.append(member)
        return member


class TypeDef(DataType):
    """
    Type definition (typedef)
    """
    def __init__(self,
                 name: str,
                 base_type: str | "DataType" | "Declaration",
                 const: bool = False,
                 pointer: bool = False,
                 volatile: bool = False,
                 array: int | None = None) -> None:
        super().__init__(name)
        self.const = const
        self.volatile = volatile
        self.pointer = pointer
        self.array = array
        self.base_type: DataType | Declaration
        if isinstance(base_type, DataType):
            self.base_type = base_type
        elif isinstance(base_type, str):
            self.base_type = Type(base_type)
        elif isinstance(base_type, Declaration):
            if not isinstance(base_type.element, DataType):
                err_msg = f'base_type: Declaration must declare a type, not {str(type(base_type.element))}'
                raise TypeError(err_msg)
            self.base_type = base_type
        else:
            err_msg = 'base_type: Invalid type, expected "str" | "DataType" | "Declaration",'
            err_msg += ' got {str(type(base_type))}'
            raise TypeError(err_msg)

    def qualifier(self, name: str) -> bool:
        """
        Returns the status of named qualifier
        """
        if name == "const":
            return self.const
        if name == "volatile":
            return self.volatile
        else:
            raise KeyError(name)

    def __str__(self) -> str:
        return self.name or ""


class Variable(Element):
    """
    Variable declaration
    """
    def __init__(self,
                 name: str,
                 data_type: str | DataType | "Declaration",
                 const: bool = False,    # Only used as pointer qualifier
                 pointer: bool = False,
                 extern: bool = False,
                 static: bool = False,
                 array: int | None = None) -> None:
        self.name = name
        self.const = const
        self.pointer = pointer
        self.extern = extern
        self.static = static
        self.array = array
        self.data_type: DataType | Declaration
        if isinstance(data_type, DataType):
            self.data_type = data_type
        elif isinstance(data_type, str):
            self.data_type = Type(data_type)
        elif isinstance(data_type, Declaration):
            if not isinstance(data_type.element, DataType):
                raise TypeError(f"data_type: Declaration must declare a DataType, not {str(type(data_type.element))}")
            self.data_type = data_type
        else:
            raise TypeError(str(type(data_type)))

    def qualifier(self, name: str) -> bool:
        """
        Returns the status of named qualifier
        """
        if name == "const":
            return self.const  # pointer qualifier, not the same as as type qualifier
        if name == "static":
            return self.static
        if name == "extern":
            return self.extern
        else:
            raise KeyError(name)

    def __str__(self) -> str:
        return self.name


class Function(Element):
    """
    Function declaration
    """
    def __init__(self,
                 name: str,
                 return_type: str | DataType | None = None,
                 static: bool = False,
                 const: bool = False,  # const function (as seen in C++)
                 extern: bool = False,
                 params: Variable | list[Variable] | None = None) -> None:
        self.name = name
        self.static = static
        self.const = const
        self.extern = extern
        if isinstance(return_type, DataType):
            self.return_type = return_type
        elif isinstance(return_type, str):
            self.return_type = Type(return_type)
        elif return_type is None:  # None is a synomym for void
            self.return_type = Type("void")
        else:
            raise TypeError(str(type(return_type)))
        self.params: list[Variable] = []
        if params is not None:
            if isinstance(params, Variable):
                self.append(params)
            elif isinstance(params, list):
                for param in params:
                    self.append(param)

    def append(self, param: Variable) -> "Function":
        """
        Adds new function parameter
        """
        if not isinstance(param, (Variable)):
            raise TypeError("Expected Variable or FunctionPtr object")
        self.params.append(param)
        return self

    def make_param(self,
                   name: str,
                   data_type: str | DataType,
                   const: bool = False,
                   pointer: bool = False,
                   array: int | None = None) -> "Function":
        """
        Creates new Variable from arguments and adds as parameter
        """
        param = Variable(name, data_type, const=const, pointer=pointer, array=array)
        return self.append(param)

    def __str__(self) -> str:
        return self.name


class Declaration(Element):
    """
    A declaration element for variables, functions, or data types.

    Args:
        element: The :class:`Variable`, :class:`Function`, or :class:`DataType`
            (including :class:`Struct`, :class:`Union`, :class:`Enum`, or
            :class:`TypeDef`) to declare.
        content: Optional initializer value (when ``element`` is a :class:`Variable`)
            or function body :class:`Block` / :class:`Sequence` (when ``element`` is
            a :class:`Function`).
    """
    def __init__(self,
                 element: Variable | Function | DataType,
                 content: Any | None = None) -> None:
        if isinstance(element, (Variable, Function, DataType)):
            self.element = element
            self.init_value: Any | None = None
            self.body: Block | None = None
        else:
            raise TypeError(f"element: Invalid type '{str(type(element))}'")
        if content is not None:
            if isinstance(element, Variable):
                self.init_value = content
            elif isinstance(element, Function):
                if isinstance(content, Block):
                    self.body = content
                elif isinstance(content, Sequence):
                    block = Block()
                    block.extend(content)
                    self.body = block
                else:
                    raise TypeError(
                        f"Expected Sequence or Block for Function declaration content, got {str(type(content))}"
                    )
            else:
                raise ValueError("content only allowed for Variable or Function declarations")


class FunctionCall(Element):
    """
    Function call expression
    """
    def __init__(self,
                 name: str | Function,
                 args: list[int | float | str | Element] | None = None) -> None:
        if isinstance(name, Function):
            num_given = 0 if args is None else len(args)
            num_expected = len(name.params)
            if num_given != num_expected:
                raise ValueError(
                    f"Function '{name.name}' expects {num_expected} argument(s), got {num_given}"
                )
            self.name = name.name
        elif isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'name: Invalid type, expected "str" | "Function", got {str(type(name))}')
        self.args: list[str | Element] = []
        if args is not None:
            for arg in args:
                self.append(arg)

    def append(self, arg: int | float | str | Element) -> "FunctionCall":
        """
        Appends argument to function call, can be chained
        """
        if isinstance(arg, (int, float)):
            self.args.append(str(arg))
        elif isinstance(arg, (str, Element)):
            self.args.append(arg)
        else:
            raise NotImplementedError(str(type(arg)))
        return self


class FunctionReturn(Element):
    """
    Function return expression
    """
    def __init__(self,
                 expression: int | float | bool | str | Element | None = None) -> None:
        self.expression: str | Element | None
        if expression is None:
            self.expression = None
        elif isinstance(expression, bool):
            self.expression = "true" if expression else "false"
        elif isinstance(expression, (int, float)):
            self.expression = str(expression)
        elif isinstance(expression, (str, Element)):
            self.expression = expression
        else:
            raise NotImplementedError(str(type(expression)))


class Assignment(Element):
    """
    Assignment has a left-hand-side and right-hand-side expressions
    """
    def __init__(self, lhs: Any, rhs: Any) -> None:
        self.lhs = self._check_and_convert(lhs)
        self.rhs = self._check_and_convert(rhs)

    def _check_and_convert(self, elem: Any) -> str | Element:
        if isinstance(elem, bool):
            return "true" if elem else "false"
        elif isinstance(elem, (int, float, str)):
            return str(elem)
        elif isinstance(elem, Element):
            return elem
        else:
            raise NotImplementedError(str(type(elem)))


class Statement(Element):
    """
    A statement can contain one or more expressions
    """
    def __init__(self, expression: Any) -> None:
        parts = []
        if isinstance(expression, (list, tuple)):
            for part in expression:
                parts.append(self._check_and_convert(part))
        else:
            parts.append(self._check_and_convert(expression))
        self.parts = tuple(parts)

    def _check_and_convert(self, elem: Any) -> str | Element:
        if isinstance(elem, bool):
            return "true" if elem else "false"
        elif isinstance(elem, (int, float, str)):
            return str(elem)
        elif isinstance(elem, Element):
            return elem
        else:
            raise NotImplementedError(str(type(elem)))


class StringLiteral(Element):
    """
    String literal
    """
    def __init__(self, text: str) -> None:
        self.text = text


class Sequence:
    """
    A sequence of statements, comments or whitespace
    """
    def __init__(self, elements: Any | list[Any] | None = None) -> None:
        self.elements: list[Comment | Statement | "Sequence" | "IfStatement"] = []
        if elements is not None:
            if isinstance(elements, list):
                for elem in elements:
                    self.append(elem)
            else:
                self.append(elements)

    def __len__(self) -> int:
        return len(self.elements)

    def append(self, elem: Any) -> "Sequence":
        """
        Appends one element to this sequence
        """
        self.elements.append(elem)
        return self

    def extend(self, seq: "Sequence") -> "Sequence":
        """
        Extends this sequence with items from another sequence
        """
        if isinstance(seq, Sequence):
            self.elements.extend(seq.elements)
        else:
            raise TypeError("seq must be of type Sequence")
        return self


class Block(Sequence):
    """
    A sequence wrapped in braces
    """


class IfStatement(Element):
    """
    If / else-if / else statement.

    Args:
        condition: Optional initial ``if`` condition expression (or :class:`Sequence`
            of condition parts).
        branch: Optional initial ``if`` branch (:class:`Statement` for an unbraced
            single-line branch, or :class:`Sequence` / :class:`Block` for a braced block).
    """
    def __init__(self,
                 condition: Any | None = None,
                 branch: Statement | Block | Sequence | None = None) -> None:
        self.conditions: list[Any] = []
        self.branches: list[Statement | Block] = []
        if condition is not None or branch is not None:
            if condition is None or branch is None:
                raise ValueError("Both condition and branch must be provided when initializing IfStatement")
            self.append(condition, branch)

    def append(self,
               condition: Any | None,
               branch: Statement | Block | Sequence) -> "IfStatement":
        """
        Appends a conditional branch, or a final ``else`` branch when ``condition`` is ``None``.

        Args:
            condition: Condition expression for an ``if`` or ``else if`` branch, or ``None``
                for the unconditional final ``else`` branch.
            branch: Branch body (:class:`Statement`, :class:`Sequence`, or :class:`Block`).
                A :class:`Sequence` is automatically converted into a braced :class:`Block`.

        Returns:
            This :class:`IfStatement` instance for method chaining.
        """
        if len(self.conditions) != len(self.branches):
            raise RuntimeError("Cannot append branch after a final else branch (condition=None)")
        if condition is None:
            if len(self.branches) == 0:
                raise ValueError("First branch of IfStatement must have a condition")
        else:
            self.conditions.append(self._check_and_convert_condition(condition))

        if isinstance(branch, Block):
            self.branches.append(branch)
        elif isinstance(branch, Sequence):
            block = Block()
            block.extend(branch)
            self.branches.append(block)
        elif isinstance(branch, Statement):
            self.branches.append(branch)
        else:
            raise TypeError(f"Expected Statement, Sequence, or Block for branch, got {str(type(branch))}")
        return self

    def else_if(self,
                condition: Any,
                branch: Statement | Block | Sequence) -> "IfStatement":
        """
        Appends an ``else if`` branch.

        Args:
            condition: Condition expression for the ``else if`` branch.
            branch: Branch body (:class:`Statement`, :class:`Sequence`, or :class:`Block`).

        Returns:
            This :class:`IfStatement` instance for method chaining.
        """
        if condition is None:
            raise ValueError("else_if requires a condition")
        if len(self.branches) == 0:
            raise RuntimeError("Cannot call else_if before the initial if branch")
        return self.append(condition, branch)

    def else_branch(self,
                    branch: Statement | Block | Sequence) -> "IfStatement":
        """
        Appends the final unconditional ``else`` branch.

        Args:
            branch: Branch body (:class:`Statement`, :class:`Sequence`, or :class:`Block`).

        Returns:
            This :class:`IfStatement` instance for method chaining.
        """
        return self.append(None, branch)

    def _check_and_convert_condition(self, cond: Any) -> Any:
        if isinstance(cond, bool):
            return "true" if cond else "false"
        if isinstance(cond, (int, float, str)):
            return str(cond)
        if isinstance(cond, (Element, Sequence)):
            return cond
        if isinstance(cond, (list, tuple)):
            return [self._check_and_convert_condition(part) for part in cond]
        raise NotImplementedError(str(type(cond)))


class NamedLabel(Element):
    """
    Named label for goto statements
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name


class BreakStatement(Statement):
    """
    Break statement
    """
    def __init__(self) -> None:
        super().__init__("break")


class ContinueStatement(Statement):
    """
    Continue statement
    """
    def __init__(self) -> None:
        super().__init__("continue")


class GotoStatement(Statement):
    """
    Goto statement
    """
    def __init__(self, label: str | NamedLabel) -> None:
        if not isinstance(label, (str, NamedLabel)):
            raise TypeError(f'label: Invalid type, expected "str" | "NamedLabel", got {str(type(label))}')
        super().__init__("goto")
        self.label = label


class ReturnStatement(Statement):
    """
    Return statement
    """
    def __init__(self,
                 expression: int | float | bool | str | Element | None = None) -> None:
        super().__init__(FunctionReturn(expression))


class SwitchLabel(Element):
    """
    Case label inside a switch statement
    """
    def __init__(self, value: int | str | Element) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, str, Element)):
            raise TypeError(f'value: Invalid type, expected "int" | "str" | "Element", got {str(type(value))}')
        self.value: str | Element = str(value) if isinstance(value, int) else value


class SwitchDefault(Element):
    """
    Default label inside a switch statement
    """


class SwitchStatement(Element):
    """
    Switch statement
    """
    def __init__(self,
                 expression: Any,
                 body: Statement | Block | Sequence | None = None) -> None:
        self.expression = self._check_and_convert_expression(expression)
        self.body: Statement | Block
        if body is None:
            self.body = Block()
        elif isinstance(body, Block):
            self.body = body
        elif isinstance(body, Sequence):
            block = Block()
            block.extend(body)
            self.body = block
        elif isinstance(body, Statement):
            self.body = body
        else:
            raise TypeError(f"Expected Statement, Sequence, or Block for body, got {str(type(body))}")

    def _check_and_convert_expression(self, expr: Any) -> str | Element:
        if isinstance(expr, bool):
            return "true" if expr else "false"
        if isinstance(expr, (int, float, str)):
            return str(expr)
        if isinstance(expr, Element):
            return expr
        raise NotImplementedError(str(type(expr)))
