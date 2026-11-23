#!/usr/bin/env bash
mypy --strict src
mypy --check-untyped-defs src tests examples dev_utils
