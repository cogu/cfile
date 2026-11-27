# cfile

A C code generator written in Python 3.

## Documentation

Full documentation, guides, and API reference are available at **[cfile.readthedocs.io](https://cfile.readthedocs.io/en/latest/)**.

## Quick Example

```python
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.include_directive("stdio.h", sys=True))
code.append(C.blank())
char_ptr_type = C.type("char", pointer=True)
main_function = C.function("main",
                           "int",
                           params=[C.variable("argc", "int"),
                                   C.variable("argv", char_ptr_type, pointer=True)])
main_body = C.sequence([
    C.statement(C.fn_call("printf", C.str_literal(r"Hello World\n"))),
    C.statement(C.fn_return(0)),
])
code.append(C.declaration(main_function, main_body))
writer = cfile.Writer()
print(writer.write_str(code))
```

Output:

```c
#include <stdio.h>

int main(int argc, char** argv)
{
    printf("Hello World\n");
    return 0;
}
```

## Requirements

Python 3.10+ (required for modern type hinting syntax).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Versions

* **v0.2:** Legacy release (bug-fixes only).
* **v0.4:** Stable release.
* **v0.5:** Development track.
