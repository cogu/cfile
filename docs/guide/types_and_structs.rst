Types, Structs, Unions & Enums
==============================

Forward vs. Full Struct Declarations
------------------------------------

Placing a :class:`~cfile.core.Struct` directly inside ``C.statement(...)`` emits a forward declaration
(``struct mystruct;``), while wrapping it in ``C.declaration_statement(...)`` (or ``C.statement(C.declaration(...))``)
emits the complete struct definition:

.. literalinclude:: ../../examples/forward_declared_struct.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/forward_declared_struct.c
   :language: c

Typedef Structs
---------------

Wrap a struct ``C.declaration(...)`` inside ``C.typedef(...)`` to generate a ``typedef struct`` declaration:

.. literalinclude:: ../../examples/typedef_struct.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/typedef_struct.c
   :language: c

Struct Initializers
-------------------

Pass a Python ``list`` (positional initializer) or ``dict`` (C99 designated initializer) as the second
argument to ``C.declaration(...)`` or ``C.declaration_statement(...)``:

.. literalinclude:: ../../examples/struct_initializer.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/struct_initializer.c
   :language: c

Unions
------

Declare C ``union`` types with :meth:`~cfile.factory.CFactory.union` and
:meth:`~cfile.factory.CFactory.union_member`, and initialize variables using positional lists or
designated dictionaries:

.. literalinclude:: ../../examples/union.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/union.c
   :language: c

Nested Structs, Anonymous Unions & Designated Initializers
----------------------------------------------------------

Nest inline ``struct`` or anonymous ``union`` declarations inside an outer ``struct`` by passing
``C.declaration(...)`` as a member's ``data_type``, and initialize them with nested lists or dicts:

.. literalinclude:: ../../examples/nested_struct.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/nested_struct.c
   :language: c

Enumerations with Automatic Member Prefixes
-------------------------------------------

Use :meth:`~cfile.factory.CFactory.enum` and :meth:`~cfile.core.Enum.make_member` (or pass a ``list`` /
``dict`` of members) to define C enumerations. Setting ``prefix`` automatically prepends the prefix to
every enumerator both in the declaration and wherever an :class:`~cfile.core.EnumMember` is referenced:

.. literalinclude:: ../../examples/enumeration.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/enumeration.c
   :language: c
