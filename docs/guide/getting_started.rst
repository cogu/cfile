Getting Started
===============

**cfile** separates **code structure** from **code formatting**:

1. Use :class:`~cfile.factory.CFactory` to construct a :class:`~cfile.core.Sequence` of C code elements.
2. Use :class:`~cfile.writer.Writer` (optionally configured with :class:`~cfile.style.StyleOptions`)
   to render the sequence to a string or file.

Hello World
-----------

The following example creates a ``main`` function that prints ``Hello World\n`` and returns ``0``:

.. literalinclude:: ../../examples/hello_world.py
   :language: python
   :start-at: import cfile

Output (default Allman style):

.. literalinclude:: ../../examples/expected/hello_world.c
   :language: c

Changing the Formatting Style
-----------------------------

Pass a :class:`~cfile.style.StyleOptions` instance to :class:`~cfile.writer.Writer` to change brace
placement, pointer alignment, indentation, or other formatting options without modifying the code tree:

.. literalinclude:: ../../examples/hello_world_styled.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/hello_world_styled.c
   :language: c

Writing to a File
-----------------

Use :meth:`~cfile.writer.Writer.write_file` instead of :meth:`~cfile.writer.Writer.write_str` to write
generated C code directly to disk:

.. code-block:: python

    writer = cfile.Writer()
    writer.write_file(code, "main.c")
