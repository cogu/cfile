"""
Flow control statements and switch-statement example
"""
import cfile

C = cfile.CFactory()
block = C.block()
switch_var = C.variable("value", "int")
switch_body = C.block()
switch_body.append(C.switch_label(1))
switch_body.append(C.break_statement())
switch_body.append(C.switch_label(2))
switch_body.append(C.break_statement())
switch_body.append(C.switch_default())
switch_body.append(C.goto_statement("CLEANUP"))
block.append(C.switch(switch_var, switch_body))
block.append(C.continue_statement())
block.append(C.named_label("CLEANUP"))
code = C.sequence(block)
writer = cfile.Writer()
print(writer.write_str(code))
