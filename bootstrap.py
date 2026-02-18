"""Bootstrap script to rename the template package."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Files containing template placeholders to replace.
# Paths are relative to project root. The source directory is handled
# separately (renamed before file contents are updated).
FILES_TO_UPDATE = [
    "pyproject.toml",
    "README.md",
    "docs/conf.py",
    "docs/contributing.md",
    "tests/unit/test_smoke.py",
    "LICENSE",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
]


def to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def validate_package_name(name: str) -> None:
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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Bootstrap the project template with your package name and metadata.",
    )
    parser.add_argument(
        "package_name",
        help="Python package name (lowercase, underscores allowed). Example: my_project",
    )
    parser.add_argument(
        "--author",
        required=True,
        help="Author name for pyproject.toml, LICENSE, and docs. Example: 'Jane Doe'",
    )
    parser.add_argument(
        "--github-user",
        required=True,
        help="GitHub username for repository URLs. Example: janedoe",
    )
    return parser.parse_args()


def main() -> None:
    """Run the bootstrap process."""
    args = parse_args()

    validate_package_name(args.package_name)
    name = args.package_name
    pascal_name = to_pascal_case(name)
    root = Path(__file__).parent

    replacements = [
        ("mypackage", name),
        ("MyPackage", pascal_name),
        ("Tucker Lancaster", args.author),
        ("tlancaster6", args.github_user),
    ]

    print(f"Bootstrapping template as '{name}' ({pascal_name})...")
    print(f"  Author: {args.author}")
    print(f"  GitHub: {args.github_user}\n")

    # Rename source directory
    src_old = root / "src" / "mypackage"
    src_new = root / "src" / name
    if src_old.exists():
        shutil.move(str(src_old), str(src_new))
        print(f"  Renamed src/mypackage -> src/{name}")
    elif not src_new.exists():
        print(f"  Warning: src/mypackage not found and src/{name} does not exist")

    # Replace template README with project README
    readme_template = root / "README_TEMPLATE.md"
    readme = root / "README.md"
    if readme_template.exists():
        shutil.move(str(readme_template), str(readme))
        print("  Replaced README.md with README_TEMPLATE.md")

    # Update file contents (including the renamed __init__.py)
    init_py = f"src/{name}/__init__.py"
    all_files = [*FILES_TO_UPDATE, init_py]

    updated = []
    for rel_path in all_files:
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
    print("  3. Open in Claude Code and run /gsd:new-project")

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
