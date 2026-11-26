"""Unit tests for writer class"""

# noqa D101
# pylint: disable=missing-class-docstring, missing-function-docstring
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cfile.core as core # noqa E402
import cfile.style as style # noqa E402
import cfile # noqa E402


class TestWhitespace(unittest.TestCase):

    def test_write_blank(self):
        element = core.Blank()
        writer = cfile.Writer()
        output = writer.write_str_elem(element)
        self.assertEqual(output, "")

    def test_write_white_space(self):
        element = core.Whitespace(4)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "    ")


class TestComment(unittest.TestCase):

    def test_line_comment(self):
        element = core.LineComment(" Comment")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "// Comment")

    def test_single_line_block_comment(self):
        element = core.BlockComment(" Comment ")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "/* Comment */")

    def test_multi_line_block_comment(self):
        comment = """ Line 1
Line 2
Line 3
Line 4 """
        element = core.BlockComment(comment)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        expected = """/* Line 1
Line 2
Line 3
Line 4 */"""
        self.assertEqual(expected, output)

    def test_block_comment_with_user_defined_width_and_line_start__str_input(self):
        comment = """Line 1
Line 2
Line 3
Line 4"""
        element = core.BlockComment(comment, width=10, line_start="* ")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        expected = """/**********
* Line 1
* Line 2
* Line 3
* Line 4
***********/"""
        self.assertEqual(expected, output)

    def test_block_comment_with_user_defined_width_and_line_start__list_input(self):
        comment = ["Line 1", "Line 2", "Line 3", "Line 4"]
        element = core.BlockComment(comment, width=10, line_start="* ")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element, trim_end=False)
        expected = """/**********
* Line 1
* Line 2
* Line 3
* Line 4
***********/
"""
        self.assertEqual(expected, output)


