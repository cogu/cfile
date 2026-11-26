"""
Same as cpp_check.py but places the "extern" brace on the same line as extern declaration
"""
import cfile

C = cfile.CFactory()

INCLUDE_GUARD_TEXT = "INCLUDE_GUARD_H"

code = C.sequence()
code.append(C.ifndef_directive(INCLUDE_GUARD_TEXT))
code.append(C.define_directive(INCLUDE_GUARD_TEXT))
code.append(C.blank())
code.append(C.ifndef_directive("__cplusplus"))
code.append([C.extern("C"), "{"])
code.append(C.endif_directive())
code.append(C.blank())
code.append(C.line_comment("PLACEHOLDER"))
code.append(C.blank())
code.append(C.ifndef_directive("__cplusplus"))
code.append(C.line("}"))
code.append([C.endif_directive(), C.line_comment("__cplusplus")])
code.append([C.endif_directive(), C.line_comment(INCLUDE_GUARD_TEXT)])
writer = cfile.Writer()
print(writer.write_str(code))
