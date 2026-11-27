"""
Function prototypes, definitions, and validated function calls
"""
import cfile

C = cfile.CFactory()
code = C.sequence()

a_var = C.variable("a", "int")
b_var = C.variable("b", "int")
add_fn = C.function("add", "int", static=True, params=[a_var, b_var])
compute_fn = C.function("compute", "int")

# Prototype declaration (with semicolon)
code.append(C.declaration_statement(add_fn))
code.append(C.blank())

# Function definition (with body sequence)
add_body = C.sequence([
    C.return_statement(f"{a_var} + {b_var}"),
])
code.append(C.declaration(add_fn, add_body))
code.append(C.blank())

# Calling add_fn using the Function object validates the argument count
result = C.variable("result", "int")
compute_body = C.sequence([
    C.declaration_statement(result, C.fn_call(add_fn, [10, 20])),
    C.return_statement(result),
])
code.append(C.declaration(compute_fn, compute_body))

style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
