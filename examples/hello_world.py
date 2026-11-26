"""
Simple hello world
"""
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
