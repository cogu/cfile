"""
Examples of comments
"""
import cfile

C = cfile.CFactory()

code = C.sequence()
code.append(C.line_comment(" Simple line Comment "))
code.append(C.blank())
code.append(C.line(C.block_comment(" Simple Block Comment ")))
code.append(C.blank())
code.append(C.block_comment("*      SECTION      *", width=20))
code.append(C.blank())
code.append(C.block_comment(["Description 1", "Description 2", "Description 3"], width=20, line_start="* "))
code.append(C.blank())
code.append([C.statement(C.variable("value", "int")), C.line_comment(" Statement followed by comment", adjust=2)])
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
