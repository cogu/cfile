"""
Loop statements (for, while, do-while) example
"""
import cfile

C = cfile.CFactory()
code = C.sequence()

n = C.variable("n", "int")
sum_var = C.variable("sum", "int")
i = C.variable("i", "int")

compute_fn = C.function("compute_sum", "int", params=[n])
body = C.block([
    C.declaration_statement(sum_var, 0),
    C.for_statement(
        C.declaration(i, 0),
        f"{i} < {n}",
        f"{i}++",
        C.sequence(C.statement(f"{sum_var} += {i}")),
    ),
    C.while_statement(
        f"{sum_var} > 100",
        C.sequence(C.statement(f"{sum_var} -= 10")),
    ),
    C.do_while_statement(
        C.sequence(C.statement(f"{sum_var}++")),
        f"{sum_var} < 10",
    ),
    C.return_statement(sum_var),
])
code.append(C.declaration(compute_fn, body))

style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
