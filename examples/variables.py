"""
Variable declarations and access
"""
import cfile

C = cfile.CFactory()
code = C.sequence()
var1 = C.variable("var1", "int")
var2 = C.variable("var2", "int")
code.append(C.statement(C.declaration(var1)))  # int var1;
code.append(C.statement(C.declaration(var2, 0)))  # int var2 = 0;
code.append(C.statement(var1))  # var1;
code.append(C.statement(C.assignment(var1, 0)))  # var1 = 0;
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
