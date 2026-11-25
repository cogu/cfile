"""
Enum declaration and prefix usage example
"""
import cfile

C = cfile.CFactory()
code = C.sequence()

color_enum = C.enum("color_tag", prefix="COLOR_")
red = color_enum.make_member("RED", 0)
green = color_enum.make_member("GREEN")
blue = color_enum.make_member("BLUE")

color_type = C.typedef("color_t", C.declaration(color_enum))
code.append(C.declaration_statement(color_type))
code.append(C.blank())

selected = C.variable("selected", color_type)
code.append(C.declaration_statement(selected, green))

style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
writer = cfile.Writer(style)
print(writer.write_str(code))
