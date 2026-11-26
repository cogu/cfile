"""
cfile writer
"""
# pylint: disable=consider-using-with
from io import StringIO
from typing import TextIO, Any, Callable
from cfile import core
import cfile.style as c_style


class Formatter:
    """
    Low-level text buffer and indentation manager used by :class:`Writer`.

    Args:
        indent_width: Number of indentation characters per indentation level.
        indentation_char: Character used for indentation (typically ``" "`` or ``"\\t"``).
    """
    def __init__(self, indent_width: int,
                 indentation_char: str) -> None:
        self.file_path: str | None = None
        self.fh: TextIO = StringIO()  # pylint: disable=invalid-name
        self.indentation_char: str = indentation_char
        self.white_space_char: str = " "
        self.indent_width = indent_width  # Number of characters (spaces) per indendation
        self.indentation_level: int = 0  # current indentation level
        self.indentation_str: str = ""
        self.line_number: int = 0
        self.column: int = 0

    def _str_open(self) -> None:
        self.fh = StringIO()
        self.line_number = 1
        self.column = 0
        self.indentation_level = 0
        self.indentation_str = ""

    def _open(self, file_path: str) -> None:
        self.fh = open(file_path, "w", encoding="utf-8")
        self.file_path = file_path
        self.line_number = 1
        self.column = 0
        self.indentation_level = 0
        self.indentation_str = ""

    def _close(self) -> None:
        self.fh.close()

    def _indent(self) -> None:
        self.indentation_level += 1
        self.indentation_str = self.indentation_char * \
            (self.indentation_level * self.indent_width)

    def _dedent(self) -> None:
        self.indentation_level -= 1
        if self.indentation_level == 0:
            self.indentation_str = ""
        else:
            self.indentation_str = self.indentation_char * \
                (self.indentation_level * self.indent_width)

    def _start_line(self) -> None:
        self.fh.write(self.indentation_str)

    def _write(self, text: str) -> None:
        self.fh.write(text)
        self.column += len(text)

    def _write_line(self, text: str) -> None:
        self.fh.write(text)
        self._eol()

    def _eol(self) -> None:
        self.fh.write("\n")
        self.line_number += 1
        self.column = 0


