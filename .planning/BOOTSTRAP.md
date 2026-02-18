## Bootstrap Scaffolding

These are the remaining scaffolding steps after the user has run `bootstrap.py` and `/gsd:new-project`. Perform them as part of the first phase of work. Delete this file after completing all steps.

### 1. Create the source package structure

Expand `src/<package>/` with subpackages as the project's architecture requires.

Every `__init__.py` must have: a module docstring, explicit imports of public symbols, and an `__all__` list. Every `.py` file starts with a one-line docstring.

Common subpackages:

| Directory | Purpose |
|-----------|---------|
| `core/` | Core domain logic |
| `config/` | Configuration, shared types, dataclasses |
| `io/` | File I/O, serialization, loaders |
| `utils/` | General-purpose helpers |

### 2. Create the test directories

```
tests/
├── unit/           # One test file per source module
├── synthetic/      # Integration tests with known ground truth
└── integration/    # End-to-end tests
```

Create whichever test directories the project actually needs. Write at least one passing test.

### 3. Create CLAUDE.md

The top-level `CLAUDE.md` is the primary agent instruction file. It should contain:

- **Project**: What the project does (1-2 sentences)
- **Environment**: Shell (Git Bash MINGW64), path format (`/c/Users/...`), project root, working directory
- **Architecture**: High-level overview of the codebase structure
- **Domain conventions**: Coordinate systems, units, key parameters (if applicable)
- **Testing**: How to run tests (all, fast-only, single file)
- **Common commands**: Copy-pasteable CLI examples

### 4. Create docs scaffolding

Create `docs/index.md` -- landing page with sphinx-design grid cards linking to API reference, contributing guide, and any other sections. Include a toctree. Follow the MyST markdown + Furo grid-card pattern.

Create `docs/api/index.rst` -- autodoc toctree, add one `.rst` file per source subpackage.

Create `docs/Makefile` and `docs/make.bat` (standard Sphinx quickstart output).

### 5. Create CODE_OF_CONDUCT.md

Standard [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). Update the enforcement contact URL to point to the project's GitHub issues.

### 6. Update pyproject.toml metadata

- `description`, `keywords`, `classifiers`
- `dependencies` (actual project deps)
- `[project.urls]` (all URLs)
- Uncomment `[project.scripts]` if the project has a CLI

### 7. Initialize tooling

```bash
detect-secrets scan > .secrets.baseline
```

### 8. Write the README

Fill in the project README with: description, installation, quick start, link to docs.

### 9. Verify

```bash
hatch run test                        # tests pass
hatch run lint                        # lint passes
hatch run typecheck                   # type check passes
hatch run pre-commit run --all-files  # hooks pass
```
