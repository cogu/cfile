"""
cfile writer
"""
# pylint: disable=consider-using-with
from io import StringIO
from enum import Enum
from typing import TextIO, Any
import cfile.core as core
import cfile.style as c_style


class ElementType(Enum):
    """
    Element types
    """
    NONE = 0
    DIRECTIVE = 1
    COMMENT = 2
    TYPE = 3
    VARIABLE = 4
    STATEMENT = 5
    FUNCTION = 6
    BLOCK_START = 7
    BLOCK_END = 8


class Formatter:
    """
    Low-level generator
    """
    def __init__(self, indent_width: int,
                 indentation_char: str) -> None:
        self.file_path: str = None
        self.fh: TextIO = None  # pylint: disable=invalid-name
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
        self.switcher_elem = {
            "Type": self._write_type,
            "Variable": self._write_variable,
            "Function": self._write_function,
            "Assignment": self._write_assignment,
            "StringLiteral": self._write_string_literal,
            "FunctionReturn": self._write_func_return,
            "FunctionCall": self._write_func_call
        }
        self.switcher_all = {
            "Blank": self._write_blank,
            "Whitespace": self._write_whitespace,
            "IncludeDirective": self._write_include_directive,
            "LineComment": self._write_line_comment,
            "BlockComment": self._write_block_comment,
            "Block": self._write_block,
            "Statement": self._write_statement,
        }
        self.switcher_all.update(self.switcher_elem)
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
        self._str_open()
        self._write_sequence(sequence)
        return self.fh.getvalue()

    def write_str_elem(self, elem: Any):
        """
        Writes single item to string using pre-selected format style
        """
        self._str_open()
        self._write_element(elem)
        return self.fh.getvalue().removesuffix("\n")

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
            if isinstance(elem, core.Function):
                self._start_line()
                self._write_function(elem)
            elif isinstance(elem, core.Statement):
                self._start_line()
                self._write_statement(elem)
            elif isinstance(elem, core.Block):
                self._start_line()
                self._write_block(elem)
            elif isinstance(elem, core.IncludeDirective):
                self._write_include_directive(elem)
            elif isinstance(elem, core.Blank):
                self._write_blank(elem)
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
        self._write_line("//" + elem.text)
        self.last_element = ElementType.COMMENT

    def _write_block_comment(self, elem: core.BlockComment) -> None:
        """
        Writes block comment
        """
        lines = elem.text.splitlines()
        self._write("/*")
        for line in lines[:-1]:
            self._write_line(line)
        self._write(lines[-1] + "*/")
        self.last_element = ElementType.COMMENT

    def _write_include_directive(self, elem: core.IncludeDirective) -> None:
        if elem.system:
            self._write_line(f'#include <{elem.path_to_file}>')
        else:
            self._write_line(f'#include "{elem.path_to_file}"')
        self.last_element = ElementType.DIRECTIVE

    def _write_type(self, elem: core.Type) -> None:
        """
        Writes data type
        """
        self._write(self._format_type(elem))
        self.last_element = ElementType.TYPE

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
        if isinstance(elem.type_ref, str):
            result = elem.type_ref
        else:
            result = self._format_type(elem.type_ref)
        if elem.pointer:
            if self.style.pointer_alignment == c_style.Alignment.LEFT:
                result += "*"
            elif self.style.pointer_alignment == c_style.Alignment.RIGHT:
                result += " *"
            elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                result += " * "
        return result

    def _write_variable(self, elem: core.Variable) -> None:
        """
        Writes variable declaration
        """
        if elem.static:
            self._write("static ")
        if elem.extern:
            self._write("extern ")
        self._write_type(elem.data_type)
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
                    if elem.data_type.pointer:
                        result += "*"
                    else:
                        result += " *"
                elif self.style.pointer_alignment == c_style.Alignment.MIDDLE:
                    result += " * "
                else:
                    raise ValueError(self.style.pointer_alignment)
        else:
            result += " "
        result += elem.name
        if elem.array is not None:
            result += f"[{elem.array}]"
        self._write(result)
        self.last_element = ElementType.VARIABLE

    def _write_function(self, elem: core.Function) -> None:
        """
        Writes function declaration
        """
        if elem.extern:
            self._write("extern ")
        if elem.static:
            self._write("static ")
        self._write_type(elem.return_type)
        self._write(f" {elem.name}(")
        if len(elem.params):
            for i, param in enumerate(elem.params):
                if i:
                    self._write(", ")
                self._write_variable(param)
        self._write(")")
        self.last_element = ElementType.FUNCTION

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
        if self.last_element == ElementType.FUNCTION:
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
        self._eol()
        self.last_element = ElementType.STATEMENT

    def _write_expression(self, elem: Any) -> None:
        if isinstance(elem, str):
            self._write(elem)
        else:
            self._write_element(elem)

    def _write_assignment(self, elem: core.Assignment) -> None:
        self._write_expression(elem.lhs)
        self._write(" ")
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
