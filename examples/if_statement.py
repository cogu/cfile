"""
If-statement example
"""
import cfile

C = cfile.CFactory()
code = C.sequence()
arg = C.variable("x", "int")
classify_fn = C.function("classify", "int", params=[arg])
body = C.block([
    C.if_statement(f"{arg} > 0", C.sequence(C.statement(C.fn_return(1))))
    .else_if(f"{arg} < 0", C.sequence(C.statement(C.fn_return(-1))))
    .else_branch(C.sequence(C.statement(C.fn_return(0))))
])
code.append(C.declaration(classify_fn, body))
style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
