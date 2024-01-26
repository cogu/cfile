"""
Factory classes
"""
from collections import namedtuple
from typing import Union, Any
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

    def line(self, inner: Any) -> core.Line:
        """
        Like statement but doesn't add ';' before new-line.
        """
        return core.Line(inner)

    def whitespace(self, width: int) -> core.Whitespace:
        """
        White space of user-defined length
        """
        return core.Whitespace(width)

    def line_comment(self, text: str, adjust: int = 1) -> core.LineComment:
        """
        New line comment
        """
        return core.LineComment(text, adjust)

    def block_comment(self,
                      text: str | list[str],
                      adjust: int = 1,
                      width: int = 0,
                      line_start: str = "") -> core.BlockComment:
        """
        New block comment
        """
        return core.BlockComment(text, adjust, width, line_start)

    def sequence(self) -> core.Sequence:
        """
        New sequence
        """
        return core.Sequence()

    def include(self, path_to_file: str, adjust: int = 0) -> core.IncludeDirective:
        """
        New include directive
        """
        return core.IncludeDirective(path_to_file, adjust=adjust)

    def sysinclude(self, path_to_file, adjust: int = 0) -> core.IncludeDirective:
        """
        New system-level include directive
        """
        return core.IncludeDirective(path_to_file, system=True, adjust=adjust)

    def ifdef(self, identifier, adjust: int = 0) -> core.IfdefDirective:
        """
        New ifdef preprocessor directove
        """
        return core.IfdefDirective(identifier, adjust=adjust)

    def ifndef(self, identifier, adjust: int = 0) -> core.IfndefDirective:
        """
        New ifndef preprocessor directove
        """
        return core.IfndefDirective(identifier, adjust=adjust)

    def endif(self, adjust: int = 0) -> core.EndifDirective:
        """
        New endif preprocessor directove
        """
        return core.EndifDirective(adjust=adjust)

    def define(self, left: str, right: str | None = None, adjust: int = 0) -> core.DefineDirective:
        """
        New define preprocessor directive
        """
        return core.DefineDirective(left, right, adjust=adjust)

    def extern(self, language: str) -> core.Extern:
        """
        New extern declaration
        """
        return core.Extern(language)

    def block(self) -> core.Block:
        """
        New block sequence
        """
        return core.Block()

    def function(self,
                 name: str,
                 return_type: str | core.DataType | None = None,
                 static: bool = False,
                 const: bool = False,  # This is not const of the return type
                 extern: bool = False,
                 params: core.Variable | list[core.Variable] | None = None) -> core.Function:
        """
        New function
        """
        return core.Function(name, return_type, static, const, extern, params)

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

    def struct_member(self,
                      name: str,
                      data_type: str | core.Type | core.Struct,
                      const: bool = False,  # Pointer qualifier only
                      pointer: bool = False,
                      array: int | None = None) -> core.StructMember:
        """
        New StructMember
        """
        return core.StructMember(name, data_type, const, pointer, array)

    def struct(self,
               name: str,
               members: core.StructMember | list[core.StructMember] | None = None
               ) -> core.Struct:
        """
        New Struct
        """
        return core.Struct(name, members)

    def variable(self,
                 name: str,
                 data_type: str | core.Type | core.Struct,
                 const: bool = False,    # Only used as pointer qualifier
                 pointer: bool = False,
                 extern: bool = False,
                 static: bool = False,
                 array: int | None = None) -> core.Variable:
        """
        New variable
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
        New typedef
        """
        return core.TypeDef(name, base_type, const, pointer, volatile, array)

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

    arg_types = int | float | str | core.Element

    def func_call(self,
                  name: str,
                  args: list[arg_types] | arg_types | None = None) -> core.FunctionCall:
        """
        New function call
        """
        if args is None:
            return core.FunctionCall(name, None)
        elif isinstance(args, list):
            return core.FunctionCall(name, args)
        else:
            return core.FunctionCall(name, [args])

    def func_return(self, expression: int | float | str | core.Element) -> core.FunctionReturn:
        """
        New return expression
        """
        return core.FunctionReturn(expression)

    def declaration(self,
                    element: Union[core.Variable, core.Function, core.DataType],
                    init_value: Any | None = None) -> core.Declaration:

        """New declaration"""
        return core.Declaration(element, init_value)
