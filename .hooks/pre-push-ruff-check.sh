#!/usr/bin/env bash
ruff check src/ tests/ || {
    echo ""
    echo "Push failed: ruff lint errors."
    echo 'Run "ruff check --fix src/ tests/" to auto-fix.'
    exit 1
}