class TestPreprocessor(unittest.TestCase):

    def test_custom_directive(self):
        C = cfile.CFactory()
        element = C.directive("ident \"@(#)main.c\"")
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#ident "@(#)main.c"')

    def test_normal_include(self):
        C = cfile.CFactory()
        element = C.include_directive("path/to/file.h")
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#include "path/to/file.h"')

    def test_system_include(self):
        C = cfile.CFactory()
        element = C.include_directive("stdio.h", sys=True)
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#include <stdio.h>')

    def test_define_with_left_part_only(self):
        C = cfile.CFactory()
        element = C.define_directive("INCLUDE_GUARD")
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#define INCLUDE_GUARD')

    def test_define_with_left_and_right(self):
        C = cfile.CFactory()
        element = C.define_directive("MAX(a,b)", "int_max(a,b)")
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#define MAX(a,b) int_max(a,b)')

    def test_undef(self):
        C = cfile.CFactory()
        element = C.undef_directive("TEMP_MACRO")
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(element), '#undef TEMP_MACRO')

    def test_if_elif_else_endif(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(C.if_directive("VERSION >= 2")), '#if VERSION >= 2')
        self.assertEqual(writer.write_str_elem(C.elif_directive("VERSION == 1")), '#elif VERSION == 1')
        self.assertEqual(writer.write_str_elem(C.else_directive()), '#else')
        self.assertEqual(writer.write_str_elem(C.endif_directive()), '#endif')

    def test_ifdef_and_ifndef(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(C.ifdef_directive("IDENTIFIER")), '#ifdef IDENTIFIER')
        self.assertEqual(writer.write_str_elem(C.ifndef_directive("IDENTIFIER")), '#ifndef IDENTIFIER')

    def test_line_error_and_pragma_directives(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(C.line_directive(42)), '#line 42')
        self.assertEqual(writer.write_str_elem(C.line_directive(42, "gen.c")), '#line 42 "gen.c"')
        self.assertEqual(writer.write_str_elem(C.error_directive('"Unsupported"')), '#error "Unsupported"')
        self.assertEqual(writer.write_str_elem(C.warning_directive('"Deprecated"')), '#warning "Deprecated"')
        self.assertEqual(writer.write_str_elem(C.pragma_directive("once")), '#pragma once')

    def test_c23_and_extension_directives(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        self.assertEqual(writer.write_str_elem(C.include_next_directive("limits.h", sys=True)),
                         '#include_next <limits.h>')
        self.assertEqual(writer.write_str_elem(C.include_next_directive("local.h")),
                         '#include_next "local.h"')
        self.assertEqual(writer.write_str_elem(C.embed_directive("icon.png")),
                         '#embed "icon.png"')
        self.assertEqual(writer.write_str_elem(C.embed_directive("data.bin", sys=True, params="limit(256)")),
                         '#embed <data.bin> limit(256)')
        self.assertEqual(
            writer.write_str_elem(C.embed_directive("blob.bin", params=["limit(64)", "if_empty(0)"])),
            '#embed "blob.bin" limit(64) if_empty(0)'
        )
        self.assertEqual(writer.write_str_elem(C.elifdef_directive("FOO")), '#elifdef FOO')
        self.assertEqual(writer.write_str_elem(C.elifndef_directive("BAR")), '#elifndef BAR')

        code = C.sequence([
            C.ifdef_directive("PLATFORM_A"),
            C.define_directive("TARGET", 1),
            C.elifdef_directive("PLATFORM_B"),
            C.define_directive("TARGET", 2),
            C.elifndef_directive("NO_FALLBACK"),
            C.warning_directive('"Using fallback target"'),
            C.define_directive("TARGET", 0),
            C.endif_directive(),
        ])
        indented_writer = cfile.Writer(
            cfile.StyleOptions(
                indent_pp_directives=style.PPDirectiveIndent.AFTER_HASH,
                pp_indent_width=1,
            )
        )
        expected = "\n".join([
            "#ifdef PLATFORM_A",
            "# define TARGET 1",
            "#elifdef PLATFORM_B",
            "# define TARGET 2",
            "#elifndef NO_FALLBACK",
            '# warning "Using fallback target"',
            "# define TARGET 0",
            "#endif",
        ])
        self.assertEqual(expected, indented_writer.write_str(code))

    def test_pp_indent_after_hash_with_include_guard(self):
        C = cfile.CFactory()
        code = C.sequence([
            C.ifndef_directive("OS_MACRO_H"),
            C.define_directive("OS_MACRO_H"),
            C.blank(),
            C.ifdef_directive("_WIN32"),
            C.ifndef_directive("WIN32_LEAN_AND_MEAN"),
            C.define_directive("WIN32_LEAN_AND_MEAN"),
            C.endif_directive(),
            C.include_directive("Windows.h", sys=True),
            C.else_directive(),
            C.include_directive("unistd.h", sys=True),
            C.endif_directive(),
            [C.endif_directive(), C.line_comment(" OS_MACRO_H")],
        ])
        opts = cfile.StyleOptions(
            indent_pp_directives=style.PPDirectiveIndent.AFTER_HASH,
            pp_indent_width=1,
        )
        writer = cfile.Writer(opts)
        expected = "\n".join([
            "#ifndef OS_MACRO_H",
            "#define OS_MACRO_H",
            "",
            "#ifdef _WIN32",
            "# ifndef WIN32_LEAN_AND_MEAN",
            "#  define WIN32_LEAN_AND_MEAN",
            "# endif",
            "# include <Windows.h>",
            "#else",
            "# include <unistd.h>",
            "#endif",
            "#endif // OS_MACRO_H",
        ])
        self.assertEqual(expected, writer.write_str(code))

    def test_pp_indent_before_hash(self):
        C = cfile.CFactory()
        code = C.sequence([
            C.ifdef_directive("FOO"),
            C.define_directive("BAR", 1),
            C.endif_directive(),
        ])
        opts = cfile.StyleOptions(
            indent_pp_directives=style.PPDirectiveIndent.BEFORE_HASH,
            pp_indent_width=2,
        )
        writer = cfile.Writer(opts)
        expected = "\n".join([
            "#ifdef FOO",
            "  #define BAR 1",
            "#endif",
        ])
        self.assertEqual(expected, writer.write_str(code))


class TestTypeDeclarations(unittest.TestCase):
    def test_basic_int(self):
        element = core.Declaration(core.Type("int"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int")

    def test_const_int(self):
        element = core.Declaration(core.Type("int", const=True))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int")

    def test_basic_int_ptr_left_align(self):
        element = core.Declaration(core.Type("int", pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int*")

    def test_basic_int_ptr_right_align(self):
        element = core.Declaration(core.Type("int", pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int *")

    def test_basic_int_ptr_middle_align(self):
        element = core.Declaration(core.Type("int", pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.MIDDLE))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int *")

    def test_const_int_ptr_left_align(self):
        element = core.Declaration(core.Type("int", const=True, pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int*")

    def test_const_int_ptr_right_align(self):
        element = core.Declaration(core.Type("int", const=True, pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int *")

    def test_nested_ptr_to_int_ptr__left_align(self):
        element = core.Declaration(core.Type(core.Type("int", pointer=True), pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int**")


class TestVariableInstance(unittest.TestCase):

    def test_writing_variable_instance_will_only_produce_its_name(self):
        element = core.Variable("value", "int")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "value")

    def test_str_helper_returns_identifier_name(self):
        var = core.Variable("value", "int")
        member = core.StructMember("field", "int")
        func = core.Function("compute", "int")
        typedef = core.TypeDef("my_int_t", "int")
        self.assertEqual(f"{var} > 0", "value > 0")
        self.assertEqual(f"{var}.{member}", "value.field")
        self.assertEqual(str(func), "compute")
        self.assertEqual(str(typedef), "my_int_t")


class TestVariableDeclaration(unittest.TestCase):

    def test_declare_int_variable_from_string_type_name(self):
        element = core.Declaration(core.Variable("value", "int"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int value")

    def test_declaration_statement_shorthand(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        var = C.variable("count", "int")
        self.assertEqual("int count;", writer.write_str_elem(C.declaration_statement(var)))
        self.assertEqual("int count = 42;", writer.write_str_elem(C.declaration_statement(var, 42)))

    def test_declare_int_variable(self):
        element = core.Declaration(core.Variable("value", core.Type("int")))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int value")

    def test_type_is_const_int(self):
        element = core.Declaration(core.Variable("value", core.Type("int", const=True)))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int value")

    def test_type_is_int_ptr(self):
        element = core.Declaration(core.Variable("value", core.Type("int", pointer=True)))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int* value")

    def test_type_is_int_ptr__right_align(self):
        element = core.Declaration(core.Variable("value", core.Type("int", pointer=True)))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int *value")

    def test_type_is_int__var_is_ptr(self):
        element = core.Declaration(core.Variable("value", core.Type("int"), pointer=True))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int* value")

    def test_type_is_int__var_is_ptr__right_align(self):
        element = core.Declaration(core.Variable("value", core.Type("int"), pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int *value")

    def test_type_is_int_ptr__var_is_ptr__left_align(self):
        element = core.Declaration(core.Variable("value", core.Type("int", pointer=True), pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int** value")

    def test_type_is_int_ptr__var_is_ptr__right_align(self):
        element = core.Declaration(core.Variable("value", core.Type("int", pointer=True), pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int **value")

    def test_type_is_str_containing_ptr__var_is_ptr___left_align(self):
        element = core.Declaration(core.Variable("value", "int*", pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int** value")

    def test_type_is_str_containing_ptr__var_is_ptr__right_align(self):
        # Manually adding '*' to the data type name is highly discouraged.
        # It causes very strange formatting.
        element = core.Declaration(core.Variable("value", "int*", pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int* *value")

    def test_type_is_int__var_is_const_ptr__left_align(self):
        element = core.Declaration(core.Variable("value", core.Type("int"), const=True, pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int* const value")

    def test_type_is_const_int_ptr__var_is_const_ptr__left_align(self):
        element = core.Declaration(core.Variable("value",
                                                 core.Type("int", const=True, pointer=True),
                                                 const=True,
                                                 pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.LEFT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int** const value")

    def test_type_is_const_int_ptr__var_is_const_ptr__right_align(self):
        element = core.Declaration(core.Variable("value",
                                                 core.Type("int", const=True, pointer=True),
                                                 const=True,
                                                 pointer=True))
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(element)
        self.assertEqual(output, "const int **const value")


class TestFunctionDeclaration(unittest.TestCase):

    def test_void_no_args(self):
        element = core.Declaration(core.Function("my_func", "void"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "void my_func(void)")

    def test_extern_void_no_args(self):
        element = core.Declaration(core.Function("my_func", "void", extern=True))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "extern void my_func(void)")

    def test_static_void_no_args(self):
        element = core.Declaration(core.Function("my_func", "void", static=True))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "static void my_func(void)")

    def test_int_ptr_no_args(self):
        element = core.Declaration(core.Function("my_func", core.Type("int", pointer=True)))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int* my_func(void)")

    def test_void_int_arg_using_make_param(self):
        element = core.Declaration(core.Function("my_func", "void").make_param("arg1", "int"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "void my_func(int arg1)")

    def test_void_int_arg_using_append(self):
        element = core.Declaration(core.Function("my_func", "void").append(core.Variable("arg1", "int")))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "void my_func(int arg1)")

    def test_void_int_arg_using_params_arg(self):
        element = core.Declaration(core.Function("my_func", "void", params=[core.Variable("arg1", "int")]))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "void my_func(int arg1)")

    def test_int_func_with_int_arg_and_char_double_ptr_arg(self):
        func = core.Function("main", "int")
        func.make_param("argc", "int").make_param("argv", core.Type(core.Type("char", pointer=True), pointer=True))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(func))
        self.assertEqual(output, "int main(int argc, char** argv)")

    def test_function_declaration_with_body_content(self):
        C = cfile.CFactory()
        func = C.function("add", "int", params=[C.variable("a", "int"), C.variable("b", "int")])
        body = C.sequence(C.return_statement("a + b"))
        decl = C.declaration(func, body)

        allman_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        expected_allman = "\n".join(["int add(int a, int b)", "{", "    return a + b;", "}"])
        self.assertEqual(expected_allman, allman_writer.write_str_elem(decl))

        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected_attach = "\n".join(["int add(int a, int b) {", "    return a + b;", "}"])
        self.assertEqual(expected_attach, attach_writer.write_str_elem(decl))


class TestAssignment(unittest.TestCase):

    def test_assign_var(self):
        a_var = core.Variable("a", "int")
        element = core.Assignment(a_var, 0)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "a = 0")


class TestStatement(unittest.TestCase):

    def test_int_variable_declaration(self):
        element = core.Statement(core.Declaration(core.Variable("a", "int")))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int a;")

    def test_int_variable_declaration_with_initializer(self):
        element = core.Statement(core.Declaration(core.Variable("a", "int"), 0))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int a = 0;")

    def test_struct_ref_variable_declaration(self):
        struct_type = core.Struct("record_t")
        element = core.Statement(core.Declaration(core.Variable("a", struct_type)))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "struct record_t a;")

    def test_struct_with_int_initializer(self):
        struct_type = core.Struct("record_t")
        element = core.Statement(core.Declaration(core.Variable("a", struct_type), [0, 0]))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "struct record_t a = {0, 0};")

    def test_struct_ref_with_int_initializer(self):
        struct_type = core.Struct("record_tag")
        typedef = core.TypeDef("record_t", struct_type)
        element = core.Statement(core.Declaration(core.Variable("a", typedef), [0, 0]))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "record_t a = {0, 0};")

    def test_const_str_var_with_str_literal_initializer(self):
        char_type = core.Type("char", const=True, pointer=True)
        element = core.Statement(core.Declaration(core.Variable("s", char_type), core.StringLiteral("Static Text")))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, 'const char* s = "Static Text";')

    def test_int_var_with_str_expression_initializer(self):
        element = core.Statement(core.Declaration(core.Variable("a", "int"), "DEFAULT_VAL"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int a = DEFAULT_VAL;")


class TestSequence(unittest.TestCase):

    def test_variable_declarations(self):
        seq = core.Sequence()
        seq.append(core.Statement(core.Declaration(core.Variable("a", "int", static=True))))
        seq.append(core.Statement(core.Declaration(core.Variable("b", core.Type("void", pointer=True), static=True))))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "static int a;\n" + "static void* b;"
        self.assertEqual(expected, output)

    def test_variable_declaration_and_comment_using_line_element(self):
        seq = core.Sequence()
        seq.append(core.Line([core.Statement(core.Declaration(core.Variable("a", "int"))),
                              core.BlockComment(" Comment ")]))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "int a; /* Comment */"
        self.assertEqual(expected, output)

    def test_variable_declaration_and_comment_using_python_list(self):
        seq = core.Sequence()
        seq.append([core.Statement(core.Declaration(core.Variable("a", "int"))), core.BlockComment(" Comment ")])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "int a; /* Comment */"
        self.assertEqual(expected, output)


class TestBlock(unittest.TestCase):

    def test_wrap_brace_after_function(self):
        seq = core.Sequence()
        seq.append(core.Declaration(core.Function("f")))
        seq.append(core.Sequence())
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        output = writer.write_str(seq)
        expected = "\n".join(["void f(void)", "{", "}"])
        self.assertEqual(expected, output)

    def test_attach_brace_to_function(self):
        seq = core.Sequence()
        seq.append(core.Declaration(core.Function("f")))
        seq.append(core.Sequence())
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        output = writer.write_str(seq)
        expected = "\n".join(["void f(void) {", "}"])
        self.assertEqual(expected, output)

    def test_variable_declarations(self):
        block = core.Sequence()
        block.append(core.Statement(core.Declaration(core.Variable("a", "int"))))
        block.append(core.Statement(core.Declaration(core.Variable("b", "int"))))
        block.append(core.Statement(core.Declaration(core.Variable("c", "int"))))
        writer = cfile.Writer(cfile.StyleOptions())
        expected = "\n".join(["{", "    int a;", "    int b;", "    int c;", "}"])
        output = writer.write_str_elem(block)
        self.assertEqual(expected, output)

    def test_function_definition(self):
        seq = core.Sequence()
        seq.append(core.Declaration(core.Function("add", "int").make_param("a", "int").make_param("b", "int")))
        body = core.Sequence()
        body.append(core.Statement("return a + b"))
        seq.append(body)
        allman_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        output = allman_writer.write_str(seq)
        expected = "\n".join(["int add(int a, int b)", "{", "    return a + b;", "}"])
        self.assertEqual(expected, output)
        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        output = attach_writer.write_str(seq)
        expected = "\n".join(["int add(int a, int b) {", "    return a + b;", "}"])
        self.assertEqual(expected, output)

    def test_struct_declaration_inside_block(self):
        outer = core.Sequence()
        inner = core.Sequence()
        outer.append(inner)
        struct = core.Struct("IntPair", members=[core.StructMember("first", "int"),
                                                 core.StructMember("second", "int")])
        inner.append(core.Statement(core.Declaration(struct)))
        allman_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        output = allman_writer.write_str(outer)
        expected = """{
    struct IntPair
    {
        int first;
        int second;
    };
}"""
        self.assertEqual(expected, output)


class TestStringLiteral(unittest.TestCase):

    def test_basic_string(self):
        element = core.StringLiteral("Test")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '"Test"')

    def test_raw_string(self):
        element = core.StringLiteral(r"Row1\nRow2\n")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, r'"Row1\nRow2\n"')


class TestFunctionCall(unittest.TestCase):

    def test_call_with_no_args(self):
        element = core.FunctionCall("f")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "f()")

    def test_call_with_one_arg(self):
        element = core.FunctionCall("f", args=[0])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "f(0)")

    def test_call_with_two_args_direct(self):
        element = core.FunctionCall("f", args=["i++", "enabled"])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "f(i++, enabled)")

    def test_call_with_two_args_chained(self):
        element = core.FunctionCall("f").append("i++").append("enabled")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "f(i++, enabled)")

    def test_call_using_function_object_no_args(self):
        C = cfile.CFactory()
        func = C.function("do_work", "void")
        element = C.fn_call(func)
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual("do_work()", writer.write_str_elem(element))

    def test_call_using_function_object_with_args(self):
        C = cfile.CFactory()
        func = C.function("add", "int", params=[C.variable("a", "int"), C.variable("b", "int")])
        x_var = C.variable("x", "int")
        element = C.fn_call(func, [x_var, 10])
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual("add(x, 10)", writer.write_str_elem(element))

    def test_call_using_function_object_wrong_arg_count_raises(self):
        C = cfile.CFactory()
        func = C.function("add", "int", params=[C.variable("a", "int"), C.variable("b", "int")])
        with self.assertRaises(ValueError):
            C.fn_call(func)
        with self.assertRaises(ValueError):
            C.fn_call(func, 1)
        with self.assertRaises(ValueError):
            C.fn_call(func, [1, 2, 3])


class TestFunctionReturn(unittest.TestCase):

    def test_int(self):
        element = core.FunctionReturn(0)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "return 0")

    def test_float(self):
        element = core.FunctionReturn(0.0)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "return 0.0")

    def test_bool(self):
        element = core.FunctionReturn(False)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "return false")

    def test_str(self):
        element = core.FunctionReturn("retval")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "return retval")

    def test_fn_call(self):
        C = cfile.CFactory()
        a_var = C.variable("a", "int")
        b_var = C.variable("b", "int")
        subtract = C.function("subtract", "int", params=[a_var, b_var])
        stmt = C.statement(C.fn_return(C.fn_call(subtract, [a_var, b_var])))
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual("return subtract(a, b);", writer.write_str_elem(stmt))


class TestTypedef(unittest.TestCase):

    def test_type_is_int(self):
        datatype = core.TypeDef("MyInt", "int")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef int MyInt")

    def test_type_is_const_int(self):
        datatype = core.TypeDef("MyConstInt", "int", const=True)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef const int MyConstInt")

    def test_type_is_int_ptr(self):
        datatype = core.TypeDef("MyIntPtr", "int", pointer=True)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef int* MyIntPtr")

    def test_type_is_int_ptr__right_align(self):
        datatype = core.TypeDef("MyIntPtr", "int", pointer=True)
        writer = cfile.Writer(
            cfile.StyleOptions(pointer_alignment=style.Alignment.RIGHT))
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef int *MyIntPtr")

    def test_type_is_int__typedf_is_ptr(self):
        datatype = core.TypeDef("MyIntPtr", core.Type("int"), pointer=True)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef int* MyIntPtr")

    def test_type_is_int_ptr__typedef_is_ptr_left_align(self):
        datatype = core.TypeDef("MyIntPtrPtr", core.Type("int", pointer=True), pointer=True)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(datatype))
        self.assertEqual(output, "typedef int** MyIntPtrPtr")


class TestLine(unittest.TestCase):

    def test_str_line(self):
        element = core.Line("Any code expression")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element, trim_end=False)
        self.assertEqual(output, "Any code expression\n")

    def test_statement_with_comment(self):
        element = core.Line([core.Statement(core.Declaration(core.Variable("value", "int"))),
                             core.LineComment("Comment")])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element, trim_end=False)
        self.assertEqual(output, "int value; //Comment\n")


class TestExtern(unittest.TestCase):

    def test_typical_cplusplus_check(self):
        code = core.Sequence()
        code.append(core.IfdefDirective("__cplusplus"))
        code.append(core.Line(core.Extern("C")))
        code.append(core.Line("{"))
        code.append(core.Line("}"))
        code.append([core.EndifDirective(), core.LineComment(" __clpusplus")])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(code)
        expected = """#ifdef __cplusplus
extern "C"
{
}
#endif // __clpusplus"""
        self.assertEqual(expected, output)


class TestStructDeclaration(unittest.TestCase):

    def test_zero_sized_struct(self):
        struct = core.Struct("MyStruct")
        writer = cfile.Writer(cfile.StyleOptions())
        expected = """struct MyStruct
{
}"""
        self.assertEqual(expected, writer.write_str_elem(core.Declaration(struct)))

    def test_struct_with_int_member(self):
        struct = core.Struct("MyStruct", members=core.StructMember("first", "int"))
        writer = cfile.Writer(cfile.StyleOptions())
        expected = """struct MyStruct
{
    int first;
}"""
        self.assertEqual(expected, writer.write_str_elem(core.Declaration(struct)))

    def test_typedef_struct_statement(self):
        struct = core.Struct("Struct_IntPair",
                             members=[core.StructMember("first", "int"),
                                      core.StructMember("second", "int")])
        statement = core.Statement(core.Declaration(core.TypeDef("IntPair_T", core.Declaration(struct))))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(statement)
        expected = """typedef struct Struct_IntPair
{
    int first;
    int second;
} IntPair_T;"""
        self.assertEqual(expected, output)

    def test_struct_declaration_with_struct_ref_member(self):
        struct = core.Struct("os_alarm_cfg_tag",
                             members=[core.StructMember("taskPtr", core.Struct("os_task_tag"), pointer=True),
                                      core.StructMember("eventMask", "uint32_t"),
                                      core.StructMember("initDelayMs", "uint32_t"),
                                      core.StructMember("periodMs", "uint32_t")])
        statement = core.Statement(core.Declaration(core.TypeDef("os_alarm_cfg_t", core.Declaration(struct))))
        writer = cfile.Writer(cfile.StyleOptions())
        expected = """typedef struct os_alarm_cfg_tag
{
    struct os_task_tag* taskPtr;
    uint32_t eventMask;
    uint32_t initDelayMs;
    uint32_t periodMs;
} os_alarm_cfg_t;"""
        self.assertEqual(expected, writer.write_str_elem(statement))


class TestStructReference(unittest.TestCase):

    def test_struct_variable(self):
        struct = core.Variable("time", core.Struct("timespec"))
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual('struct timespec time', writer.write_str_elem(core.Declaration(struct)))

    def test_struct_parameter(self):
        func = core.Function("process_time", "void", params=[core.Variable("time",
                                                             core.Struct("timespec"))])
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual('void process_time(struct timespec time)', writer.write_str_elem(core.Declaration(func)))

    def test_struct_return_and_struct_parameter(self):
        func = core.Function("timespec_add",
                             core.Struct("timespec"),
                             static=True,
                             params=[core.Variable("time1", core.Struct("timespec")),
                                     core.Variable("time2", core.Struct("timespec"))])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(core.Declaration(func))
        self.assertEqual('static struct timespec timespec_add(struct timespec time1, struct timespec time2)', output)

    def test_struct_forward_declaration(self):
        """
        Forward declaration of struct as a separate statement
        """
        struct = core.Statement(core.Struct("os_task_tag"))
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual('struct os_task_tag;', writer.write_str_elem(struct))


class TestIfStatement(unittest.TestCase):

    def test_single_if_with_statement(self):
        C = cfile.CFactory()
        if_stmt = C.if_statement("a > 0", C.statement("a = 0"))
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual("if (a > 0) a = 0;", writer.write_str_elem(if_stmt))

    def test_if_else_if_else_with_statements(self):
        C = cfile.CFactory()
        if_stmt = (
            C.if_statement("x == 1", C.statement("y = 10"))
            .else_if("x == 2", C.statement("y = 20"))
            .else_branch(C.statement("y = 30"))
        )
        writer = cfile.Writer(cfile.StyleOptions())
        expected = "\n".join([
            "if (x == 1) y = 10;",
            "else if (x == 2) y = 20;",
            "else y = 30;",
        ])
        self.assertEqual(expected, writer.write_str_elem(if_stmt))

    def test_if_else_if_else_using_append(self):
        C = cfile.CFactory()
        if_stmt = C.if_statement()
        if_stmt.append("x == 1", C.statement("y = 10"))
        if_stmt.append("x == 2", C.statement("y = 20"))
        if_stmt.append(None, C.statement("y = 30"))
        writer = cfile.Writer(cfile.StyleOptions())
        expected = "\n".join([
            "if (x == 1) y = 10;",
            "else if (x == 2) y = 20;",
            "else y = 30;",
        ])
        self.assertEqual(expected, writer.write_str_elem(if_stmt))

    def test_if_else_if_else_with_sequence_allman(self):
        C = cfile.CFactory()
        if_stmt = (
            C.if_statement("a > 0", C.sequence(C.statement("a = 1")))
            .else_if("b > 0", C.sequence([C.statement("b = 1"), C.statement("a = 2")]))
            .else_branch(C.sequence(C.statement("a = 0")))
        )
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        expected = "\n".join([
            "if (a > 0)",
            "{",
            "    a = 1;",
            "}",
            "else if (b > 0)",
            "{",
            "    b = 1;",
            "    a = 2;",
            "}",
            "else",
            "{",
            "    a = 0;",
            "}",
        ])
        self.assertEqual(expected, writer.write_str_elem(if_stmt))

    def test_if_else_if_else_with_sequence_attach(self):
        C = cfile.CFactory()
        if_stmt = (
            C.if_statement("a > 0", C.sequence(C.statement("a = 1")))
            .else_if("b > 0", C.sequence(C.statement("b = 1")))
            .else_branch(C.sequence(C.statement("a = 0")))
        )
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "if (a > 0) {",
            "    a = 1;",
            "} else if (b > 0) {",
            "    b = 1;",
            "} else {",
            "    a = 0;",
            "}",
        ])
        self.assertEqual(expected, writer.write_str_elem(if_stmt))

    def test_if_inside_function_body(self):
        C = cfile.CFactory()
        code = C.sequence()
        code.append(C.declaration(C.function("check", "int", params=[C.variable("x", "int")])))
        body = C.sequence()
        body.append(
            C.if_statement("x > 0", C.sequence(C.statement(C.fn_return(1))))
            .else_branch(C.sequence(C.statement(C.fn_return(0))))
        )
        code.append(body)
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "int check(int x) {",
            "    if (x > 0) {",
            "        return 1;",
            "    } else {",
            "        return 0;",
            "    }",
            "}",
        ])
        self.assertEqual(expected, writer.write_str(code))

    def test_complex_condition_with_sequence(self):
        C = cfile.CFactory()
        j_var = C.variable("j", "int")
        init_stmt = C.statement(C.declaration(j_var, C.fn_call("call_some_function", ["x", "y"])))
        cond = C.sequence([init_stmt, "j > 0 && j < 24"])
        if_stmt = C.if_statement(cond, C.sequence(C.statement(C.fn_return(j_var))))
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "if (int j = call_some_function(x, y); j > 0 && j < 24) {",
            "    return j;",
            "}",
        ])
        self.assertEqual(expected, writer.write_str_elem(if_stmt))

    def test_cannot_append_after_else_branch(self):
        C = cfile.CFactory()
        if_stmt = C.if_statement("a > 0", C.statement("a = 1")).else_branch(C.statement("a = 0"))
        with self.assertRaises(RuntimeError):
            if_stmt.append("b > 0", C.statement("b = 1"))
        with self.assertRaises(RuntimeError):
            if_stmt.else_branch(C.statement("b = 0"))

    def test_first_branch_must_have_condition(self):
        C = cfile.CFactory()
        if_stmt = C.if_statement()
        with self.assertRaises(ValueError):
            if_stmt.append(None, C.statement("a = 0"))


class TestFlowControlAndSwitch(unittest.TestCase):

    def test_break_continue_goto_and_named_label(self):
        C = cfile.CFactory()
        writer = cfile.Writer(cfile.StyleOptions())
        cleanup = C.named_label("CLEANUP")
        self.assertEqual("break;", writer.write_str_elem(C.break_statement()))
        self.assertEqual("continue;", writer.write_str_elem(C.continue_statement()))
        self.assertEqual("goto CLEANUP;", writer.write_str_elem(C.goto_statement("CLEANUP")))
        self.assertEqual("goto CLEANUP;", writer.write_str_elem(C.goto_statement(cleanup)))
        self.assertEqual("CLEANUP:", writer.write_str_elem(cleanup))

    def test_void_return(self):
        C = cfile.CFactory()
        writer = cfile.Writer(cfile.StyleOptions())
        self.assertEqual("return;", writer.write_str_elem(C.statement(C.fn_return())))
        self.assertEqual("return;", writer.write_str_elem(C.return_statement()))
        self.assertEqual("return 0;", writer.write_str_elem(C.return_statement(0)))

    def test_switch_allman_default_case_indent(self):
        C = cfile.CFactory()
        code = C.sequence()
        switch_var = C.variable("value", "int")
        switch_body = C.sequence([
            C.switch_label(1),
            C.break_statement(),
            C.switch_label(2),
            C.break_statement(),
            C.switch_default(),
            C.goto_statement("CLEANUP"),
        ])
        code.append(C.switch(switch_var, switch_body))
        code.append(C.continue_statement())
        code.append(C.named_label("CLEANUP"))
        writer = cfile.Writer(cfile.StyleOptions())
        expected = "\n".join([
            "switch (value)",
            "{",
            "case 1:",
            "    break;",
            "case 2:",
            "    break;",
            "default:",
            "    goto CLEANUP;",
            "}",
            "continue;",
            "CLEANUP:",
        ])
        self.assertEqual(expected, writer.write_str(code))

    def test_switch_attach_with_indented_case_labels(self):
        C = cfile.CFactory()
        switch_var = C.variable("mode", "int")
        switch_body = C.sequence([
            C.switch_label("MODE_A"),
            C.statement("x = 1"),
            C.break_statement(),
            C.switch_default(),
            C.statement("x = 0"),
            C.break_statement(),
        ])
        stmt = C.switch(switch_var, switch_body)
        opts = cfile.StyleOptions(
            break_before_braces=style.BreakBeforeBraces.ATTACH,
            indent_case_labels=True,
        )
        writer = cfile.Writer(opts)
        expected = "\n".join([
            "switch (mode) {",
            "    case MODE_A:",
            "        x = 1;",
            "        break;",
            "    default:",
            "        x = 0;",
            "        break;",
            "}",
        ])
        self.assertEqual(expected, writer.write_str_elem(stmt))

    def test_switch_case_blocks_styles(self):
        C = cfile.CFactory()
        switch_var = C.variable("x", "int")
        case_block = C.sequence([
            C.statement(C.declaration(C.variable("tmp", "int"), 1)),
            C.break_statement(),
        ])
        stmt = C.switch(switch_var, C.sequence([C.switch_label(1), case_block]))

        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected_attach = "\n".join([
            "switch (x) {",
            "case 1: {",
            "    int tmp = 1;",
            "    break;",
            "}",
            "}",
        ])
        self.assertEqual(expected_attach, attach_writer.write_str_elem(stmt))

        indented_block_writer = cfile.Writer(
            cfile.StyleOptions(
                break_before_braces=style.BreakBeforeBraces.ALLMAN,
                indent_case_blocks=True,
            )
        )
        expected_indented = "\n".join([
            "switch (x)",
            "{",
            "case 1:",
            "    {",
            "        int tmp = 1;",
            "        break;",
            "    }",
            "}",
        ])
        self.assertEqual(expected_indented, indented_block_writer.write_str_elem(stmt))

    def test_goto_label_indentation_inside_function(self):
        C = cfile.CFactory()
        cleanup = C.named_label("CLEANUP")
        body = C.sequence([
            C.if_statement("err", C.sequence([C.goto_statement(cleanup), C.named_label("INNER")])),
            cleanup,
            C.statement(C.fn_return(0)),
        ])
        writer_indented = cfile.Writer(cfile.StyleOptions(indent_goto_labels=True))
        expected_indented = "\n".join([
            "{",
            "    if (err)",
            "    {",
            "        goto CLEANUP;",
            "    INNER:",
            "    }",
            "CLEANUP:",
            "    return 0;",
            "}",
        ])
        self.assertEqual(expected_indented, writer_indented.write_str_elem(body))

        writer_unindented = cfile.Writer(cfile.StyleOptions(indent_goto_labels=False))
        expected_unindented = "\n".join([
            "{",
            "    if (err)",
            "    {",
            "        goto CLEANUP;",
            "INNER:",
            "    }",
            "CLEANUP:",
            "    return 0;",
            "}",
        ])
        self.assertEqual(expected_unindented, writer_unindented.write_str_elem(body))


class TestUnionAndNestedStructInitializers(unittest.TestCase):

    def test_union_declaration_and_reference(self):
        C = cfile.CFactory()
        u = C.union("data_u", members=[
            C.union_member("i", "int"),
            C.union_member("f", "float"),
        ])
        writer = cfile.Writer()
        expected_decl = "\n".join([
            "union data_u",
            "{",
            "    int i;",
            "    float f;",
            "};",
        ])
        self.assertEqual("union data_u;", writer.write_str_elem(C.statement(u)))
        self.assertEqual(expected_decl, writer.write_str_elem(C.statement(C.declaration(u))))
        var_stmt = C.statement(C.declaration(C.variable("val", u), {"i": 42}))
        self.assertEqual("union data_u val = {.i=42};", writer.write_str_elem(var_stmt))

    def test_anonymous_union_variable_declaration(self):
        C = cfile.CFactory()
        anon_union = C.union(members=[
            C.union_member("x", "int"),
            C.union_member("c", "char", array=4),
        ])
        u_var = C.variable("u", C.declaration(anon_union))
        stmt = C.statement(C.declaration(u_var, [1]))
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "union {",
            "    int x;",
            "    char c[4];",
            "} u = {1};",
        ])
        self.assertEqual(expected, writer.write_str_elem(stmt))

    def test_nested_struct_and_union_with_nested_and_designated_initializers(self):
        C = cfile.CFactory()
        addr_struct = C.struct("addr_t", members=[C.struct_member("port", "uint32_t")])
        in_union = C.union(members=[
            C.union_member("a8", "uint8_t", array=4),
            C.union_member("a16", "uint16_t", array=2),
        ])
        example = C.struct("example", members=[
            C.struct_member("addr", C.declaration(addr_struct)),
            C.struct_member("in_u", C.declaration(in_union)),
        ])
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected_struct = "\n".join([
            "struct example {",
            "    struct addr_t {",
            "        uint32_t port;",
            "    } addr;",
            "    union {",
            "        uint8_t a8[4];",
            "        uint16_t a16[2];",
            "    } in_u;",
            "};",
        ])
        self.assertEqual(expected_struct, writer.write_str_elem(C.statement(C.declaration(example))))

        ex_pos = C.statement(C.declaration(C.variable("ex", example), [[80], [[127, 0, 0, 1]]]))
        self.assertEqual("struct example ex = {{80}, {{127, 0, 0, 1}}};", writer.write_str_elem(ex_pos))

        ex_named = C.statement(
            C.declaration(
                C.variable("ex", example),
                {"addr": {"port": 80}, "in_u": {"a8": [127, 0, 0, 1]}},
            )
        )
        self.assertEqual(
            "struct example ex = {.addr={.port=80}, .in_u={.a8={127, 0, 0, 1}}};",
            writer.write_str_elem(ex_named),
        )


class TestEnum(unittest.TestCase):

    def test_enum_declaration_with_prefix_and_member_references(self):
        C = cfile.CFactory()
        color_enum = C.enum("color", prefix="COLOR_")
        red = color_enum.make_member("RED", 0)
        green = color_enum.make_member("GREEN")
        blue = color_enum.make_member("BLUE", 10)

        writer = cfile.Writer()
        expected = "\n".join([
            "enum color",
            "{",
            "    COLOR_RED = 0,",
            "    COLOR_GREEN,",
            "    COLOR_BLUE = 10",
            "};",
        ])
        self.assertEqual(expected, writer.write_str_elem(C.statement(C.declaration(color_enum))))
        self.assertEqual("COLOR_RED", str(red))
        self.assertEqual("case COLOR_GREEN:", writer.write_str_elem(C.switch_label(green)))
        var_stmt = C.statement(C.declaration(C.variable("c", color_enum), blue))
        self.assertEqual("enum color c = COLOR_BLUE;", writer.write_str_elem(var_stmt))

    def test_enum_from_dict_and_list_and_typedef(self):
        C = cfile.CFactory()
        state_enum = C.enum(
            "state_tag",
            members={"IDLE": 0, "ACTIVE": 1, "ERROR": 255},
            prefix="STATE_",
        )
        state_t = C.typedef("state_t", C.declaration(state_enum))
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "typedef enum state_tag {",
            "    STATE_IDLE = 0,",
            "    STATE_ACTIVE = 1,",
            "    STATE_ERROR = 255",
            "} state_t;",
        ])
        self.assertEqual(expected, writer.write_str_elem(C.statement(C.declaration(state_t))))

        anon_enum = C.enum(members=["FIRST", ("SECOND", 2), C.enum_member("THIRD")], prefix="E_")
        expected_anon = "\n".join([
            "enum {",
            "    E_FIRST,",
            "    E_SECOND = 2,",
            "    E_THIRD",
            "};",
        ])
        self.assertEqual(expected_anon, writer.write_str_elem(C.statement(C.declaration(anon_enum))))


