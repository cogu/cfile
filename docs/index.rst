cfile
=====

Welcome to the documentation for **cfile**, a programmatic C code generator for Python 3.

**cfile** lets you construct a lightweight parse tree of C language elements in Python—such as
variables, types, structs, unions, enums, typedefs, functions, control-flow statements, loops,
comments, and preprocessor directives—and render them into formatted C source and header files
using configurable, ``clang-format``-inspired style options.

Features
--------

* **Factory API**: Build C code trees cleanly through a single :class:`~cfile.factory.CFactory` entry point.
* **Reusable Symbol Objects**: Define a :class:`~cfile.core.Variable`, :class:`~cfile.core.Function`,
  :class:`~cfile.core.Struct`, :class:`~cfile.core.Union`, :class:`~cfile.core.Enum`, or
  :class:`~cfile.core.TypeDef` once, wrap it in ``C.declaration(...)`` (or ``C.declaration_statement(...)``)
  to emit its full declaration, and pass the object itself anywhere else (or in Python f-strings) to emit a reference.
* **Control Flow, Loops & Preprocessor Support**: First-class elements for ``if / else if / else`` chains,
  ``switch / case / default`` blocks, ``for / while / do ... while`` loops, ``break``, ``continue``, ``goto``,
  ``return``, aligned comments, and C99/C23 preprocessor directives with automatic indentation.
* **Configurable Formatting**: Decoupled :class:`~cfile.writer.Writer` and :class:`~cfile.style.StyleOptions`
  let you render the exact same code tree with Allman, K&R/Attach, or Linux brace placement, left/middle/right
  pointer alignment, preprocessor indentation, and configurable case/goto label indentation.

Getting Started
---------------

Start with the :doc:`guide/index` for step-by-step examples, or jump straight to :doc:`guide/getting_started`.

Project Links
-------------

* `Source code on GitHub <https://github.com/cogu/cfile>`_
* `Issue tracker <https://github.com/cogu/cfile/issues>`_

.. toctree::
   :hidden:
   :maxdepth: 2

   guide/index
   api/index
