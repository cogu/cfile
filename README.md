# cfile

A C code generator written in Python 3.

## Usage

```python
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.sysinclude("stdio.h"))
code.append(C.blank())
char_ptr_type = C.type("char", pointer=True)
code.append(C.function("main", "int").make_param("argc", "int").make_param("argv", char_ptr_type, pointer=True))
main_body = C.block()
main_body.append(C.statement(C.f_call("printf", C.str_literal(r"Hello World\n"))))
main_body.append(C.statement(C.f_return(0)))
code.append(main_body)
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
```

```C
   #include <stdio.h>

   int main(int argc, char** argv)
   {
      printf("Hello World!\n");
      return 0;
   }   
```

Same example again but we ser some formatting style options:

- Opening brace on same line
- Pointer alignment to the right

```python
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.sysinclude("stdio.h"))
code.append(C.blank())
char_ptr_type = C.type("char", pointer=True)
code.append(C.function("main", "int").make_param("argc", "int").make_param("argv", char_ptr_type, pointer=True))
main_body = C.block()
main_body.append(C.statement(C.f_call("printf", C.str_literal(r"Hello World\n"))))
main_body.append(C.statement(C.f_return(0)))
code.append(main_body)
style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH,
                           pointer_alignment=cfile.Alignment.RIGHT)
writer = cfile.Writer(style)
print(writer.write_str(code))
```

```C
   #include <stdio.h>

   int main(int argc, char **argv) {
      printf("Hello World!\n");
      return 0;
   }   
```

## Requires

Python 3.10+
