"""
Multi-variable declarations and comma-chained statements
"""
import cfile

C = cfile.CFactory()
code = C.sequence()

i = C.variable("i", "int")
j = C.variable("j", "int")
k = C.variable("k", "int", pointer=True)

code.append(C.multi_declaration_statement((i, 0), j, (k, "NULL")))
code.append(C.multi_statement(C.assignment(i, 2), C.assignment(j, 3)))

writer = cfile.Writer()
print(writer.write_str(code))
