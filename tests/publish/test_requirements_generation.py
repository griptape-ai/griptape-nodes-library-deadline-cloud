"""Tests for requirements.txt generation from library dependencies.

Regression coverage for issue #106: uv-only ``pip_install_flags`` (e.g.
``--preview``, ``--torch-backend=auto``) must NOT be written into
requirements.txt, because the worker's plain pip would reject them. Instead they
are collected and passed on the ``uv pip install`` command line.
"""

from __future__ import annotations

import io

from griptape_nodes.node_library.library_registry import Dependencies

from publish.utils import collect_pip_install_flags, write_library_deps


def _render(deps: Dependencies) -> str:
    buffer = io.StringIO()
    write_library_deps(buffer, deps)
    return buffer.getvalue()


def test_pip_dependencies_written_one_per_line() -> None:
    deps = Dependencies(pip_dependencies=["torch==2.7.0", "diffusers>=0.30"])
    lines = _render(deps).splitlines()
    assert lines == ["torch==2.7.0", "diffusers>=0.30"]


def test_pip_install_flags_are_not_written_to_requirements() -> None:
    deps = Dependencies(
        pip_dependencies=["torch==2.7.0"],
        pip_install_flags=["--preview", "--torch-backend=auto"],
    )
    rendered = _render(deps)
    assert "--preview" not in rendered
    assert "--torch-backend" not in rendered
    assert rendered.splitlines() == ["torch==2.7.0"]


def test_editable_installs_are_skipped() -> None:
    deps = Dependencies(pip_dependencies=["-e ./local-checkout", "torch==2.7.0"])
    assert _render(deps).splitlines() == ["torch==2.7.0"]


def test_empty_dependencies_write_nothing() -> None:
    assert _render(Dependencies()) == ""


def test_collect_pip_install_flags_dedupes_preserving_order() -> None:
    a = Dependencies(pip_install_flags=["--preview", "--torch-backend=auto"])
    b = Dependencies(pip_install_flags=["--torch-backend=auto", "--index-strategy=unsafe"])
    assert collect_pip_install_flags([a, b]) == [
        "--preview",
        "--torch-backend=auto",
        "--index-strategy=unsafe",
    ]


def test_collect_pip_install_flags_handles_none() -> None:
    assert collect_pip_install_flags([Dependencies(pip_dependencies=["torch"])]) == []
