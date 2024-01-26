# Changelog

Notable changes.

## Unreleased

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
