"""
Aligned trailing comments and multi-line comments
"""
import cfile

C = cfile.CFactory()
code = C.sequence([
    C.line_comment(["Multi-line", "line comment"]),
    C.blank(),
    C.block_comment(["comment line 1", "comment line 2"], padding=4, absolute=True),
    C.blank(),
    [C.declaration_statement(C.variable("x", "int"), 1), C.line_comment("short", padding=24, absolute=True)],
    [C.declaration_statement(C.variable("counter", "int"), 2), C.line_comment("aligned", padding=24, absolute=True)],
    [
        C.declaration_statement(C.variable("very_long_variable_name", "int"), 3),
        C.line_comment("fallback padding=1", padding=24, absolute=True),
    ],
])

writer = cfile.Writer()
print(writer.write_str(code))
