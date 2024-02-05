"""
cfile writer
"""
# pylint: disable=consider-using-with
from io import StringIO
from enum import Enum
from typing import TextIO, Any
from cfile import core
import cfile.style as c_style


class ElementType(Enum):
    """
    Element types
    """
    NONE = 0
    DIRECTIVE = 1
    COMMENT = 2
    TYPE_DECLARATION = 3
    STRUCT_DECLARATION = 4   # Should this be separate from type declaration?
    VARIABLE_DECLARATION = 5
    FUNCTION_DECLARATION = 6
    TYPEDEF = 7
    TYPE_INSTANCE = 8
    STRUCT_INSTANCE = 9
    VARIABLE_USAGE = 10
    FUNCTION_CALL = 11
    STATEMENT = 12
    BLOCK_START = 13
    BLOCK_END = 14


class Formatter:
    """
    Low-level generator
    """
    def __init__(self, indent_width: int,
                 indentation_char: str) -> None:
        self.file_path: str | None = None
        self.fh: TextIO | None = None  # pylint: disable=invalid-name
        self.indentation_char: str = indentation_char
        self.white_space_char: str = " "
        self.indent_width = indent_width  # Number of characters (spaces) per indendation
        self.indentation_level: int = 0  # current indentation level
        self.indentation_str: str = ""
        self.line_number: int = 0
        self.column: int = 0

    def _str_open(self):
        self.fh = StringIO()
        self.line_number = 1
        self.indentation_level = 0
        self.indentation_str = ""

    def _open(self, file_path: str):
        self.fh = open(file_path, "w", encoding="utf-8")
        self.file_path = file_path
        self.line_number = 1
        self.indentation_level = 0
        self.indentation_str = ""

    def _close(self):
        self.fh.close()

    def _indent(self):
        self.indentation_level += 1
        self.indentation_str = self.indentation_char * \
            (self.indentation_level * self.indent_width)

    def _dedent(self):
        self.indentation_level -= 1
        if self.indentation_level == 0:
            self.indentation_str = ""
        else:
            self.indentation_str = self.indentation_char * \
                (self.indentation_level * self.indent_width)

    def _start_line(self):
        self.fh.write(self.indentation_str)

    def _write(self, text):
        self.fh.write(text)
        self.column += len(text)

    def _write_line(self, text):
        self.fh.write(text)
        self._eol()

    def _eol(self):
        self.fh.write("\n")
        self.line_number += 1
        self.column = 0


