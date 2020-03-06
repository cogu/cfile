cfile
-----

A python C code generator

**Usage**::

   >>> import cfile as C
   >>> test = C.cfile('test.c')
   >>> test.code.append(C.sysinclude('stdio.h'))
   >>> test.code.append(C.blank())
   >>> test.code.append(C.function('main', 'int',).add_arg(C.variable('argc', 'int')).add_arg(C.variable('argv', 'char', pointer=2)))
   >>> body = C.block(indent=3)
   >>> body.append(C.statement(C.fcall('printf').add_param(r'"Hello World!\n"')))
   >>> body.append(C.statement('return 0'))
   >>> test.code.append(body)
   >>> print(str(test))

   #include <stdio.h>

   int main(int argc, char **argv)
   {
      printf("Hello World!\n");
      return 0;
   }

Prerequisites
-------------

Python 3
