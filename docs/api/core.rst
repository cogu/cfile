Core Elements (``cfile.core``)
==============================

The ``cfile.core`` module defines the parse-tree elements constructed by :class:`~cfile.factory.CFactory`
and rendered by :class:`~cfile.writer.Writer`.

Sequences & Blocks
------------------

.. autoclass:: cfile.core.Sequence
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Block
   :members:
   :show-inheritance:

Data Types, Structs & Typedefs
------------------------------

.. autoclass:: cfile.core.DataType
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Type
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.StructMember
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Struct
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.UnionMember
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Union
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.EnumMember
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Enum
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.TypeDef
   :members:
   :show-inheritance:

Variables, Functions & Declarations
-----------------------------------

.. autoclass:: cfile.core.Variable
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Function
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Declaration
   :members:
   :show-inheritance:

Statements, Expressions & Control Flow
--------------------------------------

.. autoclass:: cfile.core.Statement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Assignment
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.FunctionCall
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.FunctionReturn
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.ReturnStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.BreakStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.ContinueStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.GotoStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.NamedLabel
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.IfStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.SwitchStatement
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.SwitchLabel
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.SwitchDefault
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.StringLiteral
   :members:
   :show-inheritance:

Comments, Lines & Whitespace
----------------------------

.. autoclass:: cfile.core.Comment
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.LineComment
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.BlockComment
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Line
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Whitespace
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Blank
   :members:
   :show-inheritance:

Preprocessor Directives
-----------------------

.. autoclass:: cfile.core.Directive
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.IncludeDirective
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.DefineDirective
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.IfdefDirective
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.IfndefDirective
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.EndifDirective
   :members:
   :show-inheritance:

.. autoclass:: cfile.core.Extern
   :members:
   :show-inheritance:
