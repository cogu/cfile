# Changelog

Notable changes.

## [Unreleased]

### Added

* `IfStatement` (`C.if_statement`)
* `SwitchStatement` (`C.switch` / `C.switch_statement`), `SwitchLabel` (`C.switch_label`), and `SwitchDefault` (`C.switch_default`)
* Flow-control statements and labels:
  * `BreakStatement` (`C.break_statement`)
  * `ContinueStatement` (`C.continue_statement`)
  * `GotoStatement` (`C.goto_statement`)
  * `ReturnStatement` (`C.return_statement`)
  * `NamedLabel` (`C.named_label`)
* `Union` (`C.union`) and `UnionMember` (`C.union_member`), anonymous structs and unions (`name=None`), and inline nested struct/union declarations
* `Enum` (`C.enum`) and `EnumMember` (`C.enum_member`) with automatic member `prefix` support
* Support nested list initializers and named/designated `dict` initializers (`{"x": 1, "y": 2}` -> `{.x=1, .y=2}`) for structs and unions
* C99 preprocessor directives and generic `C.directive(text)`:
  * `UndefDirective` (`C.undef_directive`)
  * `IfDirective` (`C.if_directive`), `ElifDirective` (`C.elif_directive`), and `ElseDirective` (`C.else_directive`)
  * `LineDirective` (`C.line_directive`), `ErrorDirective` (`C.error_directive`), and `PragmaDirective` (`C.pragma_directive`)
* Automatic preprocessor directive indentation options in `StyleOptions` (`indent_pp_directives: PPDirectiveIndent` and `pp_indent_width`) with top-level include-guard detection
* Support passing a `Function` object directly to `FunctionCall` / `C.fn_call` with argument count validation
* Support passing a function body (`Block` or `Sequence`) directly as the second argument (`content`) of `Declaration` / `C.declaration`
* Support `Element` initializers (such as `FunctionCall`) in variable `Declaration`
* `__str__` helper on `Variable`, `StructMember`, `Function`, `TypeDef`, `NamedLabel`, and `EnumMember` returning the identifier name
* Style options:
  * `BraceWrapping.after_control_statement`
  * `StyleOptions.indent_case_labels`
  * `StyleOptions.indent_case_blocks`
  * `StyleOptions.indent_goto_labels`

### Changed

* Rename `func_call` to `fn_call` and `func_return` to `fn_return` (keeping old names as aliases)
* Refactor preprocessor directive factory methods and indentation:
  * Rename existing directive factory methods to `*_directive` (`include_directive`, `define_directive`, `ifdef_directive`, `ifndef_directive`, `endif_directive`)
  * Replace `sys_include` with `include_directive(path_to_file, sys=True)`
  * Remove manual `adjust` parameter in favor of `StyleOptions.indent_pp_directives`
* Make `StyleOptions` optional when initializing `Writer` (defaults to `StyleOptions()`)
* Make `expression` optional in `FunctionReturn` / `C.fn_return` to support void `return`
* Allow `Sequence` and `Block` (`C.sequence` and `C.block`) to accept optional initial element(s)
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
