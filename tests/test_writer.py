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
        writer = cfile.Writer(cfile.StyleOptions())
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

    def test_normal_include(self):
        element = core.IncludeDirective("path/to/file.h")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#include "path/to/file.h"')

    def test_system_include(self):
        element = core.IncludeDirective("stdio.h", system=True)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#include <stdio.h>')

    def test_define_with_left_part_only(self):
        element = core.DefineDirective("INCLUDE_GUARD")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#define INCLUDE_GUARD')

    def test_define_with_left_and_right(self):
        element = core.DefineDirective("MAX(a,b)", "int_max(a,b)")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#define MAX(a,b) int_max(a,b)')

    def test_define_with_left_part__adjusted(self):
        element = core.DefineDirective("IDENTIFIER", adjust=4)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#    define IDENTIFIER')

    def test_ifdef(self):
        element = core.IfdefDirective("IDENTIFIER")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#ifdef IDENTIFIER')

    def test_ifdef__adjusted(self):
        element = core.IfdefDirective("IDENTIFIER", adjust=2)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#  ifdef IDENTIFIER')

    def test_ifndef(self):
        element = core.IfndefDirective("IDENTIFIER")
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#ifndef IDENTIFIER')

    def test_ifndef__adjusted(self):
        element = core.IfndefDirective("IDENTIFIER", adjust=2)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#  ifndef IDENTIFIER')

    def test_endif(self):
        element = core.EndifDirective()
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#endif')

    def test_endif__adjusted(self):
        element = core.EndifDirective(adjust=4)
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, '#    endif')


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


class TestVariableDeclaration(unittest.TestCase):

    def test_declare_int_variable_from_string_type_name(self):
        element = core.Declaration(core.Variable("value", "int"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, "int value")

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

    def test_const_str_var_with_str_initializer(self):
        char_type = core.Type("char", const=True, pointer=True)
        element = core.Statement(core.Declaration(core.Variable("s", char_type), "Static Text"))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str_elem(element)
        self.assertEqual(output, 'const char* s = "Static Text";')


class TestSequence(unittest.TestCase):

    def test_variable_declarations(self):
        seq = core.Sequence()
        seq.append(core.Statement(core.Declaration(core.Variable("a", "int", static=True))))
        seq.append(core.Statement(core.Declaration(core.Variable("b", core.Type("void", pointer=True), static=True))))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "static int a;\n" + "static void* b;\n"
        self.assertEqual(expected, output)

    def test_variable_declaration_and_comment_using_line_element(self):
        seq = core.Sequence()
        seq.append(core.Line([core.Statement(core.Declaration(core.Variable("a", "int"))),
                              core.BlockComment(" Comment ")]))
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "int a; /* Comment */\n"
        self.assertEqual(expected, output)

    def test_variable_declaration_and_comment_using_python_list(self):
        seq = core.Sequence()
        seq.append([core.Statement(core.Declaration(core.Variable("a", "int"))), core.BlockComment(" Comment ")])
        writer = cfile.Writer(cfile.StyleOptions())
        output = writer.write_str(seq)
        expected = "int a; /* Comment */\n"
        self.assertEqual(expected, output)


class TestBlock(unittest.TestCase):

    def test_wrap_brace_after_function(self):
        seq = core.Sequence()
        seq.append(core.Declaration(core.Function("f")))
        seq.append(core.Block())
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        output = writer.write_str(seq)
        expected = "\n".join(["void f(void)", "{", "}", ""])
        self.assertEqual(expected, output)

    def test_attach_brace_to_function(self):
        seq = core.Sequence()
        seq.append(core.Declaration(core.Function("f")))
        seq.append(core.Block())
        writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        output = writer.write_str(seq)
        expected = "\n".join(["void f(void) {", "}", ""])
        self.assertEqual(expected, output)

    def test_variable_declarations(self):
        block = core.Block()
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
        body = core.Block()
        body.append(core.Statement("return a + b"))
        seq.append(body)
        allman_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ALLMAN))
        output = allman_writer.write_str(seq)
        expected = "\n".join(["int add(int a, int b)", "{", "    return a + b;", "}", ""])
        self.assertEqual(expected, output)
        attach_writer = cfile.Writer(cfile.StyleOptions(break_before_braces=style.BreakBeforeBraces.ATTACH))
        output = attach_writer.write_str(seq)
        expected = "\n".join(["int add(int a, int b) {", "    return a + b;", "}", ""])
        self.assertEqual(expected, output)

    def test_struct_declaration_inside_block(self):
        outer = core.Sequence()
        inner = core.Block()
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
}
"""
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
#endif // __clpusplus
"""
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
        print(">>> " + output)
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


if __name__ == '__main__':
    unittest.main()
