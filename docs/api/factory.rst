CFactory (``cfile.factory``)
============================

:class:`~cfile.factory.CFactory` is the primary factory interface for constructing C code elements.

Method Overview by Category
---------------------------

Sequences & Blocks
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.sequence`
     - Creates an unbraced sequence of code elements.
   * - :meth:`~cfile.factory.CFactory.block`
     - Creates a brace-enclosed block sequence (``{ ... }``).

Data Types, Structs & Typedefs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.type`
     - Creates a C data type reference (with optional ``const``, ``pointer``, ``volatile``, ``array``).
   * - :meth:`~cfile.factory.CFactory.struct`
     - Creates a C ``struct`` type entity.
   * - :meth:`~cfile.factory.CFactory.struct_member`
     - Creates a struct member field.
   * - :meth:`~cfile.factory.CFactory.union`
     - Creates a C ``union`` type entity.
   * - :meth:`~cfile.factory.CFactory.union_member`
     - Creates a union member field.
   * - :meth:`~cfile.factory.CFactory.enum`
     - Creates a C ``enum`` type entity (with optional ``prefix`` for member names).
   * - :meth:`~cfile.factory.CFactory.enum_member`
     - Creates an ``enum`` member constant.
   * - :meth:`~cfile.factory.CFactory.typedef`
     - Creates a ``typedef`` type alias entity.

Variables, Functions & Declarations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.variable`
     - Creates a C variable entity.
   * - :meth:`~cfile.factory.CFactory.function`
     - Creates a C function entity.
   * - :meth:`~cfile.factory.CFactory.declaration`
     - Wraps a variable, function, struct, or typedef to emit its full C declaration.
   * - :meth:`~cfile.factory.CFactory.declaration_statement`
     - Shorthand for ``C.statement(C.declaration(element, content))``.

Statements, Expressions & Control Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.statement`
     - Wraps an expression or declaration in a semicolon-terminated statement.
   * - :meth:`~cfile.factory.CFactory.assignment`
     - Creates an assignment expression (``<lhs> = <rhs>``).
   * - :meth:`~cfile.factory.CFactory.fn_call`
     - Creates a function call expression (accepts a function name or :class:`~cfile.core.Function`).
   * - :meth:`~cfile.factory.CFactory.fn_return`
     - Creates a ``return`` expression (to be wrapped in :meth:`~cfile.factory.CFactory.statement`).
   * - :meth:`~cfile.factory.CFactory.return_statement`
     - Creates a complete semicolon-terminated ``return`` statement.
   * - :meth:`~cfile.factory.CFactory.if_statement`
     - Creates an ``if / else if / else`` statement.
   * - :meth:`~cfile.factory.CFactory.switch`
     - Creates a ``switch (<expression>)`` statement.
   * - :meth:`~cfile.factory.CFactory.switch_label`
     - Creates a ``case <value>:`` label inside a ``switch`` body.
   * - :meth:`~cfile.factory.CFactory.switch_default`
     - Creates a ``default:`` label inside a ``switch`` body.
   * - :meth:`~cfile.factory.CFactory.break_statement`
     - Creates a ``break;`` statement.
   * - :meth:`~cfile.factory.CFactory.continue_statement`
     - Creates a ``continue;`` statement.
   * - :meth:`~cfile.factory.CFactory.goto_statement`
     - Creates a ``goto <label>;`` statement.
   * - :meth:`~cfile.factory.CFactory.named_label`
     - Creates a named target label (``<name>:``) for ``goto`` statements.
   * - :meth:`~cfile.factory.CFactory.str_literal`
     - Creates a double-quoted C string literal (``"<text>"``).

Comments, Lines & Whitespace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.line_comment`
     - Creates a single-line comment (``// ...``).
   * - :meth:`~cfile.factory.CFactory.block_comment`
     - Creates a block comment (``/* ... */``).
   * - :meth:`~cfile.factory.CFactory.line`
     - Creates a single line of code without a trailing semicolon.
   * - :meth:`~cfile.factory.CFactory.blank`
     - Creates a blank line element.
   * - :meth:`~cfile.factory.CFactory.whitespace`
     - Creates horizontal whitespace of a given width.

Preprocessor Directives
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - :meth:`~cfile.factory.CFactory.directive`
     - Creates a custom preprocessor directive (``#<text>``).
   * - :meth:`~cfile.factory.CFactory.include_directive`
     - Creates an ``#include "path"`` or ``#include <path>`` directive (via ``sys=True``).
   * - :meth:`~cfile.factory.CFactory.include_next_directive`
     - Creates an ``#include_next "path"`` or ``#include_next <path>`` directive (via ``sys=True``).
   * - :meth:`~cfile.factory.CFactory.embed_directive`
     - Creates a C23 ``#embed "path"`` or ``#embed <path>`` directive with optional parameters.
   * - :meth:`~cfile.factory.CFactory.define_directive`
     - Creates a ``#define <left> [right]`` directive.
   * - :meth:`~cfile.factory.CFactory.undef_directive`
     - Creates an ``#undef <identifier>`` directive.
   * - :meth:`~cfile.factory.CFactory.if_directive`
     - Creates an ``#if <expression>`` directive.
   * - :meth:`~cfile.factory.CFactory.ifdef_directive`
     - Creates an ``#ifdef <identifier>`` directive.
   * - :meth:`~cfile.factory.CFactory.ifndef_directive`
     - Creates an ``#ifndef <identifier>`` directive.
   * - :meth:`~cfile.factory.CFactory.elif_directive`
     - Creates an ``#elif <expression>`` directive.
   * - :meth:`~cfile.factory.CFactory.elifdef_directive`
     - Creates a C23 ``#elifdef <identifier>`` directive.
   * - :meth:`~cfile.factory.CFactory.elifndef_directive`
     - Creates a C23 ``#elifndef <identifier>`` directive.
   * - :meth:`~cfile.factory.CFactory.else_directive`
     - Creates an ``#else`` directive.
   * - :meth:`~cfile.factory.CFactory.endif_directive`
     - Creates an ``#endif`` directive.
   * - :meth:`~cfile.factory.CFactory.line_directive`
     - Creates a ``#line <number> ["<filename>"]`` directive.
   * - :meth:`~cfile.factory.CFactory.error_directive`
     - Creates an ``#error [message]`` directive.
   * - :meth:`~cfile.factory.CFactory.warning_directive`
     - Creates a ``#warning [message]`` directive.
   * - :meth:`~cfile.factory.CFactory.pragma_directive`
     - Creates a ``#pragma [tokens]`` directive.
   * - :meth:`~cfile.factory.CFactory.extern`
     - Creates an ``extern "<language>"`` linkage specification.

Class Reference
---------------

.. autoclass:: cfile.factory.CFactory
   :members:
   :show-inheritance:
