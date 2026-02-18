"""Smoke tests for package import."""

import mypackage


def test_version():
    assert mypackage.__version__ == "0.1.0"
