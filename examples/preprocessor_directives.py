"""
Preprocessor directives with clang-format style indentation
"""
import cfile

C = cfile.CFactory()
code = C.sequence([
    C.ifndef_directive("APP_CONFIG_H"),
    C.define_directive("APP_CONFIG_H"),
    C.blank(),
    C.include_directive("stdint.h", sys=True),
    C.blank(),
    C.ifndef_directive("APP_MAX_LEN"),
    C.define_directive("APP_MAX_LEN", 256),
    C.endif_directive(),
    C.blank(),
    C.ifdef_directive("USE_FAST_PATH"),
    C.define_directive("MODE", 1),
    C.elifdef_directive("USE_SAFE_PATH"),
    C.define_directive("MODE", 2),
    C.else_directive(),
    C.warning_directive('"Falling back to default mode"'),
    C.define_directive("MODE", 0),
    C.endif_directive(),
    C.blank(),
    [C.endif_directive(), C.line_comment("APP_CONFIG_H")],
])

style = cfile.StyleOptions(
    indent_pp_directives=cfile.PPDirectiveIndent.AFTER_HASH,
    pp_indent_width=1,
)
writer = cfile.Writer(style)
print(writer.write_str(code))
