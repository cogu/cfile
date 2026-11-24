# Test and verification

Use the virtual environment in .venv for running unit test and flake8 check.

Running unit tests:

```bash
python -m unittest discover -v tests "test_*.py"
```

Checking changes with flake:

```bash
flake8 --max-line-length=120 --extend-ignore=D107,D200,D205,D400,D401 src
flake8 --max-line-length=120 --extend-ignore=D101,D102,D107,D200,D205,D400,D401,E402 tests
flake8 --max-line-length=120 --extend-ignore=D107,D200,D205,D400,D401 examples
flake8 --max-line-length=120 --extend-ignore=D107,D200,D205,D400,D401 dev_utils
```

Running pylint:

```bash
pylint src
```

Running mypy:

```bash
mypy --strict src
mypy --check-untyped-defs src tests examples dev_utils
```

Validating examples:

```bash
./validate_examples.sh
```

# Changelog

Keep the `[Unreleased]` section in `CHANGELOG.md` updated whenever user-facing features, API changes, or bug fixes are implemented.
