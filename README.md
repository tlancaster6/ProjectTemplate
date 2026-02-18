# Project Template

A Python project template that encodes standard workflow, tooling, and aesthetic decisions. Designed to be cloned and customized—either manually or by an AI agent (Claude Code)—to bootstrap a new, functional project.

## How to Use This Template

1. Clone or copy this template into a new project directory
2. Run the bootstrap script to rename the package:
   ```bash
   python bootstrap.py <package_name>
   ```
3. Set up your environment:
   ```bash
   pip install hatch
   hatch env create
   hatch run pre-commit install
   hatch run pre-commit install --hook-type pre-push
   ```
4. Point Claude Code at the new project with a description of what you want to build
5. Tell it to read this README and follow the bootstrap sequence

---

## What's Included

```
.
├── src/mypackage/
│   ├── __init__.py         # Package root (__version__, __all__)
│   └── py.typed            # PEP 561 type stub marker
├── tests/
│   └── unit/
│       └── test_smoke.py   # Smoke test for package import
├── docs/
│   ├── conf.py             # Sphinx config (Furo theme, MyST, autodoc, nbsphinx)
│   └── contributing.md     # Dev setup, testing, commit conventions
├── .github/
│   ├── workflows/
│   │   ├── test.yml        # Matrix test (Ubuntu+Windows, Py 3.11-3.13) + pre-commit + typecheck
│   │   ├── slow-tests.yml  # Manual dispatch for @pytest.mark.slow tests
│   │   ├── docs.yml        # Sphinx build with -W on PRs
│   │   ├── release.yml     # python-semantic-release on push to main
│   │   └── publish.yml     # PyPI publish on v* tags (OIDC trusted publishing)
│   ├── dependabot.yml      # Automated dependency updates (pip + GitHub Actions)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── .claude/rules/
│   ├── code-style.md       # Ruff, Google docstrings, naming conventions
│   ├── source-code.md      # __init__.py and docstring requirements (scoped to src/)
│   └── workflow.md         # GSD workflow instructions
├── .hooks/
│   ├── pre-push-ruff-check.sh
│   └── pre-push-ruff-format.sh
├── bootstrap.py            # Renames mypackage to your package name (self-deletes)
├── pyproject.toml          # Build system (Hatch), deps, tool config
├── .pre-commit-config.yaml
├── .readthedocs.yaml
├── .editorconfig
├── .gitattributes          # LF line endings enforced, binary file markers
├── .secrets.baseline
├── .gitignore
├── LICENSE                 # MIT
└── README.md               # This file (replace during bootstrap)
```

---

## Bootstrap Sequence

The agent should perform these steps in order when setting up a new project.

### 1. Run the bootstrap script

```bash
python bootstrap.py <package_name>
```

This renames `mypackage`/`MyPackage` across all files, moves `src/mypackage/` to `src/<package>/`, and self-deletes.

### 2. Set up the environment

```bash
pip install hatch
hatch env create
hatch run pre-commit install
hatch run pre-commit install --hook-type pre-push
```

### 3. Create the source package structure

Expand `src/<package>/` with subpackages as the project's architecture requires:

Every `__init__.py` must have: a module docstring, explicit imports of public symbols, and an `__all__` list. Every `.py` file starts with a one-line docstring.

Common subpackages:

| Directory | Purpose |
|-----------|---------|
| `core/` | Core domain logic |
| `config/` | Configuration, shared types, dataclasses |
| `io/` | File I/O, serialization, loaders |
| `utils/` | General-purpose helpers |

### 4. Create the test directories

```
tests/
├── unit/           # One test file per source module
├── synthetic/      # Integration tests with known ground truth
└── integration/    # End-to-end tests
```

Create whichever test directories the project actually needs. Write at least one passing test.

### 5. Create CLAUDE.md

The top-level `CLAUDE.md` is the primary agent instruction file. It should contain:

- **Project**: What the project does (1-2 sentences)
- **Environment**: Shell (Git Bash MINGW64), path format (`/c/Users/...`), project root, working directory
- **Architecture**: High-level overview of the codebase structure
- **Domain conventions**: Coordinate systems, units, key parameters (if applicable)
- **Testing**: How to run tests (all, fast-only, single file)
- **Common commands**: Copy-pasteable CLI examples

### 6. Create docs scaffolding

