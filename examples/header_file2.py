"""
Same as header_file.py but places the brace on the same line as extern declaration
"""
import cfile

C = cfile.CFactory()

code = C.sequence()
code.append(C.ifndef("INCLUDE_GUARD"))
code.append(C.define("INCLUDE_GUARD"))
code.append(C.blank())
code.append(C.ifndef("__cplusplus", adjust=1))
code.append([C.extern("C"), "{"])
code.append(C.endif(adjust=1))
code.append(C.blank())
code.append(C.statement(C.function("function_with_c_linkage", "int")))
code.append(C.blank())
code.append(C.ifndef("__cplusplus", adjust=1))
code.append(C.line(C.extern("C")))
code.append(C.line("}"))
code.append(C.endif(adjust=1))
code.append([C.endif(), C.line_comment(" INCLUDE_GUARD")])
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
