# Changelog

Notable changes.

## [Unreleased]

## [v0.5.0] - 2026-11-27

### Added

* `IfStatement` (`C.if_statement`)
* `SwitchStatement` (`C.switch` / `C.switch_statement`), `SwitchLabel` (`C.switch_label`), and `SwitchDefault` (`C.switch_default`)
* Loop statements:
  * `WhileStatement` (`C.while_statement` / `C.while_loop`)
  * `DoWhileStatement` (`C.do_while_statement` / `C.do_while`)
  * `ForStatement` (`C.for_statement` / `C.for_loop`)
* Flow-control statements and labels:
  * `BreakStatement` (`C.break_statement`)
  * `ContinueStatement` (`C.continue_statement`)
  * `GotoStatement` (`C.goto_statement`)
  * `ReturnStatement` (`C.return_statement`)
  * `NamedLabel` (`C.named_label`)
* `Union` (`C.union`) and `UnionMember` (`C.union_member`), anonymous structs and unions (`name=None`), and inline nested struct/union declarations
* `Enum` (`C.enum`) and `EnumMember` (`C.enum_member`) with automatic member `prefix` support
* Support nested list initializers and named/designated `dict` initializers (`{"x": 1, "y": 2}` -> `{.x=1, .y=2}`) for structs and unions
* Preprocessor directives and generic `C.directive(text)`:
  * `IncludeNextDirective` (`C.include_next_directive`) and `EmbedDirective` (`C.embed_directive`)
  * `UndefDirective` (`C.undef_directive`)
  * `IfDirective` (`C.if_directive`), `ElifDirective` (`C.elif_directive`), `ElifdefDirective` (`C.elifdef_directive`), `ElifndefDirective` (`C.elifndef_directive`), and `ElseDirective` (`C.else_directive`)
  * `LineDirective` (`C.line_directive`), `ErrorDirective` (`C.error_directive`), `WarningDirective` (`C.warning_directive`), and `PragmaDirective` (`C.pragma_directive`)
* Automatic preprocessor directive indentation options in `StyleOptions` (`indent_pp_directives: PPDirectiveIndent` and `pp_indent_width`) with top-level include-guard detection
* Support passing a `Function` object directly to `FunctionCall` / `C.fn_call` with argument count validation
* Support passing a function body (`Sequence`) directly as the second argument (`content`) of `Declaration` / `C.declaration`
* Convenience factory method `C.declaration_statement(element, content=None)` as shorthand for `C.statement(C.declaration(element, content))`
* Multi-variable declarations and comma-chained statements:
  * `MultiDeclaration` (`C.multi_declaration(*items)` and `C.multi_declaration_statement(*items)`)
  * `C.multi_statement(*expressions)` for comma-separated expressions in standalone statements and `for`-loop headers
* Support `Element` initializers (such as `FunctionCall`) in variable `Declaration`
* `__str__` helper on `Variable`, `StructMember`, `Function`, `TypeDef`, `NamedLabel`, and `EnumMember` returning the identifier name
* Package version attribute `cfile.__version__`
* Style options:
  * `BraceWrapping.after_control_statement`
  * `StyleOptions.indent_case_labels`
  * `StyleOptions.indent_case_blocks`
  * `StyleOptions.indent_goto_labels`

### Changed

* Retire `core.Block` and `C.block()` in favor of `core.Sequence` and `C.sequence()` (brace wrapping is determined automatically from context)
* Replace `adjust` on `Comment`, `LineComment` (`C.line_comment`), and `BlockComment` (`C.block_comment`) with `padding: int = 1`, `margin: int = 1`, and `absolute: bool = False`, plus multi-line alignment support
* Rename `func_call` to `fn_call` and `func_return` to `fn_return` (keeping old names as aliases)
* Refactor preprocessor directive factory methods and indentation:
  * Rename existing directive factory methods to `*_directive` (`include_directive`, `define_directive`, `ifdef_directive`, `ifndef_directive`, `endif_directive`)
  * Replace `sys_include` with `include_directive(path_to_file, sys=True)`
  * Remove manual `adjust` parameter in favor of `StyleOptions.indent_pp_directives`
* Make `StyleOptions` optional when initializing `Writer` (defaults to `StyleOptions()`)
* Make `expression` optional in `FunctionReturn` / `C.fn_return` to support void `return`
* Allow `Sequence` (`C.sequence`) to accept optional initial element(s)
* Trim trailing newline by default in `Writer.write_str`
* Emit `str` values in `Declaration` initializers as unquoted C expressions (use `C.str_literal` for quoted strings)

## [v0.4.0] - 2024-03-28

### Changed

* Improved readability of example code

## [v0.3.2]

**Until v0.3.1:** Variables, functions and types were implicitly declared.

**From v0.3.2:** Variables, functions and types needs explicit declaration.

Due to a major design flaw in previous versions, breaking compatibility was necessary.

### Removed

* StuctRef (struct references).

### Added

* Declaration element
* Constructor for `Function` takes an optional params argument.

### Changed

* Variables, functions, structs are no longer implicitly declared.
  * Use explicit element `Declaration` for all declarations.
* Method `FunctionCall.add_arg` renamed to `FunctionCall.append`.

## [v0.3.1]

### Added

* Support struct declaratios and struct references

## [v0.3.0]

* New code base
  * New core and factory modules
  * New writer module with formatting options
  * Annotate code with modern type hints
* Added unit tests
* Enabled linting with Pylint and flake8
