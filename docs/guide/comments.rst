Comments & Whitespace
=====================

Line Comments, Block Comments & Banners
---------------------------------------

Use :meth:`~cfile.factory.CFactory.line_comment` and :meth:`~cfile.factory.CFactory.block_comment`
to generate ``//`` and ``/* ... */`` comments. By default, ``padding=1`` and ``margin=1`` automatically
insert a space before and after the comment delimiter so you do not need to pad your comment strings
manually.

Setting ``width > 0`` on ``C.block_comment()`` creates a banner comment with ``width`` asterisks on
the opening and closing lines:

.. literalinclude:: ../../examples/comments.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/comments.c
   :language: c

Multi-Line & Absolute-Aligned Comments
--------------------------------------

* Pass a ``list[str]`` (or multi-line ``str``) to ``C.line_comment()`` or ``C.block_comment()`` to
  emit automatically aligned multi-line comments.
* Set ``absolute=True`` to measure ``padding`` in characters from the start of the line rather than
  relative to the preceding element—useful for vertically aligning trailing comments across adjacent
  statements. If the preceding code reaches or exceeds ``padding``, **cfile** automatically falls back
  to relative spacing (``padding=1``) to prevent collisions.

.. literalinclude:: ../../examples/comments_aligned.py
   :language: python
   :start-at: import cfile

Output:

.. literalinclude:: ../../examples/expected/comments_aligned.c
   :language: c
