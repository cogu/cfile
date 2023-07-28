"""
cfile core
"""
from typing import Union, Any


class Directive:
    """
    Preprocessor directive
    """


class IncludeDirective(Directive):
    """
    Include directive
    """
    def __init__(self, path_to_file: str, system: bool = False) -> None:
        self.path_to_file = path_to_file
        self.system = system


class Comment:
    """
    Comment base
    """
    def __init__(self, text: str) -> None:
        self.text = text


class BlockComment(Comment):
    """
    Block Comment
    """
    def __init__(self, text: str, width=1) -> None:
        super().__init__(text)
        self.width = width  # how many asterisk characters to generate before/after the slash


class LineComment(Comment):
    """
    Line Comment
    """


class Whitespace:
    """
    Whitespace
    """
    def __init__(self, width) -> None:
        self.width = width


class Blank(Whitespace):
    """
    Blank line
    """
    def __init__(self) -> None:
        super().__init__(0)


class Element:
    """
    A code element, for example an expression
    """


class Type(Element):
    """
    Data type
    """
    def __init__(self,
                 type_ref: Union[str, "Type"],
                 const: bool = False,
                 pointer: bool = False,
                 volatile: bool = False,
                 array: int | None = None) -> None:  # Only used for typedefs to other array types
        self.type_ref = type_ref
        self.const = const
        self.volatile = volatile
        self.pointer = pointer
        self.array = array

    def qualifier(self, name) -> bool:
        """
        Returns the status of named qualifier
        """
        if name == "const":
            return self.const
        if name == "volatile":
            return self.volatile
        else:
            raise KeyError(name)


class Variable(Element):
    """
    Variable declaration
    """
    def __init__(self,
                 name: str,
                 data_type: str | Type,
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
        if isinstance(data_type, Type):
            self.data_type = data_type
        elif isinstance(data_type, str):
            self.data_type = Type(data_type)
        else:
            raise TypeError(str(type(data_type)))

    def qualifier(self, name) -> bool:
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


class Function(Element):
    """
    Function declaration
    """
    def __init__(self,
                 name: str,
                 return_type: str | Type | None = None,
                 static: bool = False,
                 const: bool = False,  # This is not const of the return type
                 extern: bool = False) -> None:
        self.name = name
        self.static = static
        self.const = const   # Const function (as seen in C++)
        self.extern = extern
        if isinstance(return_type, Type):
            self.return_type = return_type
        elif isinstance(return_type, str):
            self.return_type = Type(return_type)
        elif return_type is None:  # None is a synomym for void
            self.return_type = Type("void")
        else:
            raise TypeError(str(type(return_type)))
        self.params: list[Variable] = []

    def add_param(self, param: Variable) -> "Function":
        """
        Add function parameter
        """
        if not isinstance(param, (Variable)):
            raise TypeError("Expected Variable or FunctionPtr object")
        self.params.append(param)
        return self

    def make_param(self,
                   name: str,
                   data_type: str | Type,
                   const: bool = False,
                   pointer: bool = False,
                   array: int | None = None) -> "Function":
        """
        Creates new Variable from arguments and adds as parameter
        """
        param = Variable(name, data_type, const=const, pointer=pointer, array=array)
        return self.add_param(param)


class FunctionCall(Element):
    """
    Function call expression
    """
    def __init__(self, name: str, *args) -> None:
        self.name = name
        self.args = []
        for arg in args:
            self.add_arg(arg)

    def add_arg(self, arg: str | Element) -> "FunctionCall":
        """
        Add argument
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
                 expression: int | float | bool | str | Element) -> None:
        if isinstance(expression, bool):
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

    def _check_and_convert(self, elem: Any):
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

    def _check_and_convert(self, elem: Any):
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
    def __init__(self):
        self.elements: Union[Comment, Statement, "Sequence"] = []

    def __len__(self):
        return len(self.elements)

    def append(self, elem: Any) -> "Sequence":
        """
        Appends one element to this sequence
        """
        self.elements.append(elem)
        return self

    def extend(self, seq) -> "Sequence":
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
