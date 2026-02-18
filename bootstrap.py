"""Bootstrap script to rename the template package."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

# Files that contain 'mypackage' or 'MyPackage' references to replace
FILES_TO_UPDATE = [
    "pyproject.toml",
    "README.md",
    "docs/conf.py",
    "docs/contributing.md",
    ".github/workflows/test.yml",
    ".github/workflows/slow-tests.yml",
    ".github/workflows/publish.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".readthedocs.yaml",
]


def to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def validate_name(name: str) -> None:
    """Validate package name is a valid Python identifier."""
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print(f"Error: '{name}' is not a valid Python package name.")
        print("Must start with a lowercase letter and contain only [a-z0-9_].")
        sys.exit(1)


def replace_in_file(path: Path, replacements: list[tuple[str, str]]) -> bool:
    """Replace strings in a file. Returns True if any changes were made."""
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    """Run the bootstrap process."""
    if len(sys.argv) != 2:
        print("Usage: python bootstrap.py <package_name>")
        print("Example: python bootstrap.py myproject")
        sys.exit(1)

    name = sys.argv[1]
    validate_name(name)
    pascal_name = to_pascal_case(name)
    root = Path(__file__).parent

    replacements = [
        ("mypackage", name),
        ("MyPackage", pascal_name),
    ]

    print(f"Bootstrapping template as '{name}' ({pascal_name})...\n")

    # Rename source directory
    src_old = root / "src" / "mypackage"
    src_new = root / "src" / name
    if src_old.exists():
        shutil.move(str(src_old), str(src_new))
        print(f"  Renamed src/mypackage -> src/{name}")
    elif not src_new.exists():
        print(f"  Warning: src/mypackage not found and src/{name} does not exist")

    # Update file contents
    updated = []
    for rel_path in FILES_TO_UPDATE:
        path = root / rel_path
        if path.exists() and replace_in_file(path, replacements):
            updated.append(rel_path)

    if updated:
        print(f"\n  Updated references in {len(updated)} files:")
        for f in updated:
            print(f"    - {f}")

    print(f"\nBootstrap complete! Package is now '{name}'.")
    print("\nNext steps:")
    print("  1. pip install hatch && hatch env create")
    print("  2. hatch run test")
    print("  3. Update pyproject.toml metadata (description, URLs, etc.)")

    # Self-delete (may fail on Windows if interpreter holds a handle)
    bootstrap_path = Path(__file__)
    try:
        bootstrap_path.unlink()
        print(f"\n  Self-deleted {bootstrap_path.name}")
    except PermissionError:
        print(f"\n  Could not self-delete {bootstrap_path.name} (Windows file lock).")
        print(f"  Please delete it manually: del {bootstrap_path.name}")


if __name__ == "__main__":
    main()
