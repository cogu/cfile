import cfile

C = cfile.CFactory()

code = C.sequence()
mystruct = C.struct("mystruct",
                    members=[C.struct_member("field_1", "int"),
                             C.struct_member("field_2", "int")])
code.append(C.statement(C.declaration(C.typedef("mystruct_t", C.declaration(mystruct)))))
writer = cfile.Writer(cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH))
print(writer.write_str(code))
