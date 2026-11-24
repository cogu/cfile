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
    code.append(C.sys_include("stdio.h"))
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
    code.append(C.declaration(main_fn))

    main_body = C.block([
        C.statement(C.fn_call("printf", C.str_literal(r"Hello World\n"))),
        C.return_statement(0),
    ])
    code.append(main_body)

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

- **Wrapped in** ``C.declaration(...)``: Emits the full C declaration (including types, qualifiers,
  struct members, or initializers).
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

    code.append(C.statement(C.declaration(var1)))      # int var1;
    code.append(C.statement(C.declaration(var2, 0)))   # int var2 = 0;
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

    code.append(C.statement(C.declaration(struct_type)))
    code.append(C.blank())
    code.append(C.statement(C.declaration(C.variable("instance", struct_type), [0, 0])))

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

Control Flow
------------

If / Else-If / Else Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``C.if_statement()`` with ``.else_if()`` and ``.else_branch()`` (or ``.append(condition, branch)``
when building branches in a loop). Passing a ``Sequence`` or ``Block`` wraps the branch in braces;
passing a single ``Statement`` emits a single-line unbraced branch:

.. code-block:: python

    import cfile

    C = cfile.CFactory()
    code = C.sequence()
    arg = C.variable("x", "int")
    code.append(C.declaration(C.function("classify", "int", params=[arg])))

    body = C.block([
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

    switch_body = C.block([
        C.switch_label(1),
        C.break_statement(),
        C.switch_label(2),
        C.break_statement(),
        C.switch_default(),
        C.goto_statement(cleanup),
    ])

    block = C.block([
        C.switch(switch_var, switch_body),
        C.continue_statement(),
        cleanup,
    ])

    writer = cfile.Writer()
    print(writer.write_str(C.sequence(block)))

Output:

.. code-block:: c

    {
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
    }
