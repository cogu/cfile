"""
Rendering the same C code sequence with different StyleOptions presets
"""
import cfile

C = cfile.CFactory()
x = C.variable("x", "int")
ptr = C.variable("ptr", "int", pointer=True)
check_fn = C.function("check", "int", params=[x, ptr])

body = C.sequence([
    C.if_statement(f"{ptr} == NULL", C.sequence(C.return_statement(-1)))
    .else_branch(C.sequence(C.return_statement(f"*{ptr} + {x}"))),
])
code = C.sequence(C.declaration(check_fn, body))

linux_style = cfile.StyleOptions(
    break_before_braces=cfile.BreakBeforeBraces.LINUX,
    pointer_alignment=cfile.Alignment.RIGHT,
    indent_width=2,
)
writer = cfile.Writer(linux_style)
print(writer.write_str(code))
