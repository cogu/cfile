"""
Typedef of a struct then declare a variable of that struct with initializer.

Style:
- new-line after opening brace

"""
import cfile

C = cfile.CFactory()
code = C.sequence()
struct = C.struct("mystruct",
                  members=[C.struct_member("field_1", "int"),
                           C.struct_member("field_2", "int")])
struct_type = C.typedef("my_struct_t", C.declaration(struct))
code.append(C.statement(C.declaration(struct_type)))
code.append(C.blank())
code.append(C.statement(C.declaration(C.variable("instance", struct_type), [0, 0])))

writer = cfile.Writer(cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH))
print(writer.write_str(code))
