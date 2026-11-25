"""
Factory classes
"""
from collections import namedtuple
from typing import Union, Any
from cfile import core

BuiltInTypes = namedtuple("BuiltInTypes", ["char",
                                           "short",
                                           "int",
                                           "long",
                                           "float",
                                           "double"])

types = BuiltInTypes(core.Type("char"),
                     core.Type("short"),
                     core.Type("int"),
                     core.Type("long"),
                     core.Type("float"),
                     core.Type("double")
                     )


class CFactory:  # pylint: disable=too-many-public-methods
    """
    Factory for creating C language elements and code sequences.
    """

    def blank(self) -> core.Blank:
        """
        Creates a blank line element.

        Returns:
            A new :class:`~cfile.core.Blank` instance.
        """
        return core.Blank()

    def line(self, inner: Any) -> core.Line:
        """
        Creates a single line of code without appending a trailing semicolon ``;``.

        Args:
            inner: A string, :class:`~cfile.core.Element`, or list of parts to write on the line.

        Returns:
            A new :class:`~cfile.core.Line` instance.
        """
        return core.Line(inner)

    def whitespace(self, width: int) -> core.Whitespace:
        """
        Creates horizontal whitespace of a given character width.

        Args:
            width: Number of space characters to emit.

        Returns:
            A new :class:`~cfile.core.Whitespace` instance.
        """
        return core.Whitespace(width)

    def line_comment(self, text: str, adjust: int = 1) -> core.LineComment:
        """
        Creates a single-line comment (``// ...``).

        Args:
            text: The comment text following ``//``.
            adjust: Number of leading spaces to insert when placed after another element on the same line.

        Returns:
            A new :class:`~cfile.core.LineComment` instance.
        """
        return core.LineComment(text, adjust)

    def block_comment(self,
                      text: str | list[str],
                      adjust: int = 1,
                      width: int = 0,
                      line_start: str = "") -> core.BlockComment:
        """
        Creates a block comment (``/* ... */``).

        Args:
            text: Comment text as a single string (may be multi-line) or a list of line strings.
            adjust: Number of leading spaces to insert when placed after another element on the same line.
            width: When ``> 0``, prints a banner of ``width`` asterisks on the opening and closing lines
                and places ``text`` on the lines in between.
            line_start: Prefix prepended to each inner line when ``width > 0`` (e.g. ``"* "``).

        Returns:
            A new :class:`~cfile.core.BlockComment` instance.
        """
        return core.BlockComment(text, adjust, width, line_start)

    def sequence(self, elements: Any | list[Any] | None = None) -> core.Sequence:
        """
        Creates an unbraced sequence of code elements.

        Args:
            elements: Optional initial element or list of elements to append to the sequence.

        Returns:
            A new :class:`~cfile.core.Sequence` instance.
        """
        return core.Sequence(elements)

    def directive(self, text: str) -> core.Directive:
        """
        Creates a custom preprocessor directive (``#<text>``).

        Args:
            text: Directive text following ``#``.

        Returns:
            A new :class:`~cfile.core.Directive` instance.
        """
        return core.Directive(text)

    def include_directive(self, path_to_file: str, sys: bool = False) -> core.IncludeDirective:
        """
        Creates an ``#include`` preprocessor directive.

        Args:
            path_to_file: Header file path to include.
            sys: When ``True``, wraps the path in angle brackets (``#include <...>``);
                when ``False`` (the default), wraps it in double quotes (``#include "..."``).

        Returns:
            A new :class:`~cfile.core.IncludeDirective` instance.
        """
        return core.IncludeDirective(path_to_file, sys=sys)

    def include_next_directive(self, path_to_file: str, sys: bool = False) -> core.IncludeNextDirective:
        """
        Creates an ``#include_next`` preprocessor directive (GCC/Clang extension).

        Args:
            path_to_file: Header file path to include.
            sys: When ``True``, wraps the path in angle brackets (``#include_next <...>``);
                when ``False`` (the default), wraps it in double quotes (``#include_next "..."``).

        Returns:
            A new :class:`~cfile.core.IncludeNextDirective` instance.
        """
        return core.IncludeNextDirective(path_to_file, sys=sys)

    def embed_directive(self,
                        path_to_file: str,
                        sys: bool = False,
                        params: str | list[str] | None = None) -> core.EmbedDirective:
        """
        Creates a C23 ``#embed`` preprocessor directive.

        Args:
            path_to_file: Resource file path to embed.
            sys: When ``True``, wraps the path in angle brackets (``#embed <...>``);
                when ``False`` (the default), wraps it in double quotes (``#embed "..."``).
            params: Optional embed parameter string or list of parameter strings
                (e.g. ``"limit(256)"`` or ``["limit(256)", "if_empty(0)"]``).

        Returns:
            A new :class:`~cfile.core.EmbedDirective` instance.
        """
        return core.EmbedDirective(path_to_file, sys=sys, params=params)

    def define_directive(self, left: str, right: str | int | float | None = None) -> core.DefineDirective:
        """
        Creates a ``#define <left> [right]`` preprocessor directive.

        Args:
            left: Macro name or function-like macro signature (e.g. ``"MAX(a, b)"``).
            right: Optional macro expansion text or value.

        Returns:
            A new :class:`~cfile.core.DefineDirective` instance.
        """
        return core.DefineDirective(left, right)

    def undef_directive(self, identifier: str) -> core.UndefDirective:
        """
        Creates an ``#undef <identifier>`` preprocessor directive.

        Args:
            identifier: Preprocessor macro identifier to undefine.

        Returns:
            A new :class:`~cfile.core.UndefDirective` instance.
        """
        return core.UndefDirective(identifier)

    def if_directive(self, expression: str) -> core.IfDirective:
        """
        Creates an ``#if <expression>`` preprocessor directive.

        Args:
            expression: Constant preprocessor expression to evaluate.

        Returns:
            A new :class:`~cfile.core.IfDirective` instance.
        """
        return core.IfDirective(expression)

    def ifdef_directive(self, identifier: str) -> core.IfdefDirective:
        """
        Creates an ``#ifdef <identifier>`` preprocessor directive.

        Args:
            identifier: Preprocessor macro identifier to test.

        Returns:
            A new :class:`~cfile.core.IfdefDirective` instance.
        """
        return core.IfdefDirective(identifier)

    def ifndef_directive(self, identifier: str) -> core.IfndefDirective:
        """
        Creates an ``#ifndef <identifier>`` preprocessor directive.

        Args:
            identifier: Preprocessor macro identifier to test.

        Returns:
            A new :class:`~cfile.core.IfndefDirective` instance.
        """
        return core.IfndefDirective(identifier)

    def elif_directive(self, expression: str) -> core.ElifDirective:
        """
        Creates an ``#elif <expression>`` preprocessor directive.

        Args:
            expression: Constant preprocessor expression to evaluate.

        Returns:
            A new :class:`~cfile.core.ElifDirective` instance.
        """
        return core.ElifDirective(expression)

    def elifdef_directive(self, identifier: str) -> core.ElifdefDirective:
        """
        Creates a C23 ``#elifdef <identifier>`` preprocessor directive.

        Args:
            identifier: Preprocessor macro identifier to test.

        Returns:
            A new :class:`~cfile.core.ElifdefDirective` instance.
        """
        return core.ElifdefDirective(identifier)

    def elifndef_directive(self, identifier: str) -> core.ElifndefDirective:
        """
        Creates a C23 ``#elifndef <identifier>`` preprocessor directive.

        Args:
            identifier: Preprocessor macro identifier to test.

        Returns:
            A new :class:`~cfile.core.ElifndefDirective` instance.
        """
        return core.ElifndefDirective(identifier)

    def else_directive(self) -> core.ElseDirective:
        """
        Creates an ``#else`` preprocessor directive.

        Returns:
            A new :class:`~cfile.core.ElseDirective` instance.
        """
        return core.ElseDirective()

    def endif_directive(self) -> core.EndifDirective:
        """
        Creates an ``#endif`` preprocessor directive.

        Returns:
            A new :class:`~cfile.core.EndifDirective` instance.
        """
        return core.EndifDirective()

    def line_directive(self, line_number: int | str, filename: str | None = None) -> core.LineDirective:
        """
        Creates a ``#line <line_number> ["<filename>"]`` preprocessor directive.

        Args:
            line_number: Line number to set.
            filename: Optional source filename string.

        Returns:
            A new :class:`~cfile.core.LineDirective` instance.
        """
        return core.LineDirective(line_number, filename)

    def error_directive(self, message: str = "") -> core.ErrorDirective:
        """
        Creates an ``#error [message]`` preprocessor directive.

        Args:
            message: Diagnostic error message text.

        Returns:
            A new :class:`~cfile.core.ErrorDirective` instance.
        """
        return core.ErrorDirective(message)

    def warning_directive(self, message: str = "") -> core.WarningDirective:
        """
        Creates a ``#warning [message]`` preprocessor directive (C23 and compiler extension).

        Args:
            message: Diagnostic warning message text.

        Returns:
            A new :class:`~cfile.core.WarningDirective` instance.
        """
        return core.WarningDirective(message)

    def pragma_directive(self, tokens: str = "") -> core.PragmaDirective:
        """
        Creates a ``#pragma [tokens]`` preprocessor directive.

        Args:
            tokens: Pragma tokens following ``#pragma`` (e.g. ``"once"``).

        Returns:
            A new :class:`~cfile.core.PragmaDirective` instance.
        """
        return core.PragmaDirective(tokens)

    def extern(self, language: str) -> core.Extern:
        """
        Creates an ``extern "<language>"`` linkage specification (e.g. ``extern "C"``).

        Args:
            language: Language linkage string (such as ``"C"``).

        Returns:
            A new :class:`~cfile.core.Extern` instance.
        """
        return core.Extern(language)

    def block(self, elements: Any | list[Any] | None = None) -> core.Block:
        """
        Creates a brace-enclosed block sequence (``{ ... }``).

        Args:
            elements: Optional initial element or list of elements inside the block.

        Returns:
            A new :class:`~cfile.core.Block` instance.
        """
        return core.Block(elements)

    def function(self,
                 name: str,
                 return_type: str | core.DataType | None = None,
                 static: bool = False,
                 const: bool = False,  # This is not const of the return type
                 extern: bool = False,
                 params: core.Variable | list[core.Variable] | None = None) -> core.Function:
        """
        Creates a function entity.

        Wrap the returned object in :meth:`declaration` to emit its prototype or header,
        or pass it to :meth:`fn_call` to invoke it.

        Args:
            name: Function identifier name.
            return_type: Return data type name or :class:`~cfile.core.DataType`
                (defaults to ``"void"`` when ``None``).
            static: When ``True``, adds the ``static`` storage class specifier.
            const: When ``True``, marks the function ``const`` (C++).
            extern: When ``True``, adds the ``extern`` storage class specifier.
            params: Optional single :class:`~cfile.core.Variable` or list of parameter variables.

        Returns:
            A new :class:`~cfile.core.Function` instance.
        """
        return core.Function(name, return_type, static, const, extern, params)

    def type(self,
             type_ref: str | core.Type,
             const: bool = False,
             pointer: bool = False,
             volatile: bool = False,
             array: int | None = None) -> core.Type:
        """
        Creates a C data type reference.

        Args:
            type_ref: Base type name (e.g. ``"int"``, ``"char"``) or nested :class:`~cfile.core.Type`.
            const: When ``True``, qualifies the type with ``const``.
            pointer: When ``True``, makes the type a pointer (``*``).
            volatile: When ``True``, qualifies the type with ``volatile``.
            array: Optional array dimension size.

        Returns:
            A new :class:`~cfile.core.Type` instance.
        """
        return core.Type(type_ref, const, pointer, volatile, array)

    def struct_member(self,
                      name: str,
                      data_type: str | core.DataType | core.Declaration,
                      const: bool = False,  # Pointer qualifier only
                      pointer: bool = False,
                      array: int | None = None) -> core.StructMember:
        """
        Creates a struct member field.

        Args:
            name: Field identifier name.
            data_type: Field data type name, :class:`~cfile.core.DataType`, or nested struct/union
                :class:`~cfile.core.Declaration`.
            const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
            pointer: When ``True``, declares the field as a pointer to ``data_type``.
            array: Optional array dimension size (emits ``name[array]``).

        Returns:
            A new :class:`~cfile.core.StructMember` instance.
        """
        return core.StructMember(name, data_type, const, pointer, array)

    def struct(self,
               name: str | None = None,
               members: core.StructMember | list[core.StructMember] | None = None
               ) -> core.Struct:
        """
        Creates a C ``struct`` type entity.

        When used directly in a statement, emits a forward declaration or type reference
        (``struct <name>``). When wrapped in :meth:`declaration`, emits the full struct
        definition with its members.

        Args:
            name: Optional struct tag name (``None`` for an anonymous ``struct``).
            members: Optional single :class:`~cfile.core.StructMember` or list of struct members.

        Returns:
            A new :class:`~cfile.core.Struct` instance.
        """
        return core.Struct(name, members)

    def union_member(self,
                     name: str,
                     data_type: str | core.DataType | core.Declaration,
                     const: bool = False,  # Pointer qualifier only
                     pointer: bool = False,
                     array: int | None = None) -> core.UnionMember:
        """
        Creates a union member field.

        Args:
            name: Field identifier name.
            data_type: Field data type name, :class:`~cfile.core.DataType`, or nested struct/union
                :class:`~cfile.core.Declaration`.
            const: When ``True`` (with ``pointer=True``), qualifies the pointer as ``* const``.
            pointer: When ``True``, declares the field as a pointer to ``data_type``.
            array: Optional array dimension size (emits ``name[array]``).

        Returns:
            A new :class:`~cfile.core.UnionMember` instance.
        """
        return core.UnionMember(name, data_type, const, pointer, array)

    def union(self,
              name: str | None = None,
              members: core.StructMember | list[core.StructMember] | None = None
              ) -> core.Union:
        """
        Creates a C ``union`` type entity.

        When used directly in a statement, emits a forward declaration or type reference
        (``union <name>``). When wrapped in :meth:`declaration`, emits the full union
        definition with its members.

        Args:
            name: Optional union tag name (``None`` for an anonymous ``union``).
            members: Optional single :class:`~cfile.core.UnionMember` / :class:`~cfile.core.StructMember`
                or list of members.

        Returns:
            A new :class:`~cfile.core.Union` instance.
        """
        return core.Union(name, members)

    def enum_member(self,
                    name: str,
                    value: int | str | core.Element | None = None,
                    prefix: str = "") -> core.EnumMember:
        """
        Creates an ``enum`` member constant.

        Args:
            name: Enumerator identifier name (without ``prefix``).
            value: Optional explicit integer, string expression, or :class:`~cfile.core.Element` value.
            prefix: Optional prefix prepended to ``name`` when rendered.

        Returns:
            A new :class:`~cfile.core.EnumMember` instance.
        """
        return core.EnumMember(name, value, prefix)

    def enum(self,
             name: str | None = None,
             members: (
                 core.EnumMemberInput
                 | list[core.EnumMemberInput]
                 | dict[str, int | str | core.Element | None]
                 | None
             ) = None,
             prefix: str = "") -> core.Enum:
        """
        Creates a C ``enum`` type entity.

        When used directly in a statement or variable type, emits ``enum <name>``.
        When wrapped in :meth:`declaration`, emits the full ``enum`` definition with
        its enumerator list.

        Args:
            name: Optional enum tag name (``None`` for an anonymous ``enum``).
            members: Optional initial enumerator(s). Accepts a single
                :class:`~cfile.core.EnumMember`, ``str``, or ``(name, value)`` tuple;
                a list of any of those; or a ``dict`` mapping enumerator names to values.
            prefix: Optional prefix string automatically prepended to every member's
                name when declared or referenced.

        Returns:
            A new :class:`~cfile.core.Enum` instance.
        """
        return core.Enum(name, members, prefix)

    def variable(self,
                 name: str,
                 data_type: str | core.DataType | core.Declaration,
                 const: bool = False,    # Only used as pointer qualifier
                 pointer: bool = False,
                 extern: bool = False,
                 static: bool = False,
                 array: int | None = None) -> core.Variable:
        """
        Creates a C variable entity.

        Wrap the returned object in :meth:`declaration` to declare the variable, or pass it
        directly to expressions, statements, function calls, or Python f-strings to emit
        its identifier name.

        Args:
            name: Variable identifier name.
            data_type: Variable type name, :class:`~cfile.core.DataType` (including
                :class:`~cfile.core.Type`, :class:`~cfile.core.Struct`, :class:`~cfile.core.Union`,
                or :class:`~cfile.core.TypeDef`), or inline struct/union :class:`~cfile.core.Declaration`.
            const: When ``True`` (with ``pointer=True``), qualifies the pointer itself as ``* const``.
                To declare a pointer to a ``const`` value (``const int *x``), set ``const=True`` on
                the ``data_type`` via :meth:`type` instead.
            pointer: When ``True``, declares the variable as a pointer to ``data_type``.
            extern: When ``True``, adds the ``extern`` storage class specifier.
            static: When ``True``, adds the ``static`` storage class specifier.
            array: Optional array dimension size (emits ``name[array]``).

        Returns:
            A new :class:`~cfile.core.Variable` instance.
        """
        return core.Variable(name, data_type, const, pointer, extern, static, array)

    def typedef(self,
                name: str,
                base_type: str | core.DataType | core.Declaration,
                const: bool = False,    # Only used as pointer qualifier
                pointer: bool = False,
                volatile: bool = False,
                array: int | None = None) -> core.TypeDef:
        """
        Creates a ``typedef`` type alias entity.

        Wrap the returned object in :meth:`declaration` to emit the ``typedef`` declaration,
        or pass the object as the ``data_type`` of a :meth:`variable` to reference the alias name.

        Args:
            name: New typedef alias name.
            base_type: Target type name, :class:`~cfile.core.DataType`, or inline struct
                :class:`~cfile.core.Declaration`.
            const: When ``True``, adds the ``const`` qualifier.
            pointer: When ``True``, makes the typedef a pointer to ``base_type``.
            volatile: When ``True``, adds the ``volatile`` qualifier.
            array: Optional array dimension size.

        Returns:
            A new :class:`~cfile.core.TypeDef` instance.
        """
        return core.TypeDef(name, base_type, const, pointer, volatile, array)

    def statement(self, expression: Any) -> core.Statement:
        """
        Wraps an expression or declaration in a semicolon-terminated C statement.

        Args:
            expression: Expression, :class:`~cfile.core.Element`, string, or tuple/list of parts.

        Returns:
            A new :class:`~cfile.core.Statement` instance.
        """
        return core.Statement(expression)

    def assignment(self, lhs: Any, rhs: Any) -> core.Assignment:
        """
        Creates an assignment expression (``<lhs> = <rhs>``).

        Args:
            lhs: Left-hand side variable or expression.
            rhs: Right-hand side value or expression.

        Returns:
            A new :class:`~cfile.core.Assignment` instance.
        """
        return core.Assignment(lhs, rhs)

    def str_literal(self, text: str) -> core.StringLiteral:
        """
        Creates a double-quoted C string literal (``"<text>"``).

        Args:
            text: Raw string contents inside the quotes.

        Returns:
            A new :class:`~cfile.core.StringLiteral` instance.
        """
        return core.StringLiteral(text)

    arg_types = int | float | str | core.Element

    def fn_call(self,
                name: str | core.Function,
                args: list[arg_types] | arg_types | None = None) -> core.FunctionCall:
        """
        Creates a function call expression (``<name>(<args>)``).

        Args:
            name: Function name as a ``str``, or a :class:`~cfile.core.Function` object.
                When a :class:`~cfile.core.Function` is provided, the number of supplied
                arguments is validated against ``len(name.params)``.
            args: Optional single argument or list of arguments.

        Returns:
            A new :class:`~cfile.core.FunctionCall` instance.
        """
        if args is None:
            return core.FunctionCall(name, None)
        elif isinstance(args, list):
            return core.FunctionCall(name, args)
        else:
            return core.FunctionCall(name, [args])

    def func_call(self,
                  name: str | core.Function,
                  args: list[arg_types] | arg_types | None = None) -> core.FunctionCall:
        """
        Alias for :meth:`fn_call`.

        Args:
            name: Function name as a ``str``, or a :class:`~cfile.core.Function` object.
            args: Optional single argument or list of arguments.

        Returns:
            A new :class:`~cfile.core.FunctionCall` instance.
        """
        return self.fn_call(name, args)

    def fn_return(self, expression: int | float | bool | str | core.Element | None = None) -> core.FunctionReturn:
        """
        Creates a ``return`` expression (to be wrapped in :meth:`statement`).

        Args:
            expression: Optional return value or expression. When ``None``, emits a
                void ``return``.

        Returns:
            A new :class:`~cfile.core.FunctionReturn` instance.
        """
        return core.FunctionReturn(expression)

    def func_return(self, expression: int | float | bool | str | core.Element | None = None) -> core.FunctionReturn:
        """
        Alias for :meth:`fn_return`.

        Args:
            expression: Optional return value or expression.

        Returns:
            A new :class:`~cfile.core.FunctionReturn` instance.
        """
        return self.fn_return(expression)

    def return_statement(self,
                         expression: int | float | bool | str | core.Element | None = None) -> core.ReturnStatement:
        """
        Creates a complete semicolon-terminated ``return`` statement.

        Args:
            expression: Optional return value or expression. When ``None``, emits ``return;``.

        Returns:
            A new :class:`~cfile.core.ReturnStatement` instance.
        """
        return core.ReturnStatement(expression)

    def declaration(self,
                    element: core.Variable | core.Function | core.DataType,
                    content: Any | None = None) -> core.Declaration:
        """
        Wraps a variable, function, struct, union, enum, or typedef to emit its full C declaration.

        Args:
            element: The :class:`~cfile.core.Variable`, :class:`~cfile.core.Function`, or
                :class:`~cfile.core.DataType` to declare.
            content: Optional initial value (when ``element`` is a :class:`~cfile.core.Variable`)
                or function body :class:`~cfile.core.Block` / :class:`~cfile.core.Sequence`
                (when ``element`` is a :class:`~cfile.core.Function`).

        Returns:
            A new :class:`~cfile.core.Declaration` instance.
        """
        return core.Declaration(element, content)

    def if_statement(self,
                     condition: Any | None = None,
                     branch: Union[core.Statement, core.Block, core.Sequence, None] = None) -> core.IfStatement:
        """
        Creates an ``if / else if / else`` statement.

        Additional branches can be chained using :meth:`~cfile.core.IfStatement.else_if`,
        :meth:`~cfile.core.IfStatement.else_branch`, or :meth:`~cfile.core.IfStatement.append`.

        Args:
            condition: Optional initial ``if`` condition expression (or :class:`~cfile.core.Sequence`
                of condition parts).
            branch: Optional initial ``if`` branch (:class:`~cfile.core.Statement` for an unbraced
                single-line branch, or :class:`~cfile.core.Sequence` / :class:`~cfile.core.Block`
                for a brace-enclosed block).

        Returns:
            A new :class:`~cfile.core.IfStatement` instance.
        """
        return core.IfStatement(condition, branch)

    def break_statement(self) -> core.BreakStatement:
        """
        Creates a ``break;`` statement.

        Returns:
            A new :class:`~cfile.core.BreakStatement` instance.
        """
        return core.BreakStatement()

    def continue_statement(self) -> core.ContinueStatement:
        """
        Creates a ``continue;`` statement.

        Returns:
            A new :class:`~cfile.core.ContinueStatement` instance.
        """
        return core.ContinueStatement()

    def named_label(self, name: str) -> core.NamedLabel:
        """
        Creates a named target label (``<name>:``) for ``goto`` statements.

        Args:
            name: Label identifier name.

        Returns:
            A new :class:`~cfile.core.NamedLabel` instance.
        """
        return core.NamedLabel(name)

    def goto_statement(self, label: str | core.NamedLabel) -> core.GotoStatement:
        """
        Creates a ``goto <label>;`` statement.

        Args:
            label: Target label name as a ``str`` or a :class:`~cfile.core.NamedLabel` instance.

        Returns:
            A new :class:`~cfile.core.GotoStatement` instance.
        """
        return core.GotoStatement(label)

    def switch_label(self, value: int | str | core.Element) -> core.SwitchLabel:
        """
        Creates a ``case <value>:`` label for use inside a ``switch`` body.

        Args:
            value: Case constant (integer, string identifier, or :class:`~cfile.core.Element`).

        Returns:
            A new :class:`~cfile.core.SwitchLabel` instance.
        """
        return core.SwitchLabel(value)

    def switch_default(self) -> core.SwitchDefault:
        """
        Creates a ``default:`` label for use inside a ``switch`` body.

        Returns:
            A new :class:`~cfile.core.SwitchDefault` instance.
        """
        return core.SwitchDefault()

    def switch(self,
               expression: Any,
               body: Union[core.Statement, core.Block, core.Sequence, None] = None) -> core.SwitchStatement:
        """
        Creates a ``switch (<expression>)`` statement.

        Args:
            expression: Controlling expression evaluated by the ``switch``.
            body: Body of the ``switch`` (typically a :class:`~cfile.core.Block` or
                :class:`~cfile.core.Sequence` containing :class:`~cfile.core.SwitchLabel`,
                :class:`~cfile.core.SwitchDefault`, and statements).

        Returns:
            A new :class:`~cfile.core.SwitchStatement` instance.
        """
        return core.SwitchStatement(expression, body)

    def switch_statement(self,
                         expression: Any,
                         body: Union[core.Statement, core.Block, core.Sequence, None] = None) -> core.SwitchStatement:
        """
        Alias for :meth:`switch`.

        Args:
            expression: Controlling expression evaluated by the ``switch``.
            body: Body of the ``switch``.

        Returns:
            A new :class:`~cfile.core.SwitchStatement` instance.
        """
        return core.SwitchStatement(expression, body)