class Writer(Formatter):
    """
    High-level C code generator that renders a :class:`~cfile.core.Sequence` or
    single :class:`~cfile.core.Element` into formatted C source code.

    Args:
        style: Formatting options controlling brace placement, indentation, pointer
            alignment, and label indentation. When ``None``, a default
            :class:`~cfile.style.StyleOptions` instance is used.
    """
    def __init__(self, style: c_style.StyleOptions | None = None) -> None:
        if style is None:
            style = c_style.StyleOptions()
        super().__init__(style.indent_width, style.indent_char)
        self.style = style
        self.switcher_all: dict[str, Callable[[Any], None]] = {
            "Type": self._write_base_type,
            "TypeDef": self._write_typedef_usage,
            "Struct": self._write_struct_usage,
            "Union": self._write_union_usage,
            "Enum": self._write_enum_usage,
            "EnumMember": self._write_enum_member_usage,
            "Variable": self._write_variable_usage,
            "Function": self._write_function_usage,
            "Declaration": self._write_declaration,
            "MultiDeclaration": self._write_multi_declaration,
            "Assignment": self._write_assignment,
            "StringLiteral": self._write_string_literal,
            "FunctionReturn": self._write_func_return,
            "FunctionCall": self._write_func_call,
            "Blank": self._write_blank,
            "Whitespace": self._write_whitespace,
            "LineComment": self._write_line_comment,
            "BlockComment": self._write_block_comment,
            "Sequence": self._write_block,
            "Statement": self._write_statement,
            "BreakStatement": self._write_statement,
            "ContinueStatement": self._write_statement,
            "GotoStatement": self._write_statement,
            "ReturnStatement": self._write_statement,
            "IfStatement": self._write_if_statement,
            "NamedLabel": self._write_named_label,
            "SwitchLabel": self._write_switch_label,
            "SwitchDefault": self._write_switch_default,
            "SwitchStatement": self._write_switch_statement,
            "WhileStatement": self._write_while_statement,
            "DoWhileStatement": self._write_do_while_statement,
            "ForStatement": self._write_for_statement,
            "Line": self._write_line_element,
            "Directive": self._write_directive,
            "IncludeDirective": self._write_directive,
            "IncludeNextDirective": self._write_directive,
            "EmbedDirective": self._write_directive,
            "DefineDirective": self._write_directive,
            "UndefDirective": self._write_directive,
            "IfDirective": self._write_directive,
            "IfdefDirective": self._write_directive,
            "IfndefDirective": self._write_directive,
            "ElifDirective": self._write_directive,
            "ElifdefDirective": self._write_directive,
            "ElifndefDirective": self._write_directive,
            "ElseDirective": self._write_directive,
            "EndifDirective": self._write_directive,
            "LineDirective": self._write_directive,
            "ErrorDirective": self._write_directive,
            "WarningDirective": self._write_directive,
            "PragmaDirective": self._write_directive,
            "Extern": self._write_extern,
        }
        self._pp_stack: list[int] = []
        self._next_ifndef_is_guard: bool = False

    def write_file(self, sequence: core.Sequence, file_path: str) -> None:
        """
        Writes a sequence of C code elements to a file on disk using the configured format style.

        The generated file always ends with a trailing newline.

        Args:
            sequence: The code sequence to render.
            file_path: Destination file path to write (UTF-8 encoded).
        """
        self._open(file_path)
        self._write_sequence(sequence)
        self._close()

    def write_str(self, sequence: core.Sequence, trim_end: bool = True) -> str:
        """
        Writes a sequence of C code elements to a string using the configured format style.

        Args:
            sequence: The code sequence to render.
            trim_end: When ``True`` (the default), removes the trailing newline ``"\\n"``
                at the end of the rendered output so the returned string can be passed
                directly to ``print()`` without producing an extra blank line. Set to
                ``False`` to preserve the trailing newline.

        Returns:
            The rendered C source code as a string.
        """
        assert isinstance(sequence, core.Sequence)
        self._str_open()
        self._pp_stack = []
        self._next_ifndef_is_guard = False
        self._write_sequence(sequence)
        assert isinstance(self.fh, StringIO)
        value = self.fh.getvalue()
        return value.removesuffix("\n") if trim_end else value

    def write_str_elem(self, elem: Any, trim_end: bool = True) -> str:
        """
        Writes a single C code element to a string using the configured format style.

        Args:
            elem: A single :class:`~cfile.core.Element` or :class:`~cfile.core.Block`
                to render.
            trim_end: When ``True`` (the default), removes any trailing newline ``"\\n"``
                from the end of the rendered element string. Set to ``False`` to preserve
                the trailing newline.

        Returns:
            The rendered C element as a string.
        """
        self._str_open()
        self._pp_stack = []
        self._next_ifndef_is_guard = False
        self._write_element(elem)
        assert isinstance(self.fh, StringIO)
        value = self.fh.getvalue()
        return value.removesuffix("\n") if trim_end else value

    def _write_element(self, elem: Any) -> None:
        class_name = elem.__class__.__name__
        write_method = self.switcher_all.get(class_name, None)
        if write_method is not None:
            write_method(elem)
        else:
            raise NotImplementedError(f"Found no writer for element {class_name}")

    def _write_sequence(self, sequence: core.Sequence) -> None:
        """
        Writes a sequence
        """
        num_elements = len(sequence.elements)
        for i, elem in enumerate(sequence.elements):
            if isinstance(elem, list):
                tmp = core.Line(elem)
                self._start_line()
                self._write_line_element(tmp)
            elif isinstance(elem, core.Function):
                self._start_line()
                self._write_function_usage(elem)
            elif isinstance(elem, core.Statement):
                self._start_line()
                self._write_statement(elem)
                self._eol()
            elif isinstance(elem, core.LineComment):
                self._start_line()
                self._write_line_comment(elem)
                self._eol()
            elif isinstance(elem, (core.SwitchLabel, core.SwitchDefault)):
                next_is_block = (i + 1 < num_elements) and isinstance(sequence.elements[i + 1], core.Sequence)
                self._write_case_element_in_sequence(elem, next_is_block)
            elif isinstance(elem, core.NamedLabel):
                self._write_named_label_in_sequence(elem)
            elif isinstance(elem, core.Sequence):
                prev_elem = sequence.elements[i - 1] if i > 0 else None
                self._write_block_in_sequence(elem, prev_elem)
            elif isinstance(elem, core.Line):
                self._start_line()
                self._write_line_element(elem)
            elif isinstance(elem, core.Directive):
                if self._is_include_guard(sequence, i):
                    self._next_ifndef_is_guard = True
                self._start_line()
                self._write_directive(elem)
                self._eol()
            else:
                self._start_line()
                class_name = elem.__class__.__name__
                write_method = self.switcher_all.get(class_name, None)
                if write_method is not None:
                    write_method(elem)
                else:
                    raise NotImplementedError(f"Found no writer for element {class_name}")

    def _is_include_guard(self, sequence: core.Sequence, index: int) -> bool:
        if len(self._pp_stack) != 0 or index + 1 >= len(sequence.elements):
            return False
        elem = sequence.elements[index]
        next_elem = sequence.elements[index + 1]
        return (
            isinstance(elem, core.IfndefDirective)
            and isinstance(next_elem, core.DefineDirective)
            and next_elem.left == elem.identifier
            and next_elem.right is None
        )

    def _write_case_element_in_sequence(self,
                                        elem: core.SwitchLabel | core.SwitchDefault,
                                        next_is_block: bool) -> None:
        outdented = self.indentation_level > 0
        if outdented:
            self._dedent()
        self._start_line()
        if isinstance(elem, core.SwitchLabel):
            self._write_switch_label(elem)
        else:
            self._write_switch_default(elem)
        if outdented:
            self._indent()
        attach_case_block = (
            next_is_block
            and not self.style.brace_wrapping.after_case_label
            and not self.style.indent_case_blocks
        )
        if not attach_case_block:
            self._eol()

    def _write_named_label_in_sequence(self, elem: core.NamedLabel) -> None:
        if not self.style.indent_goto_labels:
            label_indent = ""
        else:
            label_level = max(0, self.indentation_level - 1)
            label_indent = self.indentation_char * (label_level * self.indent_width)
        self._write(label_indent)
        self._write_named_label(elem)
        self._eol()

    def _write_block_in_sequence(self, elem: core.Sequence, prev_elem: Any) -> None:
        prev_is_func_decl = (
            isinstance(prev_elem, core.Declaration)
            and isinstance(prev_elem.element, core.Function)
            and prev_elem.body is None
        )
        prev_is_case_label = isinstance(prev_elem, (core.SwitchLabel, core.SwitchDefault))

        if prev_is_func_decl:
            if self.style.brace_wrapping.after_function:
                self._eol()
                self._start_line()
                self._write_block(elem)
            else:
                self._write(" ")
                self._write_block(elem)
        elif prev_is_case_label:
            if not self.style.brace_wrapping.after_case_label and not self.style.indent_case_blocks:
                outdented = self.indentation_level > 0
                if outdented:
                    self._dedent()
                self._write(" ")
                self._write_block(elem)
                if outdented:
                    self._indent()
            elif not self.style.indent_case_blocks:
                outdented = self.indentation_level > 0
                if outdented:
                    self._dedent()
                self._start_line()
                self._write_block(elem)
                if outdented:
                    self._indent()
            else:
                self._start_line()
                self._write_block(elem)
        else:
            self._start_line()
            self._write_block(elem)

    def _write_line_element(self, elem: core.Line) -> None:
        for i, part in enumerate(elem.parts):
            if i > 0 and not isinstance(part, core.Comment):
                self._write(" ")
            self._write_line_part(part)
        self._eol()

    def _write_line_part(self, elem: str | core.Element) -> None:
        if isinstance(elem, core.Element):
            class_name = elem.__class__.__name__
            write_method = self.switcher_all.get(class_name, None)
            if write_method is not None:
                write_method(elem)
            else:
                raise NotImplementedError(f"Found no writer for element {class_name}")
        elif isinstance(elem, str):
            self._write(elem)
        else:
            raise NotImplementedError(str(type(elem)))

    def _write_blank(self, white_space: core.Blank) -> None:  # pylint: disable=unused-argument
        """
        Writes blank line
        """
        self._write_line("")

    def _write_whitespace(self, white_space: core.Whitespace) -> None:
        """
        Writes whitespace
        """
        self._write(self.white_space_char * white_space.width)

    def _write_line_comment(self, elem: core.LineComment) -> None:
        """
        Writes line comment
        """
        if self.column > 0:
            self._write(" " * elem.adjust)
        if isinstance(elem.text, str):
            self._write("//" + elem.text)
        else:
            raise NotImplementedError("list of strings not yet supported")

    def _write_block_comment(self, elem: core.BlockComment) -> None:
        """
        Writes block comment
        """
        if self.column > 0:
            self._write(" " * elem.adjust)
        if isinstance(elem.text, str):
            lines = elem.text.splitlines()
        elif isinstance(elem.text, list):
            lines = elem.text
        else:
            raise TypeError("Unsupported type", str(type(elem.text)))
        if elem.width == 0:
            self._format_block_comment(lines, False, 1, "")
        else:
            self._format_block_comment(lines, True, elem.width, elem.line_start)

    def _format_block_comment(self, lines: list[str], wrap_text: bool, width: int, line_start: str) -> None:
        self._write(f"/{'*'*width}")
        if wrap_text:
            self._eol()
            for line in lines:
                self._write_line(line_start + line)
            self._write_line(f"{'*'*(width+1)}/")
        else:
            for line in lines[:-1]:
                self._write_line(line_start + line)
            self._write(lines[-1] + f"{'*'*width}/")

    def _write_declaration(self, elem: core.Declaration) -> None:
        """
        Declares type, typedef, variable or function
        """
        if isinstance(elem.element, core.Type):
            self._write_type_declaration(elem.element)
        elif isinstance(elem.element, core.TypeDef):
            self._write_typedef_declaration(elem.element)
        elif isinstance(elem.element, core.Struct):
            self._write_struct_declaration(elem.element)
        elif isinstance(elem.element, core.Union):
            self._write_union_declaration(elem.element)
        elif isinstance(elem.element, core.Enum):
            self._write_enum_declaration(elem.element)
        elif isinstance(elem.element, core.Variable):
            self._write_variable_declaration(elem.element)
        elif isinstance(elem.element, core.Function):
            self._write_function_declaration(elem.element)
            if elem.body is not None:
                if self.style.brace_wrapping.after_function:
                    self._eol()
                    self._start_line()
                    self._write_block(elem.body)
                else:
                    self._write(" ")
                    self._write_block(elem.body)
        else:
            raise NotImplementedError(str(type(elem.element)))
        if elem.init_value is not None:
            self._write(" = ")
            self._write_initializer(elem.init_value)

    def _write_multi_declaration(self, elem: core.MultiDeclaration) -> None:
        """
        Writes a multi-variable declaration sharing a common base type
        """
        for i, decl in enumerate(elem.declarations):
            if i == 0:
                self._write_declaration(decl)
            else:
                self._write(", ")
                assert isinstance(decl.element, core.Variable)
                self._write_secondary_variable_declarator(decl.element)
                if decl.init_value is not None:
                    self._write(" = ")
                    self._write_initializer(decl.init_value)

    def _write_secondary_variable_declarator(self, elem: core.Variable) -> None:
        result = ""
        if elem.pointer:
            if elem.const:
                if self.style.space_around_pointer_qualifiers == c_style.SpaceLocation.DEFAULT:
                    if self.style.pointer_alignment == c_style.Alignment.RIGHT:
                        result += "*const "
                    else:
                        result += "* const "
                else:
                    raise NotImplementedError("Only default space location supported for pointer qualifiers")
            else:
                if self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                    result += "* "
                else:
                    result += "*"
        result += elem.name
        if elem.array is not None:
            result += f"[{elem.array}]"
        self._write(result)

    def _write_initializer(self, value: Any) -> None:
        """
        Writes initializer
        """
        if isinstance(value, list):
            self._write("{")
            for i, member in enumerate(value):
                if i > 0:
                    self._write(", ")
                self._write_initializer(member)
            self._write("}")
        elif isinstance(value, dict):
            self._write("{")
            for i, (key, member) in enumerate(value.items()):
                if i > 0:
                    self._write(", ")
                self._write(f".{key}=")
                self._write_initializer(member)
            self._write("}")
        else:
            self._write_initializer_member(value)

    def _write_initializer_member(self, value: Any) -> None:
        """
        Writes initializer member
        """
        if isinstance(value, bool):
            self._write("true" if value else "false")
        elif isinstance(value, (int, float)):
            self._write(str(value))
        elif isinstance(value, str):
            self._write(value)
        elif isinstance(value, core.Element):
            self._write_element(value)
        else:
            raise NotImplementedError(str(type(value)))

    def _write_base_type(self, elem: core.Type) -> None:
        """
        Writes name of type
        """
        if isinstance(elem.base_type, str):
            self._write(elem.base_type)
        else:
            self._write_base_type(elem.base_type)

    def _write_type_declaration(self, elem: core.Type) -> None:
        """
        Writes type declaration
        """
        self._write(self._format_type(elem))

    def _format_type(self, elem: core.Type) -> str:
        parts = []
        handled = {"const": False,
                   "volatile": False,
                   "type": False}
        for qualifier in self.style.type_qualifier_order:
            assert qualifier in handled
            handled[qualifier] = True
            if qualifier == "type":
                parts.append(self._format_type_part(elem))
            else:
                if elem.qualifier(qualifier):
                    parts.append(qualifier)
        for key, value in handled.items():
            if value is False and elem.qualifier(key):
                raise RuntimeError(f"Used qualifier '{key}' not part of selected qualifier_order list")
        return " ".join(parts)

    def _format_type_part(self, elem: core.Type) -> str:
        """
        Writes type name and pointer
        """
        result = ""
        if isinstance(elem.base_type, str):
            result += elem.base_type
        else:
            result += self._format_type(elem.base_type)
        if elem.pointer:
            if self.style.pointer_alignment == c_style.Alignment.LEFT:
                result += "*"
            elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                result += " *"
            elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                result += " *"
        return result

    def _write_variable_usage(self, elem: core.Variable) -> None:
        """
        Writes variable usage
        """
        self._write(elem.name)

    def _write_variable_declaration(self, elem: core.Variable) -> None:
        """
        Writes variable declaration
        """
        if elem.static:
            self._write("static ")
        if elem.extern:
            self._write("extern ")
        if isinstance(elem.data_type, core.Type):
            self._write_type_declaration(elem.data_type)
        elif isinstance(elem.data_type, core.Struct):
            self._write_struct_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Union):
            self._write_union_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Enum):
            self._write_enum_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Declaration):
            self._write_declaration(elem.data_type)
        elif isinstance(elem.data_type, core.TypeDef):
            self._write_typedef_usage(elem.data_type)
        else:
            raise NotImplementedError(str(type(elem.data_type)))
        result = ""
        if elem.pointer:
            if elem.const:
                if self.style.space_around_pointer_qualifiers == c_style.SpaceLocation.DEFAULT:
                    if self.style.pointer_alignment == c_style.Alignment.LEFT:
                        result += "* const "
                    elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                        result += "*const "
                    elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                        result += " * const "
                    else:
                        raise ValueError(self.style.pointer_alignment)
                else:
                    raise NotImplementedError("Only default space location supported for pointer qualifiers")
            else:
                if self.style.pointer_alignment == c_style.Alignment.LEFT:
                    result += "* "
                elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                    if isinstance(elem.data_type, core.Type) and elem.data_type.pointer:
                        result += "*"
                    else:
                        result += " *"
                elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                    result += " * "
                else:
                    raise ValueError(self.style.pointer_alignment)
        elif isinstance(elem.data_type, core.Type):
            if not (elem.data_type.pointer and self.style.pointer_alignment == c_style.Alignment.RIGHT):
                result += " "
        else:
            result += " "
        result += elem.name
        if elem.array is not None:
            result += f"[{elem.array}]"
        self._write(result)

    def _write_typedef_usage(self, elem: core.TypeDef) -> None:
        """
        Writes typedef usage
        """
        if not elem.name:
            raise ValueError("Typedef without name detected")
        self._write(elem.name)

    def _write_typedef_declaration(self, elem: core.TypeDef) -> None:
        """
        Writes typedef declaration
        """
        self._write("typedef ")

        if elem.const and not elem.pointer:
            self._write("const ")
        if isinstance(elem.base_type, core.Type):
            self._write_type_declaration(elem.base_type)
        elif isinstance(elem.base_type, core.Struct):
            self._write_struct_usage(elem.base_type)
        elif isinstance(elem.base_type, core.Union):
            self._write_union_usage(elem.base_type)
        elif isinstance(elem.base_type, core.Enum):
            self._write_enum_usage(elem.base_type)
        elif isinstance(elem.base_type, core.Declaration):
            self._write_declaration(elem.base_type)
        elif isinstance(elem.base_type, core.TypeDef):
            self._write_typedef_usage(elem.base_type)
        else:
            raise NotImplementedError(str(type(elem.base_type)))
        result = ""
        if elem.pointer:
            if elem.const:
                if self.style.space_around_pointer_qualifiers == c_style.SpaceLocation.DEFAULT:
                    if self.style.pointer_alignment == c_style.Alignment.LEFT:
                        result += "* const "
                    elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                        result += "*const "
                    elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                        result += " * const "
                    else:
                        raise ValueError(self.style.pointer_alignment)
                else:
                    raise NotImplementedError("Only default space location supported for pointer qualifiers")
            else:
                if self.style.pointer_alignment == c_style.Alignment.LEFT:
                    result += "* "
                elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                    if isinstance(elem.base_type, core.Type) and elem.base_type.pointer:
                        result += "*"
                    else:
                        result += " *"
                elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                    result += " * "
                else:
                    raise ValueError(self.style.pointer_alignment)
        else:
            if not ((isinstance(elem.base_type, core.Type) and elem.base_type.pointer) and (
                    self.style.pointer_alignment == c_style.Alignment.RIGHT)):
                result += " "
        assert elem.name is not None
        result += elem.name
        if elem.array is not None:
            result += f"[{elem.array}]"
        self._write(result)

    def _write_function_usage(self, elem: core.Function) -> None:
        """
        Writes function usage (name of the function)
        """
        if not elem.name:
            raise ValueError("Function with no name detected")
        self._write(elem.name)

    def _write_function_declaration(self, elem: core.Function) -> None:
        """
        Writes function declaration
        """
        if elem.extern:
            self._write("extern ")
        if elem.static:
            self._write("static ")
        if isinstance(elem.return_type, core.Type):
            self._write_type_declaration(elem.return_type)
        elif isinstance(elem.return_type, core.Struct):
            self._write_struct_usage(elem.return_type)
        elif isinstance(elem.return_type, core.Union):
            self._write_union_usage(elem.return_type)
        elif isinstance(elem.return_type, core.Enum):
            self._write_enum_usage(elem.return_type)
        elif isinstance(elem.return_type, core.TypeDef):
            self._write_typedef_usage(elem.return_type)
        else:
            raise NotImplementedError(str(type(elem.return_type)))
        self._write(f" {elem.name}(")
        if len(elem.params):
            for i, param in enumerate(elem.params):
                if i:
                    self._write(", ")
                self._write_variable_declaration(param)
        else:
            self._write("void")
        self._write(")")

    def _write_block(self, elem: core.Sequence) -> None:
        """
        Writes a brace-enclosed block sequence
        """
        self._write_starting_brace()
        if len(elem.elements):
            self._indent()
            self._write_sequence(elem)
            self._dedent()
            self._write_ending_brace()
        else:
            if self.style.short_functions_on_single_line in (c_style.ShortFunction.EMPTY,
                                                             c_style.ShortFunction.INLINE):
                self._write("}")
                self._eol()
            else:
                self._write_ending_brace()

    def _write_starting_brace(self) -> None:
        self._write("{")
        self._eol()

    def _write_ending_brace(self) -> None:
        self._start_line()
        self._write("}")
        self._eol()

    def _write_statement(self, elem: core.Statement) -> None:
        if isinstance(elem, core.GotoStatement):
            self._write(f"goto {elem.label};")
            return
        assert len(elem.parts) != 0
        if len(elem.parts) > 1:
            for i, part in enumerate(elem.parts):
                if i:
                    self._write(", ")
                self._write_expression(part)
        else:
            self._write_expression(elem.parts[0])
        self._write(";")

    def _write_expression(self, elem: Any) -> None:
        if isinstance(elem, str):
            self._write(elem)
        else:
            self._write_element(elem)

    def _write_if_statement(self, elem: core.IfStatement) -> None:
        if len(elem.branches) == 0:
            raise ValueError("IfStatement has no branches")
        num_conditions = len(elem.conditions)
        num_branches = len(elem.branches)
        for i, branch in enumerate(elem.branches):
            is_last = i == (num_branches - 1)
            if i == 0:
                self._write("if (")
                self._write_condition(elem.conditions[0])
                self._write(")")
            elif i < num_conditions:
                self._write("else if (")
                self._write_condition(elem.conditions[i])
                self._write(")")
            else:
                self._write("else")

            if isinstance(branch, core.Sequence):
                if self.style.brace_wrapping.after_control_statement:
                    self._eol()
                    self._start_line()
                    self._write("{")
                    self._eol()
                else:
                    self._write(" {")
                    self._eol()
                if len(branch.elements):
                    self._indent()
                    self._write_sequence(branch)
                    self._dedent()
                self._start_line()
                self._write("}")
                if is_last or self.style.brace_wrapping.before_else:
                    self._eol()
                    if not is_last:
                        self._start_line()
                else:
                    self._write(" ")
            elif isinstance(branch, core.Statement):
                self._write(" ")
                self._write_statement(branch)
                self._eol()
                if not is_last:
                    self._start_line()
            else:
                raise NotImplementedError(str(type(branch)))

    def _write_condition(self, cond: Any) -> None:
        if isinstance(cond, core.Sequence):
            for i, part in enumerate(cond.elements):
                if i > 0:
                    self._write(" ")
                self._write_expression(part)
        elif isinstance(cond, list):
            for i, part in enumerate(cond):
                if i > 0:
                    self._write(" ")
                self._write_expression(part)
        else:
            self._write_expression(cond)

    def _write_assignment(self, elem: core.Assignment) -> None:
        self._write_expression(elem.lhs)
        self._write(" = ")
        self._write_expression(elem.rhs)

    def _write_string_literal(self, elem: core.StringLiteral) -> None:
        self._write(f'"{elem.text}"')

    def _write_func_return(self, elem: core.FunctionReturn) -> None:
        if elem.expression is None:
            self._write("return")
        else:
            self._write("return ")
            self._write_expression(elem.expression)

    def _write_named_label(self, elem: core.NamedLabel) -> None:
        self._write(f"{elem.name}:")

    def _write_switch_label(self, elem: core.SwitchLabel) -> None:
        self._write("case ")
        self._write_expression(elem.value)
        self._write(":")

    def _write_switch_default(self, elem: core.SwitchDefault) -> None:  # pylint: disable=unused-argument
        self._write("default:")

    def _write_switch_statement(self, elem: core.SwitchStatement) -> None:
        self._write("switch (")
        self._write_expression(elem.expression)
        self._write(")")
        if isinstance(elem.body, core.Sequence):
            if self.style.brace_wrapping.after_control_statement:
                self._eol()
                self._start_line()
                self._write("{")
                self._eol()
            else:
                self._write(" {")
                self._eol()
            if len(elem.body.elements):
                self._indent()
                if self.style.indent_case_labels:
                    self._indent()
                self._write_sequence(elem.body)
                if self.style.indent_case_labels:
                    self._dedent()
                self._dedent()
            self._start_line()
            self._write("}")
            self._eol()
        elif isinstance(elem.body, core.Statement):
            self._write(" ")
            self._write_statement(elem.body)
            self._eol()
        else:
            raise NotImplementedError(str(type(elem.body)))

    def _write_loop_body(self, body: core.Statement | core.Sequence) -> None:
        if isinstance(body, core.Sequence):
            if self.style.brace_wrapping.after_control_statement:
                self._eol()
                self._start_line()
                self._write("{")
                self._eol()
            else:
                self._write(" {")
                self._eol()
            if len(body.elements):
                self._indent()
                self._write_sequence(body)
                self._dedent()
            self._start_line()
            self._write("}")
            self._eol()
        elif isinstance(body, core.Statement):
            self._write(" ")
            self._write_statement(body)
            self._eol()
        else:
            raise NotImplementedError(str(type(body)))

    def _write_while_statement(self, elem: core.WhileStatement) -> None:
        self._write("while (")
        self._write_condition(elem.condition)
        self._write(")")
        self._write_loop_body(elem.body)

    def _write_do_while_statement(self, elem: core.DoWhileStatement) -> None:
        self._write("do")
        if isinstance(elem.body, core.Sequence):
            if self.style.brace_wrapping.after_control_statement:
                self._eol()
                self._start_line()
                self._write("{")
                self._eol()
            else:
                self._write(" {")
                self._eol()
            if len(elem.body.elements):
                self._indent()
                self._write_sequence(elem.body)
                self._dedent()
            self._start_line()
            self._write("}")
        elif isinstance(elem.body, core.Statement):
            self._write(" ")
            self._write_statement(elem.body)
        else:
            raise NotImplementedError(str(type(elem.body)))

        if self.style.brace_wrapping.before_while:
            self._eol()
            self._start_line()
            self._write("while (")
        else:
            self._write(" while (")
        self._write_condition(elem.condition)
        self._write(");")
        self._eol()

    def _write_for_statement(self, elem: core.ForStatement) -> None:
        self._write("for (")
        if elem.init is not None:
            self._write_for_clause(elem.init)
        self._write(";")
        if elem.condition is not None:
            self._write(" ")
            self._write_condition(elem.condition)
        self._write(";")
        if elem.update is not None:
            self._write(" ")
            self._write_for_clause(elem.update)
        self._write(")")
        self._write_loop_body(elem.body)

    def _write_for_clause(self, clause: Any) -> None:
        if isinstance(clause, core.Sequence):
            for i, part in enumerate(clause.elements):
                if i > 0:
                    self._write(", ")
                self._write_expression(part)
        elif isinstance(clause, list):
            for i, part in enumerate(clause):
                if i > 0:
                    self._write(", ")
                self._write_expression(part)
        else:
            self._write_expression(clause)

    def _write_func_call(self, elem: core.FunctionCall) -> None:
        self._write(f"{elem.name}(")
        for i, arg in enumerate(elem.args):
            if i:
                self._write(", ")
            self._write_expression(arg)
        self._write(")")

    def _write_struct_usage(self, elem: core.Struct) -> None:
        """
        Writes struct usage
        """
        if not elem.name:
            raise ValueError("struct doesn't have a name. Did you mean to use a declaration?")
        self._write(f"struct {elem.name}")

    def _write_struct_declaration(self, elem: core.Struct) -> None:
        """
        Writes struct declaration
        """
        self._write(f"struct {elem.name}" if elem.name else "struct")
        if self.style.brace_wrapping.after_struct:
            self._eol()
            self._start_line()
            self._write("{")
            self._eol()
        else:
            self._write(" {")
            self._eol()
        if len(elem.members):
            self._indent()
        for member in elem.members:
            self._start_line()
            self._write_struct_member(member)
            self._write(";")
            self._eol()
        if len(elem.members):
            self._dedent()
        self._start_line()
        self._write("}")

    def _write_union_usage(self, elem: core.Union) -> None:
        """
        Writes union usage
        """
        if not elem.name:
            raise ValueError("union doesn't have a name. Did you mean to use a declaration?")
        self._write(f"union {elem.name}")

    def _write_union_declaration(self, elem: core.Union) -> None:
        """
        Writes union declaration
        """
        self._write(f"union {elem.name}" if elem.name else "union")
        if self.style.brace_wrapping.after_union:
            self._eol()
            self._start_line()
            self._write("{")
            self._eol()
        else:
            self._write(" {")
            self._eol()
        if len(elem.members):
            self._indent()
        for member in elem.members:
            self._start_line()
            self._write_struct_member(member)
            self._write(";")
            self._eol()
        if len(elem.members):
            self._dedent()
        self._start_line()
        self._write("}")

    def _write_enum_usage(self, elem: core.Enum) -> None:
        """
        Writes enum usage
        """
        if not elem.name:
            raise ValueError("enum doesn't have a name. Did you mean to use a declaration?")
        self._write(f"enum {elem.name}")

    def _write_enum_member_usage(self, elem: core.EnumMember) -> None:
        """
        Writes enum member usage
        """
        self._write(elem.full_name)

    def _write_enum_declaration(self, elem: core.Enum) -> None:
        """
        Writes enum declaration
        """
        self._write(f"enum {elem.name}" if elem.name else "enum")
        if self.style.brace_wrapping.after_enum:
            self._eol()
            self._start_line()
            self._write("{")
            self._eol()
        else:
            self._write(" {")
            self._eol()
        num_members = len(elem.members)
        if num_members:
            self._indent()
        for i, member in enumerate(elem.members):
            self._start_line()
            self._write_enum_member_declaration(member)
            if i < num_members - 1:
                self._write(",")
            self._eol()
        if num_members:
            self._dedent()
        self._start_line()
        self._write("}")

    def _write_enum_member_declaration(self, elem: core.EnumMember) -> None:
        """
        Writes enum member inside an enum declaration
        """
        self._write(elem.full_name)
        if elem.value is not None:
            self._write(" = ")
            self._write_expression(elem.value)

    def _write_struct_member(self, elem: core.StructMember) -> None:
        """
        Writes struct member
        """
        if isinstance(elem.data_type, core.Type):
            self._write_type_declaration(elem.data_type)
        elif isinstance(elem.data_type, core.Struct):
            self._write_struct_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Union):
            self._write_union_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Enum):
            self._write_enum_usage(elem.data_type)
        elif isinstance(elem.data_type, core.Declaration):
            self._write_declaration(elem.data_type)
        elif isinstance(elem.data_type, core.TypeDef):
            self._write_typedef_usage(elem.data_type)
        else:
            raise NotImplementedError(str(type(elem.data_type)))
        result = ""
        if elem.pointer:
            if elem.const:
                if self.style.space_around_pointer_qualifiers == c_style.SpaceLocation.DEFAULT:
                    if self.style.pointer_alignment == c_style.Alignment.LEFT:
                        result += "* const "
                    elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                        result += "*const "
                    elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                        result += " * const "
                    else:
                        raise ValueError(self.style.pointer_alignment)
                else:
                    raise NotImplementedError("Only default space location supported for pointer qualifiers")
            else:
                if self.style.pointer_alignment == c_style.Alignment.LEFT:
                    result += "* "
                elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                    if isinstance(elem.data_type, core.Type) and elem.data_type.pointer:
                        result += "*"
                    else:
                        result += " *"
                elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                    result += " * "
                else:
                    raise ValueError(self.style.pointer_alignment)
        else:
            if not (isinstance(elem.data_type, core.Type) and elem.data_type.pointer and (
                    self.style.pointer_alignment == c_style.Alignment.RIGHT)):
                result += " "
        result += elem.name
        if elem.array is not None:
            result += f"[{elem.array}]"
        self._write(result)

