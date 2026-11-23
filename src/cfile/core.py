"""
cfile core
"""
from typing import Union, Any


class Element:
    """
    A code element, for example an expression
    """


class Directive(Element):
    """
    Preprocessor directive
    """
    def __init__(self, adjust: int = 0) -> None:
        self.adjust = adjust


class IncludeDirective(Directive):
    """
    Include directive
    """
    def __init__(self, path_to_file: str, system: bool = False, adjust: int = 0) -> None:
        super().__init__(adjust)
        self.path_to_file = path_to_file
        self.system = system


class IfdefDirective(Directive):
    """
    Ifdef preprocessor directive
    """
    def __init__(self, identifier: str, adjust: int = 0) -> None:
        super().__init__(adjust)
        self.identifier = identifier


class IfndefDirective(Directive):
    """
    Ifndef preprocessor directive
    """
    def __init__(self, identifier: str, adjust: int = 0) -> None:
        super().__init__(adjust)
        self.identifier = identifier


class EndifDirective(Directive):
    """
    Endif preprocessor directive
    """


class DefineDirective(Directive):
    """
    Preprocessor define directive
    """
    def __init__(self, left: str, right: str | None = None, adjust: int = 0) -> None:
        super().__init__(adjust)
        self.left = left
        self.right = right


class Extern(Element):
    """
    Extern declaration
    """
    def __init__(self, language: str) -> None:
        self.language = language


class Comment(Element):
    """
    Comment base
    adjust: Adds spaces before comment begins to allow right-adjustment
    """
    def __init__(self, text: str | list[str], adjust: int = 1) -> None:
        self.text = text
        self.adjust = adjust


class BlockComment(Comment):
    """
    Block Comment
    width: When > 0, sets the number of asterisks used on first and last line.
           Also puts the text between first and last line.
    line_start: Combine with width > 0. Puts this string at beginning of each line
                inside the comment
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
                 base_type: Union[str, "Type"],
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
    Struct element. This is similar to Variable
    but doesn't support type qualifier such as static
    or extern
    """
    def __init__(self,
                 name: str,
                 data_type: DataType | str,
                 const: bool = False,    # Pointer qualifier only
                 pointer: bool = False,
                 array: int | None = None) -> None:
        self.name = name
        self.const = const
        self.pointer = pointer
        self.array = array
        if isinstance(data_type, DataType):
            self.data_type = data_type
        elif isinstance(data_type, str):
            self.data_type = Type(data_type)
        else:
            raise TypeError(str(type(data_type)))

    def __str__(self) -> str:
        return self.name


class Struct(DataType):
    """
    A struct definition
    """
    def __init__(self, name: str | None, members: StructMember | list[StructMember] | None = None) -> None:
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
        Appends new element to the struct definition
        """
        if not isinstance(member, StructMember):
            raise TypeError(f'Invalid type, expected "StructMember", got {str(type(member))}')
        self.members.append(member)

    def make_member(self,
                    name: str,
                    data_type: str | DataType,
                    const: bool = False,  # Pointer qualifier only
                    pointer: bool = False,
                    array: int | None = None) -> StructMember:
        """
        Creates a new StructMember and appends it to the list of elements
        """
        member = StructMember(name, data_type, const, pointer, array)
        self.members.append(member)
        return member


class TypeDef(DataType):
    """
    Type definition (typedef)
    """
    def __init__(self,
                 name: str,
                 base_type: Union[str, "DataType", "Declaration"],
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
                 data_type: str | DataType,
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
        if isinstance(data_type, DataType):
            self.data_type = data_type
        elif isinstance(data_type, str):
            self.data_type = Type(data_type)
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
    A declaration element
    Valid sub-elements:
    - Variable
    - DataType (including struct)
    - Function
    """
    def __init__(self,
                 element: Union[Variable, Function, DataType],
                 init_value: Any | None = None) -> None:
        if isinstance(element, (Variable, Function, DataType)):
            self.element = element
            self.init_value = None
        else:
            raise TypeError(f"element: Invalid type '{str(type(element))}'")
        if init_value is not None:
            if not isinstance(element, Variable):
                raise ValueError("init_value only allowed for Variable declarations")
            self.init_value = init_value


class FunctionCall(Element):
    """
    Function call expression
    """
    def __init__(self, name: str, args: list[int | float | str | Element] | None = None) -> None:
        self.name = name
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
                 expression: int | float | bool | str | Element) -> None:
        self.expression: str | Element
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
        self.elements: list[Union[Comment, Statement, "Sequence", "IfStatement"]] = []
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
    If / else-if / else statement
    """
    def __init__(self,
                 condition: Any | None = None,
                 branch: Union[Statement, Block, Sequence, None] = None) -> None:
        self.conditions: list[Any] = []
        self.branches: list[Union[Statement, Block]] = []
        if condition is not None or branch is not None:
            if condition is None or branch is None:
                raise ValueError("Both condition and branch must be provided when initializing IfStatement")
            self.append(condition, branch)

    def append(self,
               condition: Any | None,
               branch: Union[Statement, Block, Sequence]) -> "IfStatement":
        """
        Appends a conditional branch, or a final else branch when condition is None
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
                branch: Union[Statement, Block, Sequence]) -> "IfStatement":
        """
        Appends an else-if branch
        """
        if condition is None:
            raise ValueError("else_if requires a condition")
        if len(self.branches) == 0:
            raise RuntimeError("Cannot call else_if before the initial if branch")
        return self.append(condition, branch)

    def else_branch(self,
                    branch: Union[Statement, Block, Sequence]) -> "IfStatement":
        """
        Appends the final else branch
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
