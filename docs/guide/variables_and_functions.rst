Variables & Functions
=====================

Declarations vs. References
---------------------------

In **cfile**, objects returned by ``C.variable()``, ``C.function()``, ``C.struct()``, ``C.union()``,
``C.enum()``, and ``C.typedef()`` represent the underlying C entity:

* **Wrapped in** ``C.declaration(...)`` or ``C.declaration_statement(...)``: Emits the full C declaration
  (including types, qualifiers, struct/union/enum members, initializers, or function bodies).
* **Used directly** (or interpolated in a Python f-string): Emits a reference to the entity's identifier name
  (or a forward declaration in the case of a struct/union statement).

Variables and Assignments
-------------------------

Use ``C.variable()``, ``C.declaration_statement()``, and ``C.assignment()`` to declare and assign variables:

.. literalinclude:: ../../examples/variables.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/variables.c
   :language: c

Multi-Variable Declarations & Comma-Chained Statements
------------------------------------------------------

To declare multiple variables sharing the same base type in a single statement, use
:meth:`~cfile.factory.CFactory.multi_declaration` or
:meth:`~cfile.factory.CFactory.multi_declaration_statement`. Each item may be a bare
:class:`~cfile.core.Variable`, a ``(Variable, init_value)`` 2-tuple, or a :class:`~cfile.core.Declaration`.

To chain multiple expressions with commas in a single statement (or in a ``for``-loop header), use
:meth:`~cfile.factory.CFactory.multi_statement`:

.. literalinclude:: ../../examples/multi_declarations.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/multi_declarations.c
   :language: c

Functions, Prototypes & Validated Calls
---------------------------------------

* Wrap a :class:`~cfile.core.Function` in ``C.declaration_statement(fn)`` to emit a semicolon-terminated
  prototype.
* Pass a body :class:`~cfile.core.Sequence` as the second argument of ``C.declaration(fn, body)`` to emit
  a function definition.
* Pass a :class:`~cfile.core.Function` object directly to ``C.fn_call(fn, args)`` to validate the argument
  count automatically against the function's parameter list.

.. literalinclude:: ../../examples/functions.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/functions.c
   :language: c
