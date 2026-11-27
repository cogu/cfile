Preprocessor Directives & Headers
=================================

Header Files with Include Guards & ``extern "C"``
-------------------------------------------------

Use ``C.ifndef_directive()``, ``C.define_directive()``, ``C.include_directive(..., sys=True)``,
``C.extern("C")``, and ``C.endif_directive()`` to generate C/C++ compatible header files:

.. literalinclude:: ../../examples/typedef_header.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/typedef_header.c
   :language: c

C99, C23 & Extension Directives with Indentation
------------------------------------------------

**cfile** supports all C99 preprocessor directives as well as C23 and widely used compiler extensions
(``#elifdef``, ``#elifndef``, ``#warning``, ``#include_next``, ``#embed``) plus a generic
``C.directive(text)`` escape hatch.

Enable ``clang-format``-style automatic preprocessor indentation via
:attr:`~cfile.style.StyleOptions.indent_pp_directives` and
:attr:`~cfile.style.StyleOptions.pp_indent_width`. Top-level header include guards
(``#ifndef GUARD`` immediately followed by ``#define GUARD``) are automatically detected and do not
indent the rest of the header:

.. literalinclude:: ../../examples/preprocessor_directives.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/preprocessor_directives.c
   :language: c
