"""Smoke tests for package import."""

import mypackage


def test_version():
    assert mypackage.__version__