class TestLoops(unittest.TestCase):

    def test_while_loop_allman_and_attach(self):
        C = cfile.CFactory()
        count = C.variable("count", "int")
        body = C.sequence([
            C.statement(C.fn_call("process", count)),
            C.statement(f"{count}--"),
        ])
        loop = C.while_statement(f"{count} > 0", body)

        allman_writer = cfile.Writer()
        expected_allman = "\n".join([
            "while (count > 0)",
            "{",
            "    process(count);",
            "    count--;",
            "}",
        ])
        self.assertEqual(expected_allman, allman_writer.write_str_elem(loop))

        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected_attach = "\n".join([
            "while (count > 0) {",
            "    process(count);",
            "    count--;",
            "}",
        ])
        self.assertEqual(expected_attach, attach_writer.write_str_elem(loop))

    def test_while_loop_single_statement_and_alias(self):
        C = cfile.CFactory()
        writer = cfile.Writer()
        loop = C.while_loop(True, C.statement(C.fn_call("poll")))
        self.assertEqual("while (true) poll();", writer.write_str_elem(loop))

    def test_do_while_allman_and_attach(self):
        C = cfile.CFactory()
        attempts = C.variable("attempts", "int")
        body = C.sequence([
            C.statement(f"{attempts}++"),
        ])
        loop = C.do_while_statement(body, f"{attempts} < 3")

        allman_writer = cfile.Writer()
        expected_allman = "\n".join([
            "do",
            "{",
            "    attempts++;",
            "}",
            "while (attempts < 3);",
        ])
        self.assertEqual(expected_allman, allman_writer.write_str_elem(loop))

        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected_attach = "\n".join([
            "do {",
            "    attempts++;",
            "} while (attempts < 3);",
        ])
        self.assertEqual(expected_attach, attach_writer.write_str_elem(loop))

        macro_loop = C.do_while(C.sequence(C.statement(C.fn_call("action"))), 0)
        expected_macro = "\n".join([
            "do {",
            "    action();",
            "} while (0);",
        ])
        self.assertEqual(expected_macro, attach_writer.write_str_elem(macro_loop))

    def test_for_statement_c99_declaration_and_variants(self):
        C = cfile.CFactory()
        i = C.variable("i", "int")
        n = C.variable("n", "int")
        body = C.sequence(C.statement(C.fn_call("work", i)))

        loop = C.for_statement(C.declaration(i, 0), f"{i} < {n}", f"{i}++", body)
        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        expected = "\n".join([
            "for (int i = 0; i < n; i++) {",
            "    work(i);",
            "}",
        ])
        self.assertEqual(expected, attach_writer.write_str_elem(loop))

        loop_from_stmt = C.for_loop(C.declaration_statement(i, 0), f"{i} < {n}", f"{i}++", body)
        self.assertEqual(expected, attach_writer.write_str_elem(loop_from_stmt))

        forever = C.for_statement(body=C.sequence(C.break_statement()))
        expected_forever = "\n".join([
            "for (;;) {",
            "    break;",
            "}",
        ])
        self.assertEqual(expected_forever, attach_writer.write_str_elem(forever))

        no_init = C.for_statement(condition=f"{i} < 10", update=f"{i}++", body=C.statement(C.fn_call("step", i)))
        self.assertEqual("for (; i < 10; i++) step(i);", attach_writer.write_str_elem(no_init))

    def test_multi_declaration_and_multi_statement_in_sequence_and_for_loop(self):
        C = cfile.CFactory()
        i = C.variable("i", "int")
        j = C.variable("j", "int")
        k = C.variable("k", "int", pointer=True)
        writer = cfile.Writer()

        decl_stmt = C.multi_declaration_statement((i, 0), (j, 0), (k, "NULL"))
        self.assertEqual("int i = 0, j = 0, *k = NULL;", writer.write_str_elem(decl_stmt))

        mixed_decl = C.multi_declaration_statement(i, C.declaration(j, 1), (k, "NULL"))
        self.assertEqual("int i, j = 1, *k = NULL;", writer.write_str_elem(mixed_decl))

        multi_stmt = C.multi_statement(C.assignment(i, 2), C.assignment(j, 3))
        self.assertEqual("i = 2, j = 3;", writer.write_str_elem(multi_stmt))

        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        for_with_multi_stmt = C.for_loop(
            C.multi_statement(C.assignment(i, 0), C.assignment(j, 0)),
            f"{i} < 10",
            C.multi_statement(f"{i}++", f"{j}--"),
            C.sequence(C.statement(C.fn_call("use", [i, j]))),
        )
        expected_for_stmt = "\n".join([
            "for (i = 0, j = 0; i < 10; i++, j--) {",
            "    use(i, j);",
            "}",
        ])
        self.assertEqual(expected_for_stmt, attach_writer.write_str_elem(for_with_multi_stmt))

        for_with_multi_decl = C.for_loop(
            C.multi_declaration((i, 0), (j, 0)),
            f"{i} < 10",
            f"{i}++",
            C.sequence(C.statement(C.fn_call("use", [i, j]))),
        )
        expected_for_decl = "\n".join([
            "for (int i = 0, j = 0; i < 10; i++) {",
            "    use(i, j);",
            "}",
        ])
        self.assertEqual(expected_for_decl, attach_writer.write_str_elem(for_with_multi_decl))

    def test_multi_declaration_incompatible_types_raises(self):
        C = cfile.CFactory()
        i = C.variable("i", "int")
        f = C.variable("f", "float")
        s = C.variable("s", "int", static=True)
        with self.assertRaises(ValueError):
            C.multi_declaration(i, f)
        with self.assertRaises(ValueError):
            C.multi_declaration(i, s)


if __name__ == '__main__':
    unittest.main()
