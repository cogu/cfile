"""
Example of header file with type declaration
"""
import cfile

C = cfile.CFactory()

INCLUDE_GUARD_TEXT = "INCLUDE_GUARD_H"

code = C.sequence()
code.append(C.ifndef(INCLUDE_GUARD_TEXT))
code.append(C.define(INCLUDE_GUARD_TEXT))
code.append(C.blank())
code.append(C.ifndef("__cplusplus"))
code.append(C.line(C.extern("C")))
code.append(C.line("{"))
code.append(C.endif(adjust=1))
code.append(C.blank())
code.append(C.sysinclude("stdint.h"))
code.append(C.blank())
struct = C.struct("heap_tag", members=[C.struct_member("pItem", "void", pointer=True),
                                       C.struct_member("u32Value", "uint32_t")])
code.append(C.statement(C.typedef("heap_t", struct)))
code.append(C.blank())
code.append(C.ifndef("__cplusplus"))
code.append(C.line("}"))
code.append([C.endif(), C.line_comment(" __cplusplus")])
code.append([C.endif(), C.line_comment(" " + INCLUDE_GUARD_TEXT)])
writer = cfile.Writer(cfile.StyleOptions())
print(writer.write_str(code))
