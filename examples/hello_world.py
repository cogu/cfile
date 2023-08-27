"""
Simple hello world
"""
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.sysinclude("stdio.h"))
code.append(C.blank())
char_ptr_type = C.type("char", pointer=True)
code.append(C.function("main", "int").make_param("argc", "int").make_param("argv", char_ptr_type, pointer=True))
main_body = C.block()
main_body.append(C.statement(C.func_call("printf", C.str_literal(r"Hello World\n"))))
main_body.append(C.statement(C.func_return(0)))
code.append(main_body)
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