class Writer(Formatter):
    """
    High level generator
    """
    def __init__(self, style: c_style.StyleOptions) -> None:
        super().__init__(style.indent_width, style.indent_char)
        self.style = style
        self.switcher_all = {
            "Type": self._write_base_type,
            "TypeDef": self._write_typedef_usage,
            "Struct": self._write_struct_usage,
            "Variable": self._write_variable_usage,
            "Function": self._write_function_usage,
            "Declaration": self._write_declaration,
            "Assignment": self._write_assignment,
            "StringLiteral": self._write_string_literal,
            "FunctionReturn": self._write_func_return,
            "FunctionCall": self._write_func_call,
            "Blank": self._write_blank,
            "Whitespace": self._write_whitespace,
            "LineComment": self._write_line_comment,
            "BlockComment": self._write_block_comment,
            "Block": self._write_block,
            "Statement": self._write_statement,
            "Line": self._write_line_element,
            "IncludeDirective": self._write_include_directive,
            "DefineDirective": self._write_define_directive,
            "IfdefDirective": self._write_ifdef_directive,
            "IfndefDirective": self._write_ifndef_directive,
            "EndifDirective": self._write_endif_directive,
            "Extern": self._write_extern,
        }
        self.last_element = ElementType.NONE

    def write_file(self, sequence: core.Sequence, file_path: str):
        """
        Writes the sequence to file using pre-selected format style
        """
        self._open(file_path)
        self._write_sequence(sequence)
        self._close()

    def write_str(self, sequence: core.Sequence) -> str:
        """
        Writes the sequence to string using pre-selected format style
        """
        assert isinstance(sequence, core.Sequence)
        self._str_open()
        self._write_sequence(sequence)
        assert isinstance(self.fh, StringIO)
        return self.fh.getvalue()

    def write_str_elem(self, elem: Any, trim_end: bool = True) -> str:
        """
        Writes single item to string using pre-selected format style
        """
        self._str_open()
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
        for elem in sequence.elements:
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
            elif isinstance(elem, core.Block):
                self._start_line()
                self._write_block(elem)
            elif isinstance(elem, core.Line):
                self._start_line()
                self._write_line_element(elem)
            else:
                self._start_line()
                class_name = elem.__class__.__name__
                write_method = self.switcher_all.get(class_name, None)
                if write_method is not None:
                    write_method(elem)
                else:
                    raise NotImplementedError(f"Found no writer for element {class_name}")
                if isinstance(elem, core.Directive):
                    self._eol()

    def _write_line_element(self, elem: core.Line) -> None:
        for i, part in enumerate(elem.parts):
            if i > 0:
                if isinstance(part, core.Comment):
                    self._write(" " * part.adjust)
                else:
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
        if isinstance(elem.text, str):
            self._write("//" + elem.text)
        else:
            raise NotImplementedError("list of strings not yet supported")
        self.last_element = ElementType.COMMENT

    def _write_block_comment(self, elem: core.BlockComment) -> None:
        """
        Writes block comment
        """
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
        self.last_element = ElementType.COMMENT

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
        elif isinstance(elem.element, core.Variable):
            self._write_variable_declaration(elem.element)
        elif isinstance(elem.element, core.Function):
            self._write_function_declaration(elem.element)
        else:
            raise NotImplementedError(str(type(elem.element)))
        if elem.init_value is not None:
            self._write(" = ")
            self._write_initializer(elem.init_value)

    def _write_initializer(self, value: Any) -> None:
        """
        Writes initializer
        """
        if isinstance(value, list):
            self._write("{")
            for i, member in enumerate(value):
                if i > 0:
                    self._write(", ")
                self._write_initializer_member(member)
            self._write("}")
        else:
            self._write_initializer_member(value)

    def _write_initializer_member(self, value: Any) -> None:
        """
        Writes initializer member
        """
        if isinstance(value, int):
            self._write(str(value))
        elif isinstance(value, str):
            self._write(f'"{value}"')
        else:
            raise NotImplementedError(str(type(value)))

    def _write_base_type(self, elem: core.Type) -> None:
        """
        Writes name of type
        """
        self._write(elem.base_type)

    def _write_type_declaration(self, elem: core.Type) -> None:
        """
        Writes type declaration
        """
        self._write(self._format_type(elem))
        self.last_element = ElementType.TYPE_DECLARATION

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
        self.last_element = ElementType.VARIABLE_USAGE

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
        self.last_element = ElementType.VARIABLE_DECLARATION

    def _write_typedef_usage(self, elem: core.TypeDef):
        """
        Writes typedef usage
        """
        if not elem.name:
            raise ValueError("Typedef without name detected")
        self._write(elem.name)

    def _write_typedef_declaration(self, elem: core.TypeDef):
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
        elif isinstance(elem.base_type, core.Declaration):
            self._write_declaration(elem.base_type)
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
        self.last_element = ElementType.TYPEDEF

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
        self.last_element = ElementType.FUNCTION_DECLARATION

    def _write_block(self, elem: core.Block) -> None:
        """
        Writes a block sequence
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
        handled = False
        if self.last_element == ElementType.FUNCTION_DECLARATION:
            handled = True
            if self.style.brace_wrapping.after_function:
                self._eol()
                self._start_line()
                self._write("{")
                self._eol()
            else:
                self._write(" {")
                self._eol()
        if not handled:
            self._write("{")
            self._eol()

    def _write_ending_brace(self) -> None:
        self._start_line()
        self._write("}")
        self._eol()

    def _write_statement(self, elem: core.Statement) -> None:
        assert len(elem.parts) != 0
        if len(elem.parts) > 1:
            for i, part in enumerate(elem.parts):
                if i:
                    self._write(" ")
                self._write_expression(part)
        else:
            self._write_expression(elem.parts[0])
        self._write(";")
        self.last_element = ElementType.STATEMENT

    def _write_expression(self, elem: Any) -> None:
        if isinstance(elem, str):
            self._write(elem)
        else:
            self._write_element(elem)

    def _write_assignment(self, elem: core.Assignment) -> None:
        self._write_expression(elem.lhs)
        self._write(" = ")
        self._write_expression(elem.rhs)

    def _write_string_literal(self, elem: core.StringLiteral) -> None:
        self._write(f'"{elem.text}"')

    def _write_func_return(self, elem: core.FunctionReturn) -> None:
        self._write("return ")
        self._write_expression(elem.expression)

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
        self._write(f"struct {elem.name}")
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
        self.last_element = ElementType.STRUCT_DECLARATION

    def _write_struct_member(self, elem: core.StructMember) -> None:
        """
        Writes struct member
        """
        if isinstance(elem.data_type, core.Type):
            self._write_type_declaration(elem.data_type)
        elif isinstance(elem.data_type, core.Struct):
            self._write_struct_usage(elem.data_type)
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

    def _write_include_directive(self, elem: core.IncludeDirective) -> None:
        if elem.system:
            self._write(f'#include <{elem.path_to_file}>')
        else:
            self._write(f'#include "{elem.path_to_file}"')
        self.last_element = ElementType.DIRECTIVE

    def _write_define_directive(self, elem: core.DefineDirective) -> None:
        if elem.right is not None:
            self._write(f"#{' '*elem.adjust}define {elem.left} {elem.right}")
        else:
            self._write(f"#{' '*elem.adjust}define {elem.left}")
        self.last_element = ElementType.DIRECTIVE

    def _write_ifdef_directive(self, elem: core.IfdefDirective) -> None:
        self._write(f"#{' '*elem.adjust}ifdef {elem.identifier}")
        self.last_element = ElementType.DIRECTIVE

    def _write_ifndef_directive(self, elem: core.IfndefDirective) -> None:
        self._write(f"#{' '*elem.adjust}ifndef {elem.identifier}")
        self.last_element = ElementType.DIRECTIVE

    def _write_endif_directive(self, elem: core.EndifDirective) -> None:
        self._write(f"#{' '*elem.adjust}endif")
        self.last_element = ElementType.DIRECTIVE

    def _write_extern(self, elem: core.Extern) -> None:
        self._write(f'extern "{elem.language}"')
        self.last_element = ElementType.DIRECTIVE
