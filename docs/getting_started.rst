Generating C Code Programmatically
==================================

**cfile** separates **code structure** from **code formatting**:

1. Use :class:`cfile.factory.CFactory` to build a sequence of C code elements.
2. Use :class:`cfile.writer.Writer` (optionally configured with :class:`cfile.style.StyleOptions`)
   to render the sequence to a string or file.

Hello World
-----------

The following example creates a ``main`` function that prints ``Hello World\n`` and returns ``0``:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()
    code.append(C.include_directive("stdio.h", sys=True))
    code.append(C.blank())

    char_ptr_type = C.type("char", pointer=True)
    main_fn = C.function(
        "main",
        "int",
        params=[
            C.variable("argc", "int"),
            C.variable("argv", char_ptr_type, pointer=True),
        ],
    )
    main_body = C.sequence([
        C.statement(C.fn_call("printf", C.str_literal(r"Hello World\n"))),
        C.return_statement(0),
    ])
    code.append(C.declaration(main_fn, main_body))

    writer = cfile.Writer()
    print(writer.write_str(code))

Output (default Allman style):

.. code-block:: c

    #include <stdio.h>

    int main(int argc, char** argv)
    {
        printf("Hello World\n");
        return 0;
    }

Changing the Formatting Style
-----------------------------

Pass a :class:`~cfile.style.StyleOptions` instance to :class:`~cfile.writer.Writer` to change brace
placement, pointer alignment, indentation, or case label formatting without modifying the code tree:

.. code-block:: python

    style = cfile.StyleOptions(
        break_before_braces=cfile.BreakBeforeBraces.ATTACH,
        pointer_alignment=cfile.Alignment.RIGHT,
    )
    writer = cfile.Writer(style)
    print(writer.write_str(code))

Output:

.. code-block:: c

    #include <stdio.h>

    int main(int argc, char **argv) {
        printf("Hello World\n");
        return 0;
    }

Declarations vs. References
---------------------------

In **cfile**, objects returned by ``C.variable()``, ``C.function()``, ``C.struct()``, and ``C.typedef()``
represent the underlying C entity:

- **Wrapped in** ``C.declaration(...)`` (or ``C.declaration_statement(...)``): Emits the full C declaration
  (including types, qualifiers, struct members, or initializers).
- **Used directly** (or interpolated in an f-string): Emits a reference to the entity's name
  (or a forward declaration in the case of a struct statement).

Variables and Assignments
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()
    var1 = C.variable("var1", "int")
    var2 = C.variable("var2", "int")

    code.append(C.declaration_statement(var1))         # int var1;
    code.append(C.declaration_statement(var2, 0))      # int var2 = 0;
    code.append(C.statement(C.assignment(var1, var2))) # var1 = var2;

    writer = cfile.Writer()
    print(writer.write_str(code))

Structs, Typedefs, and Initializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()

    struct = C.struct(
        "mystruct",
        members=[
            C.struct_member("field_1", "int"),
            C.struct_member("field_2", "int"),
        ],
    )
    struct_type = C.typedef("my_struct_t", C.declaration(struct))

    code.append(C.declaration_statement(struct_type))
    code.append(C.blank())
    code.append(C.declaration_statement(C.variable("instance", struct_type), [0, 0]))

    style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
    writer = cfile.Writer(style)
    print(writer.write_str(code))

Output:

.. code-block:: c

    typedef struct mystruct {
        int field_1;
        int field_2;
    } my_struct_t;

    my_struct_t instance = {0, 0};

Unions, Nested Declarations, and Designated Initializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can declare ``union`` types with ``C.union()`` and ``C.union_member()``, nest inline ``struct`` or
``union`` declarations inside an outer struct using ``C.declaration(...)``, and initialize variables
using nested Python lists (positional initializers) or dictionaries (C99 designated initializers):

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()
    code.append(C.include_directive("stdint.h", sys=True))
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
    code.append(
        C.statement(
            C.declaration(
                ex2,
                {"addr": {"port": port}, "in_u": {"a8": ip_address.split(".")}},
            )
        )
    )

    style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
    writer = cfile.Writer(style)
    print(writer.write_str(code))

Output:

.. code-block:: c

    #include <stdint.h>

    struct example {
        struct addr_t {
            uint32_t port;
        } addr;
        union {
            uint8_t a8[4];
            uint16_t a16[2];
        } in_u;
    };

    struct example ex1 = {{80}, {{127, 0, 0, 1}}};
    struct example ex2 = {.addr={.port=80}, .in_u={.a8={127, 0, 0, 1}}};

