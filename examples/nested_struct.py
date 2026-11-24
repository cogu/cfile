"""
Nested struct and union declaration with positional and designated initializers
"""
import cfile

C = cfile.CFactory()
code = C.sequence()
code.append(C.sys_include("stdint.h"))
code.append(C.blank())
addr_struct = C.struct("addr_t", members=[C.struct_member("port", "uint32_t")])
in_union = C.union(members=[
    C.union_member("a8", "uint8_t", array=4),
    C.union_member("a16", "uint16_t", array=2),
])
example = C.struct("example", members=[
    C.struct_member("addr", C.declaration(addr_struct)),
    C.struct_member("in_u", C.declaration(in_union)),
])
code.append(C.statement(C.declaration(example)))
code.append(C.blank())
port = 80
ip_address = "127.0.0.1"
ex1 = C.variable("ex1", example)
ex2 = C.variable("ex2", example)
code.append(C.statement(C.declaration(ex1, [[port], [ip_address.split(".")]])))
code.append(C.statement(C.declaration(ex2, {"addr": {"port": port}, "in_u": {"a8": ip_address.split(".")}})))

style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
