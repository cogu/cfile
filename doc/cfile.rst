cfile
=====


sequence
--------

.. py:class:: sequence()

Returns a new sequence. A sequence is simply a list where each item in the list represents a line of code.
Use sequence.append to insert new items to the list. Use sequence.lines() to get the sequence as strings.

Example::

   import cfile as C
   code = C.sequence()
   
block
-----

.. py:class:: block(indent=None, innerIndent=0, head=None, tail=None)

Creates a new C block (a block starts with '{' and ends with '}')

.. py:attribute:: block.code

An instance of sequence_.

   
.. py::method:: sequence.append(item)

appends item to the sequence. the item can be any of:

* cfile.line: A line of code.
* cfile.include: An include.
* cfile.statement: A statement.
* cfile.sequence: another sequence.
* cfile.block: A block (a block is also a sequence).
* other things. 
   
variable
--------

.. py:class:: variable(name, typename='int', static=0, const=0, pointer=0, alias=0,extern=0, array=None)

Creates a C variable. Note that static, const, pointer and extern can be initialized with True/False as well as 0,1,2 etc.


function
--------

.. py::class:: function(name, typename='int', const=0, pointer=0, classname="", args=None)

Creates a C function. Note that const and pointer can be initialized with True/False as well as 0,1,2 etc.


