"""
Basic union declaration and initialization example
"""
import cfile

C = cfile.CFactory()
code = C.sequence()
raw_union = C.union("raw_value", members=[
    C.union_member("x", "int"),
    C.union_member("c", "char", array=4),
])
code.append(C.declaration_statement(raw_union))
code.append(C.blank())
code.append(C.declaration_statement(C.variable("u1", raw_union), [1]))
code.append(C.declaration_statement(C.variable("u2", raw_union), {"c": [1, 0, 0, 0]}))

style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
