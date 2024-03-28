# Changelog

Notable changes.

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
