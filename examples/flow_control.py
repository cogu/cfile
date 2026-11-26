"""
Flow control statements and switch-statement example
"""
import cfile

C = cfile.CFactory()
switch_var = C.variable("value", "int")
switch_body = C.sequence()
switch_body.append(C.switch_label(1))
switch_body.append(C.break_statement())
switch_body.append(C.switch_label(2))
switch_body.append(C.break_statement())
switch_body.append(C.switch_default())
switch_body.append(C.goto_statement("CLEANUP"))
code = C.sequence([
    C.switch(switch_var, switch_body),
    C.continue_statement(),
    C.named_label("CLEANUP"),
])
writer = cfile.Writer()
print(writer.write_str(code))
