"""Run all example scripts and compare their output with checked-in C snapshots."""

import argparse
from difflib import unified_diff
import os
from pathlib import Path
import subprocess
import sys


def run_example(script_path: Path, src_dir: Path) -> str | None:
    """Execute a single example script and return normalized stdout, or None on error."""
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{src_dir}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else str(src_dir)
    )

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(script_path.parent),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    if result.returncode != 0:
        print(f"Execution failed ({result.returncode}): {script_path}", file=sys.stderr)
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        return None

    return result.stdout.replace("\r\n", "\n")


def run_and_validate(script_path: Path, expected_path: Path, src_dir: Path) -> bool:
    """Execute a single example script and compare its stdout against expected_path."""
    actual = run_example(script_path, src_dir)
    if actual is None:
        return False

    expected = expected_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    if actual != expected:
        print(f"Output differs: {script_path.name} vs {expected_path.name}")
        diff = unified_diff(
            expected.split("\n"),
            actual.split("\n"),
            fromfile=str(expected_path),
            tofile=f"{script_path} (stdout)",
            lineterm="",
        )
        for line in diff:
            print(line)
        return False

    return True


def main() -> int:
    """Validate (or update) all example scripts in examples/ against examples/expected/*.c."""
    parser = argparse.ArgumentParser(description="Validate example scripts against expected C snapshots.")
    parser.add_argument(
        "--update",
        action="store_true",
        help="Run all example scripts and overwrite examples/expected/*.c snapshots.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    examples_dir = repo_root / "examples"
    expected_dir = examples_dir / "expected"
    src_dir = repo_root / "src"

    example_scripts = {
        path.stem: path
        for path in examples_dir.glob("*.py")
        if not path.name.startswith("__")
    }

    if args.update:
        expected_dir.mkdir(parents=True, exist_ok=True)
        updated = 0
        for stem, script_path in sorted(example_scripts.items()):
            output = run_example(script_path, src_dir)
            if output is None:
                return 1
            (expected_dir / f"{stem}.c").write_text(output, encoding="utf-8", newline="\n")
            updated += 1
        print(f"Updated {updated} example snapshots.")
        return 0

    expected_files = {
        path.stem: path
        for path in expected_dir.glob("*.c")
    }

    matches = True

    for stem in sorted(example_scripts.keys() - expected_files.keys()):
        print(f"Missing expected snapshot: {expected_dir / f'{stem}.c'}")
        matches = False

    for stem in sorted(expected_files.keys() - example_scripts.keys()):
        print(f"Unexpected snapshot without example script: {expected_files[stem]}")
        matches = False

    matched_count = 0
    for stem in sorted(example_scripts.keys() & expected_files.keys()):
        if run_and_validate(example_scripts[stem], expected_files[stem], src_dir):
            matched_count += 1
        else:
            matches = False

    if matches:
        print(f"All {matched_count} example outputs match expected snapshots.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
