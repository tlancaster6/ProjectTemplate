# Project Template

A Python project template designed for AI-assisted development with Claude Code

## Setup (Two Phases)

### Phase 1: Bootstrap the repository

1. Copy this template into a new project directory
2. Run the bootstrap script to rename the package and set metadata:
   ```bash
   python bootstrap.py <package_name> --author "Your Name" --github-user yourusername
   ```
3. Set up the development environment:
   ```bash
   pip install hatch
   hatch env create
   hatch run pre-commit install
   hatch run pre-commit install --hook-type pre-push
   ```
4. Verify the template works:
   ```bash
   hatch run test
   hatch run lint
   hatch run typecheck
   ```

### Phase 2: Initialize the project

Open the project in Claude Code and run `/gsd:new-project`. This starts an interactive session that:

- Captures your project's goals, scope, and architecture
- Creates `.planning/PROJECT.md` with the project context
- Generates a phased roadmap for execution

The agent will use the bootstrap instructions in `.claude/rules/bootstrap.md` to finish scaffolding (source structure, tests, docs, CLAUDE.md, etc.) as part of the first phase of work.

## What's Included

### Tooling

| Tool | Purpose |
|------|---------|
| **Hatch** | Build system + environment management |
| **Ruff** | Linting + formatting |
| **basedpyright** | Static type checking |
| **pytest** | Testing, with `@pytest.mark.slow` for expensive tests |
| **pre-commit** | On-commit: ruff, trailing whitespace, YAML check, secret detection |
| **pre-push hooks** | Full ruff lint + format check |
| **python-semantic-release** | Automated versioning from conventional commits |
| **Sphinx + Furo** | Documentation (MyST markdown, autodoc, nbsphinx) |
| **Dependabot** | Automated dependency updates (pip + GitHub Actions) |
| **Codecov** | Coverage tracking in CI |

### CI/CD Workflows

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `test.yml` | Push/PR to main | Matrix test (Ubuntu + Windows, Python 3.11-3.13), pre-commit, basedpyright |
| `slow-tests.yml` | Manual dispatch | Full test suite including `@pytest.mark.slow` |
| `docs.yml` | PR to main | Sphinx build with `-W` (warnings as errors) |
| `release.yml` | Push to main | Semantic versioning from conventional commits |
| `publish.yml` | `v*` tag | Build + publish to TestPyPI then PyPI (OIDC trusted publishing) |

### Secrets Required for CI/CD

| Secret | Where | Purpose |
|--------|-------|---------|
| `CODECOV_TOKEN` | Repository secret | Coverage upload |
| `RELEASE_TOKEN` | Repository secret | PAT for semantic-release to push tags |
| PyPI OIDC | Environment `pypi` | Trusted publishing (no token needed) |
| TestPyPI OIDC | Environment `testpypi` | Trusted publishing (no token needed) |

### Code Style

- **Formatter**: Ruff (line length 88, double quotes, space indent)
- **Docstrings**: Google style
- **Type hints**: Required on all public functions
- **Imports**: stdlib, then third-party, then local (blank line between groups)
- **Naming**: `snake_case.py` files, `PascalCase` classes, `snake_case` functions, `UPPER_SNAKE_CASE` constants

### Ruff Rules

`E4`, `E7`, `E9` (pycodestyle), `F` (pyflakes), `W` (warnings), `I` (isort), `UP` (pyupgrade), `B` (bugbear), `SIM` (simplify), `RUF` (ruff-specific), `PT` (pytest-style)

## File Structure

```
.
├── src/mypackage/
│   ├── __init__.py         # Package root (version via importlib.metadata, __all__)
│   └── py.typed            # PEP 561 type stub marker
├── tests/unit/
│   └── test_smoke.py       # Smoke test for package import
├── docs/
│   ├── conf.py             # Sphinx config (Furo, MyST, autodoc, nbsphinx)
│   └── contributing.md     # Dev setup, testing, commit conventions
├── .github/
│   ├── workflows/          # CI/CD (test, slow-tests, docs, release, publish)
│   ├── dependabot.yml      # Automated dependency updates
│   ├── ISSUE_TEMPLATE/     # Bug report + feature request forms
│   └── PULL_REQUEST_TEMPLATE.md
├── .claude/rules/
│   ├── bootstrap.md        # Agent bootstrap instructions
│   ├── code-style.md       # Formatting and naming conventions
│   ├── source-code.md      # __init__.py and docstring requirements
│   └── workflow.md         # GSD workflow instructions
├── .hooks/                 # Pre-push ruff lint + format scripts
├── bootstrap.py            # Renames mypackage to your package (self-deletes)
├── README_TEMPLATE.md      # Skeletal project README (replaces this file)
├── pyproject.toml          # Build system (Hatch), deps, tool config
├── .pre-commit-config.yaml
├── .readthedocs.yaml
├── .editorconfig
├── .gitattributes
├── .secrets.baseline
├── .gitignore
└── LICENSE                 # MIT
```
