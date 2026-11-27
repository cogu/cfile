# Backlog

Planned features and enhancements for upcoming `v0.5.x` releases, listed roughly in priority order.

## 1. Flexible, Symbolic & Multi-Dimensional Arrays

Extend the `array` parameter on `Variable`, `StructMember`, `UnionMember`, `Type`, and `TypeDef` beyond `int | None`:

* **Unsized arrays**: `const uint8_t data[] = {1, 2, 3};` and struct flexible array members (`uint8_t payload[];`)
* **Symbolic / macro sizes**: `char name[MAX_NAME_LEN];`
* **Multi-dimensional arrays**: `int matrix[3][4];`

## 2. Function Pointers

First-class support for C function pointer types, variables, parameters, struct/union members, and typedefs:

* Variable / member: `int (*callback)(int a, int b);`
* Typedef: `typedef void (*handler_t)(void *ctx);`

## 3. `inline` & Variadic Functions

* Add `inline: bool = False` to `Function` / `C.function(...)` for C99+ header functions (e.g., `static inline int clamp(int x)`).
* Add `variadic: bool = False` (or ellipsis parameter support) for variadic functions (e.g., `int log_msg(const char *fmt, ...);`).

## 4. Struct & Union Bit-Fields

Add optional `bit_width` support to `StructMember` and `UnionMember` for embedded and protocol structures:

```c
struct flags {
    uint32_t enabled : 1;
    uint32_t priority : 3;
};
```

## 5. Multi-Line Formatted Initializers

Add formatting support for wrapping and indenting large array and struct initializers (such as generated `const` lookup tables or arrays of structs) across multiple lines instead of emitting everything on a single line.

## 6. Trailing Comments on Struct, Union & Enum Members

Allow attaching optional `Comment` objects to `StructMember`, `UnionMember`, and `EnumMember` so aligned inline comments work inside struct, union, and enum declarations:

```c
typedef enum color_tag {
    COLOR_RED = 0,  // Red color
    COLOR_GREEN,    // Green color
    COLOR_BLUE      // Blue color
} color_t;
```

## 7. Additional Type Qualifiers, Storage Classes & Attributes

* C99 `restrict` pointer qualifier (`void * restrict dst`)
* Additional storage classes / qualifiers (`register`, `_Thread_local` / `thread_local`, `_Atomic`)
* Optional compiler / standard attributes (`__attribute__((packed))`, C23 `[[nodiscard]]`, etc.)

## 8. C11 / C23 Compile-Time Assertions

Convenience support for `_Static_assert(expr, "message");` / `static_assert(expr, "message");`.
