Control Flow & Loops
====================

If / Else-If / Else Statements
------------------------------

Use :meth:`~cfile.factory.CFactory.if_statement` with :meth:`~cfile.core.IfStatement.else_if` and
:meth:`~cfile.core.IfStatement.else_branch` (or :meth:`~cfile.core.IfStatement.append` when building
branches dynamically in a loop). Passing a :class:`~cfile.core.Sequence` wraps the branch in braces;
passing a single :class:`~cfile.core.Statement` emits a single-line unbraced branch:

.. literalinclude:: ../../examples/if_statement.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/if_statement.c
   :language: c

Switch Statements & Jump Statements
-----------------------------------

Use :meth:`~cfile.factory.CFactory.switch`, :meth:`~cfile.factory.CFactory.switch_label`,
:meth:`~cfile.factory.CFactory.switch_default`, :meth:`~cfile.factory.CFactory.break_statement`,
:meth:`~cfile.factory.CFactory.continue_statement`, :meth:`~cfile.factory.CFactory.goto_statement`,
and :meth:`~cfile.factory.CFactory.named_label`:

.. literalinclude:: ../../examples/flow_control.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/flow_control.c
   :language: c

Loops (``for``, ``while``, ``do ... while``)
--------------------------------------------

Use :meth:`~cfile.factory.CFactory.for_statement` (alias :meth:`~cfile.factory.CFactory.for_loop`),
:meth:`~cfile.factory.CFactory.while_statement` (alias :meth:`~cfile.factory.CFactory.while_loop`),
and :meth:`~cfile.factory.CFactory.do_while_statement` (alias :meth:`~cfile.factory.CFactory.do_while`).

You can combine :meth:`~cfile.factory.CFactory.multi_declaration` and
:meth:`~cfile.factory.CFactory.multi_statement` inside ``for``-loop headers without producing duplicate
semicolons:

.. literalinclude:: ../../examples/loops.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/loops.c
   :language: c