# Preprocessor directives

    def _write_directive(self, elem: core.Directive) -> None:
        current_depth = sum(self._pp_stack)
        if isinstance(elem, (core.IfDirective, core.IfdefDirective, core.IfndefDirective)):
            depth = current_depth
            if isinstance(elem, core.IfndefDirective) and self._next_ifndef_is_guard:
                self._pp_stack.append(0)
                self._next_ifndef_is_guard = False
            else:
                self._pp_stack.append(1)
        elif isinstance(elem, (core.ElifDirective, core.ElifdefDirective, core.ElifndefDirective, core.ElseDirective)):
            top_step = self._pp_stack[-1] if self._pp_stack else 0
            depth = max(0, current_depth - top_step)
        elif isinstance(elem, core.EndifDirective):
            top_step = self._pp_stack.pop() if self._pp_stack else 0
            depth = max(0, current_depth - top_step)
        else:
            depth = current_depth

        pp_width = self.indent_width if self.style.pp_indent_width < 0 else self.style.pp_indent_width
        spaces = " " * (depth * pp_width)
        if self.style.indent_pp_directives == c_style.PPDirectiveIndent.AFTER_HASH:
            self._write(f"#{spaces}{elem.text}")
        elif self.style.indent_pp_directives == c_style.PPDirectiveIndent.BEFORE_HASH:
            self._write(f"{spaces}#{elem.text}")
        else:
            self._write(f"#{elem.text}")

    def _write_extern(self, elem: core.Extern) -> None:
        self._write(f'extern "{elem.language}"')
