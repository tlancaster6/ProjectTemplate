#!/usr/bin/env bash
ruff format --check src/ tests/ || {
    echo ""
    echo "Push failed: format violations."
    echo 'Run "ruff format src/ tests/" to fix.'
    exit 1
}
