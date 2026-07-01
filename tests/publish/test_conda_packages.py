"""Tests for conda-package injection helpers."""

from __future__ import annotations

from publish.utils import ensure_conda_package


def test_adds_missing_package() -> None:
    assert ensure_conda_package("python=3.12 git", "uv") == "python=3.12 git uv"


def test_idempotent_when_already_present() -> None:
    assert ensure_conda_package("python=3.12 git uv", "uv") == "python=3.12 git uv"


def test_ignores_version_suffix_when_matching() -> None:
    # "python=3.12" already provides "python"; do not append a bare "python".
    assert ensure_conda_package("python=3.12 git", "python") == "python=3.12 git"


def test_adds_to_empty_string() -> None:
    assert ensure_conda_package("", "uv") == "uv"