Enumerations with Automatic Member Prefixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``C.enum()`` and ``make_member()`` (or pass a ``list`` / ``dict`` of members) to define C enumerations.
Setting ``prefix`` on the enum automatically prepends the prefix to every enumerator both in the ``enum``
declaration and wherever an :class:`~cfile.core.EnumMember` object is referenced:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()

    color_enum = C.enum("color_tag", prefix="COLOR_")
    red = color_enum.make_member("RED", 0)
    green = color_enum.make_member("GREEN")
    blue = color_enum.make_member("BLUE")

    color_type = C.typedef("color_t", C.declaration(color_enum))
    code.append(C.statement(C.declaration(color_type)))
    code.append(C.blank())

    selected = C.variable("selected", color_type)
    code.append(C.statement(C.declaration(selected, green)))

    style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
    writer = cfile.Writer(style)
    print(writer.write_str(code))

Output:

.. code-block:: c

    typedef enum color_tag {
        COLOR_RED = 0,
        COLOR_GREEN,
        COLOR_BLUE
    } color_t;

    color_t selected = COLOR_GREEN;

Control Flow
------------

If / Else-If / Else Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``C.if_statement()`` with ``.else_if()`` and ``.else_branch()`` (or ``.append(condition, branch)``
when building branches in a loop). Passing a ``Sequence`` wraps the branch in braces;
passing a single ``Statement`` emits a single-line unbraced branch:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()
    arg = C.variable("x", "int")
    code.append(C.declaration(C.function("classify", "int", params=[arg])))

    body = C.sequence([
        C.if_statement(f"{arg} > 0", C.sequence(C.return_statement(1)))
        .else_if(f"{arg} < 0", C.sequence(C.return_statement(-1)))
        .else_branch(C.sequence(C.return_statement(0)))
    ])
    code.append(body)

    style = cfile.StyleOptions(break_before_braces=cfile.BreakBeforeBraces.ATTACH)
    writer = cfile.Writer(style)
    print(writer.write_str(code))

Output:

.. code-block:: c

    int classify(int x) {
        if (x > 0) {
            return 1;
        } else if (x < 0) {
            return -1;
        } else {
            return 0;
        }
    }

Switch Statements and Jump Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``C.switch()``, ``C.switch_label()``, ``C.switch_default()``, ``C.break_statement()``,
``C.continue_statement()``, ``C.goto_statement()``, and ``C.named_label()``:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    cleanup = C.named_label("CLEANUP")
    switch_var = C.variable("value", "int")

    switch_body = C.sequence([
        C.switch_label(1),
        C.break_statement(),
        C.switch_label(2),
        C.break_statement(),
        C.switch_default(),
        C.goto_statement(cleanup),
    ])

    code = C.sequence([
        C.switch(switch_var, switch_body),
        C.continue_statement(),
        cleanup,
    ])

    writer = cfile.Writer()
    print(writer.write_str(code))

Output:

.. code-block:: c

    switch (value)
    {
    case 1:
        break;
    case 2:
        break;
    default:
        goto CLEANUP;
    }
    continue;
    CLEANUP:

Loops (``for``, ``while``, ``do ... while``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``C.for_statement()`` (or ``C.for_loop()``), ``C.while_statement()`` (or ``C.while_loop()``),
and ``C.do_while_statement()`` (or ``C.do_while()``). To declare multiple variables of the same
type or chain multiple expressions with commas in ``for`` headers (or standalone statements), use
``C.multi_declaration()``, ``C.multi_declaration_statement()``, and ``C.multi_statement()``:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()

    n = C.variable("n", "int")
    sum_var = C.variable("sum", "int")
    i = C.variable("i", "int")
    j = C.variable("j", "int")

    compute_fn = C.function("compute_sum", "int", params=[n])
    body = C.sequence([
        C.declaration_statement(sum_var, 0),
        C.for_statement(
            C.multi_declaration((i, 0), (j, 0)),
            f"{i} < {n}",
            C.multi_statement(f"{i}++", f"{j}+=2"),
            C.sequence(C.statement(f"{sum_var} += {i} + {j}")),
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

Output:

.. code-block:: c

    int compute_sum(int n) {
        int sum = 0;
        for (int i = 0, j = 0; i < n; i++, j+=2) {
            sum += i + j;
        }
        while (sum > 100) {
            sum -= 10;
        }
        do {
            sum++;
        } while (sum < 10);
        return sum;
    }
