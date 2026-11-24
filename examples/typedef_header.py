"""
Example header file with some type declarations
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
os_task_tag = C.struct("os_task_tag")
code.append([C.statement(os_task_tag), C.line_comment("Forward declaration")])
code.append(C.blank())
struct = C.struct("os_alarm_cfg_tag",
                  members=[C.struct_member("taskPtr", os_task_tag, pointer=True),
                           C.struct_member("eventMask", "uint32_t"),
                           C.struct_member("initDelayMs", "uint32_t"),
                           C.struct_member("periodMs", "uint32_t")])
code.append(C.statement(C.declaration(C.typedef("os_alarm_cfg_t", C.declaration(struct)))))
code.append(C.blank())
code.append(C.ifndef("__cplusplus"))
code.append(C.line("}"))
code.append([C.endif(), C.line_comment(" __cplusplus")])
code.append([C.endif(), C.line_comment(" " + INCLUDE_GUARD_TEXT)])

writer = cfile.Writer()
print(writer.write_str(code))
