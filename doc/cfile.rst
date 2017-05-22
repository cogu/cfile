cfile
=====

C code generator for python


Sequence
--------

.. py:class:: sequence()

Returns a new sequence. A sequence is simply a list where each item in the list represents a line of code.
Use sequence.append to insert new items to the list. Use sequence.lines() to get the sequence as strings.

Example::

   import cfile as C
   code = C.sequence()
   
Block
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

   
Variable
--------

.. py:class:: variable(name, typename='int', static=0, const=0, pointer=0, alias=0,extern=0, array=None)

Creates a C variable. Note that static, const, pointer and extern can be initialized with True/False as well as 0,1,2 etc.


Function
--------

.. py:class:: function(name, typename='int', static=0, const=0, pointer=0, classname="", args=None)

Parameters
~~~~~~~~~~

**Name**: Name of new function (string)

**typename**: return type name (string). Default='int'.

**static**: Controls the static property. Default=0.

* 0: function is not const
* 1: function is const
* False: See 0
* True: See 1

**const**: Controls the const property. Default=0.

* 0: function is not const
* 1: function is const
* False: See 0
* True: See 1

**pointer**: Controls the pointer property. Default=0.

* 0: return type is not pointer
* 1: return type is pointer (*)
* False: See 0
* True: See 1
* 2: return type is pointer to pointer (\**)
* 3: return type is pointer to pointer to pointer (\***)

**classname**: C++ class name

**args**: Function arguments (list of cfile.variable objects). Arguments can also be added after the function has been created.


 