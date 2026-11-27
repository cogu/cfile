Formatting & Style Options
==========================

**cfile** decouples code generation from formatting through :class:`~cfile.style.StyleOptions`,
inspired by ``clang-format``. The same :class:`~cfile.core.Sequence` can be rendered in multiple
C coding styles simply by passing a different :class:`~cfile.style.StyleOptions` instance to
:class:`~cfile.writer.Writer`.

Key Style Options
-----------------

* :attr:`~cfile.style.StyleOptions.break_before_braces`: Preset brace placement
  (:attr:`~cfile.style.BreakBeforeBraces.ALLMAN`, :attr:`~cfile.style.BreakBeforeBraces.ATTACH`,
  :attr:`~cfile.style.BreakBeforeBraces.LINUX`, or :attr:`~cfile.style.BreakBeforeBraces.CUSTOM` with
  a custom :class:`~cfile.style.BraceWrapping`).
* :attr:`~cfile.style.StyleOptions.pointer_alignment`: Placement of ``*`` in pointer declarations
  (:attr:`~cfile.style.Alignment.LEFT`, :attr:`~cfile.style.Alignment.RIGHT`, or
  :attr:`~cfile.style.Alignment.MIDDLE`).
* :attr:`~cfile.style.StyleOptions.indent_width` / :attr:`~cfile.style.StyleOptions.indent_char`:
  Indentation width (default ``4``) and character (default ``" "``).
* :attr:`~cfile.style.StyleOptions.indent_case_labels`,
  :attr:`~cfile.style.StyleOptions.indent_case_blocks`, and
  :attr:`~cfile.style.StyleOptions.indent_goto_labels`: Fine-grained control over ``switch`` and
  ``goto`` label indentation.
* :attr:`~cfile.style.StyleOptions.indent_pp_directives` and
  :attr:`~cfile.style.StyleOptions.pp_indent_width`: Preprocessor conditional indentation
  (:attr:`~cfile.style.PPDirectiveIndent.NONE`, :attr:`~cfile.style.PPDirectiveIndent.AFTER_HASH`, or
  :attr:`~cfile.style.PPDirectiveIndent.BEFORE_HASH`).

Example: Linux Kernel Brace Style with Right-Aligned Pointers
-------------------------------------------------------------

In :attr:`~cfile.style.BreakBeforeBraces.LINUX` style, function opening braces are placed on a new
line while control-flow braces (``if``, ``else``, ``for``, ``while``, ``switch``) stay attached on
the same line:

.. literalinclude:: ../../examples/formatting_style.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/formatting_style.c
   :language: c

For the full list of options, see :doc:`../api/style`.