Create `docs/index.md` -- landing page with sphinx-design grid cards linking to API reference, contributing guide, and any other sections. Include a toctree. Follow the MyST markdown + Furo grid-card pattern.

Create `docs/api/index.rst` -- autodoc toctree, add one `.rst` file per source subpackage.

Create `docs/Makefile` and `docs/make.bat` (standard Sphinx quickstart output).

### 7. Create CODE_OF_CONDUCT.md

Standard [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). Update the enforcement contact URL to point to the project's GitHub issues.

### 8. Update pyproject.toml metadata

- `description`, `keywords`, `classifiers`
- `dependencies` (actual project deps)
- `[project.urls]` (all URLs)
- Uncomment `[project.scripts]` if the project has a CLI

### 9. Initialize tooling

```bash
detect-secrets scan > .secrets.baseline
```

### 10. Replace this README

Write a real project README with: description, installation, quick start, link to docs.

### 11. Verify

```bash
hatch run test                        # tests pass
hatch run lint                        # lint passes
hatch run typecheck                   # type check passes
hatch run pre-commit run --all-files   # hooks pass
```

---

## Decisions Encoded Here

### Tooling

| Tool | Purpose |
|------|---------|
| **Hatch** | Build system + environment management (replaces setuptools + venv + pip extras) |
| **Ruff** | Linting + formatting (replaces black, isort, flake8) |
| **basedpyright** | Static type checking |
| **pytest** | Testing, with `@pytest.mark.slow` for expensive tests |
| **pre-commit** | On-commit: ruff lint/format, trailing whitespace, YAML check, large file check, secret detection |
| **pre-push hooks** | Full ruff lint + ruff format check |
| **python-semantic-release** | Automated versioning from conventional commits |
| **Sphinx + Furo** | Documentation with MyST markdown, autodoc, nbsphinx for notebooks |
| **Dependabot** | Automated dependency updates for pip and GitHub Actions |
| **Codecov** | Coverage tracking in CI |

### Code Style

- **Formatter**: Ruff (line length 88, double quotes, space indent)
- **Docstrings**: Google style
- **Type hints**: Required on all public functions; document complex types in docstrings
- **Imports**: stdlib, then third-party, then local (blank line between groups)
- **Naming**: `snake_case.py` files, `PascalCase` classes, `snake_case` functions, `UPPER_SNAKE_CASE` constants
- **`__init__.py`**: Every package has one with explicit imports, `__all__`, and a module docstring
- **Every `.py` file** starts with a one-line module docstring

### Ruff Rules

| Code | Category |
|------|----------|
| `E4`, `E7`, `E9` | pycodestyle errors |
| `F` | pyflakes |
| `W` | pycodestyle warnings |
| `I` | isort |
| `UP` | pyupgrade |
| `B` | flake8-bugbear |
| `SIM` | flake8-simplify |
| `RUF` | Ruff-specific rules |
| `PT` | flake8-pytest-style |

### CI/CD Workflows

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `test.yml` | Push/PR to main | Matrix test (Ubuntu + Windows, Python 3.11-3.13), pre-commit check, basedpyright |
| `slow-tests.yml` | Manual dispatch | Full test suite including `@pytest.mark.slow` |
| `docs.yml` | PR to main | Build Sphinx docs with `-W` (warnings as errors) |
| `release.yml` | Push to main | `python-semantic-release` creates version tag from conventional commits |
| `publish.yml` | `v*` tag | Build + publish to TestPyPI then PyPI (OIDC trusted publishing) |

### Secrets Required for CI/CD

| Secret | Where | Purpose |
|--------|-------|---------|
| `CODECOV_TOKEN` | Repository secret | Coverage upload |
| `RELEASE_TOKEN` | Repository secret | PAT for semantic-release to push tags |
| PyPI OIDC | Environment `pypi` | Trusted publishing (no token needed) |
| TestPyPI OIDC | Environment `testpypi` | Trusted publishing (no token needed) |

### GSD Workflow

This template is designed to work with the GSD (Get Shit Done) workflow for Claude Code. After bootstrapping:

1. Run `/gsd:new-project` to initialize `.planning/PROJECT.md` and roadmap
2. The agent will create `.planning/` artifacts (architecture docs, phase plans, etc.)
3. These are auto-generated and tracked in `.planning/` -- don't manually edit them
