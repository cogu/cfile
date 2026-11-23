#!/usr/bin/env bash
exec python3 "$(dirname -- "$0")/dev_utils/validate_examples.py" "$@"
