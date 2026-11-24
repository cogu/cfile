# Changelog

Notable changes.

## [Unreleased]

### Added

* `IfStatement` (`C.if_statement`)
* `SwitchStatement` (`C.switch` / `C.switch_statement`), `SwitchLabel` (`C.switch_label`), and `SwitchDefault` (`C.switch_default`)
* Flow-control statements and labels: `BreakStatement` (`C.break_statement`), `ContinueStatement` (`C.continue_statement`), `GotoStatement` (`C.goto_statement`), `ReturnStatement` (`C.return_statement`), and `NamedLabel` (`C.named_label`)
* Support passing a `Function` object directly to `FunctionCall` / `C.fn_call` with argument count validation
* Support `Element` initializers (such as `FunctionCall`) in variable `Declaration`
* `__str__` helper on `Variable`, `StructMember`, `Function`, `TypeDef`, and `NamedLabel` returning the identifier name
* Style options: `BraceWrapping.after_control_statement`, `StyleOptions.indent_case_labels`, `StyleOptions.indent_case_blocks`, and `StyleOptions.indent_goto_labels`

### Changed

* Rename `func_call` to `fn_call`, `func_return` to `fn_return`, and `sysinclude` to `sys_include` (keeping old names as aliases)
* Make `StyleOptions` optional when initializing `Writer` (defaults to `StyleOptions()`)
* Make `expression` optional in `FunctionReturn` / `C.fn_return` to support void `return`
* Allow `Sequence` and `Block` (`C.sequence` and `C.block`) to accept optional initial element(s)
* Trim trailing newline by default in `Writer.write_str`

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
