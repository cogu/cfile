"""
Factory classes
"""
from collections import namedtuple
from typing import Any
import cfile.core as core

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


class CFactory:
    """
    Factory for the C programming language
    """

    def blank(self) -> core.Blank:
        """
        Blank line
        """
        return core.Blank()

    def whitespace(self, width: int) -> core.Whitespace:
        """
        White space of user-defined length
        """
        return core.Whitespace(width)

    def line_comment(self, text) -> core.LineComment:
        """
        New line comment
        """
        return core.LineComment(text)

    def block_comment(self, text) -> core.BlockComment:
        """
        New block comment
        """
        return core.BlockComment(text)

    def sequence(self) -> core.Sequence:
        """
        New sequence
        """
        return core.Sequence()

    def include(self, path_to_file: str) -> core.IncludeDirective:
        """
        New include directive
        """
        return core.IncludeDirective(path_to_file)

    def sysinclude(self, path_to_file) -> core.IncludeDirective:
        """
        New system-level include directive
        """
        return core.IncludeDirective(path_to_file, system=True)

    def block(self) -> core.Block():
        """
        New block sequence
        """
        return core.Block()

    def function(self,
                 name: str,
                 return_type: str | core.Type | None = None,
                 static: bool = False,
                 const: bool = False,  # This is not const of the return type
                 extern: bool = False) -> core.Function:
        """
        New function
        """
        return core.Function(name, return_type, static, const, extern)

    def type(self,
             type_ref: str | core.Type,
             const: bool = False,
             pointer: bool = False,
             volatile: bool = False,
             array: int | None = None) -> core.Type:
        """
        New type
        """
        return core.Type(type_ref, const, pointer, volatile, array)

    def variable(self,
                 name: str,
                 data_type: str | core.Type,
                 const: bool = False,    # Only used as pointer qualifier
                 pointer: bool = False,
                 extern: bool = False,
                 static: bool = False,
                 array: int | None = None) -> core.Variable:
        """
        New variable
        """
        return core.Variable(name, data_type, const, pointer, extern, static, array)

    def statement(self, expression: Any) -> core.Statement:
        """
        New statement
        """
        return core.Statement(expression)

    def assignment(self, lhs: Any, rhs: Any) -> core.Assignment:
        """
        New assignment
        """
        return core.Assignment(lhs, rhs)

    def str_literal(self, text: str) -> core.StringLiteral:
        """
        New function call
        """
        return core.StringLiteral(text)

    def f_call(self, name: str, *args) -> core.FunctionCall:
        """
        New function call
        """
        return core.FunctionCall(name, *args)

    def f_return(self, expression: int | float | str | core.Element) -> core.FunctionReturn:
        """
        New return expression
        """
        return core.FunctionReturn(expression)
