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
code.append(C.declaration(C.function("main", "int", params=[C.variable("argc", "int"),
                                                            C.variable("argv", char_ptr_type, pointer=True)
                                                            ])))
main_body = C.block()
main_body.append(C.statement(C.func_call("printf", C.str_literal(r"Hello World\n"))))
main_body.append(C.statement(C.func_return(0)))
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

Here's the same example again but this time we change the formatting style of the output:

- Opening brace on same line
- Pointer alignment to the right

```python
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.sysinclude("stdio.h"))
code.append(C.blank())
char_ptr_type = C.type("char", pointer=True)
code.append(C.declaration(C.function("main", "int", params=[C.variable("argc", "int"),
                                                            C.variable("argv", char_ptr_type, pointer=True)
                                                            ])))
main_body = C.block()
main_body.append(C.statement(C.func_call("printf", C.str_literal(r"Hello World\n"))))
main_body.append(C.statement(C.func_return(0)))
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

## Important update about declarations

Starting from version 0.3.1 you need to wrap functions, variables, structs and typedefs inside `C.declaraton` to actually declare them.
Before v0.3.1 these elements were implicitly declared when encountered in the code sequence.

Not using `C.declaration` will only print the name when used on variables, functions or typedefs. For structs it will have the following meaning:

* without declaration: Will only forward declare the struct type.
* With declaration: Will fully declare the struct and its members.

Example:

```python
import cfile

C = cfile.CFactory()

code = C.sequence()
mystruct = C.struct("mystruct",
                    members=[C.struct_member("field_1", "int"),
                             C.struct_member("field_2", "int")])
code.append(C.statement(mystruct))  # Forward declaration
code.append(C.blank())
code.append(C.statement(C.declaration(mystruct)))  # Struct declaration
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
```

```C
struct mystruct;

struct mystruct
{
    int field_1;
    int field_2;
};
```

When declaring typedefs of structs you can wrap the struct declaration inside the declaration of the typedef.

Example:

```python
import cfile

C = cfile.CFactory()

code = C.sequence()
mystruct = C.struct("mystruct",
                    members=[C.struct_member("field_1", "int"),
                             C.struct_member("field_2", "int")])
code.append(C.statement(C.declaration(C.typedef("mystruct_t", C.declaration(mystruct)))))
writer = cfile.Writer(cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH))
print(writer.write_str(code))
```

```C
typedef struct mystruct {
    int field_1;
    int field_2;
} mystruct_t;
```

## Requires

Python 3.10+ (Needed for modern type hinting support).

## Documentation

Documentation for v0.3 will be written at a later date.

For currently supported style options see class StyleOptions in cfile.style module.

## Changelog

See [Changelog document](CHANGELOG.md).

## About versions

**v0.2:** No longer maintained.

**v0.3:** Active development track. Code base is completely rewritten since v0.2.

**v0.4:** Once v0.3 is stable enough it will be released to Pypi as v0.4.
