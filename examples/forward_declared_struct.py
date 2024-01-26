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
