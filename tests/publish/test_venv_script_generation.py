"""Tests for the worker environment setup script and job template generation.

Regression coverage for issue #106 and its follow-up: the worker must install
with uv (which understands the uv-only flags) and must target the conda Python
3.12 interpreter rather than the AMI's system Python 3.11.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from publish.deadline_cloud_job_template_generator import DeadlineCloudJobTemplateGenerator
from publish.utils import build_venv_script


def test_venv_script_installs_with_uv_not_plain_pip() -> None:
    script = build_venv_script()
    assert '"$UV_BIN" pip install' in script
    # The old broken form ran plain pip directly against requirements.txt.
    assert "\npip install -r" not in script
    assert "python -m pip install --upgrade" not in script


def test_venv_script_targets_conda_python_312() -> None:
    script = build_venv_script()
    assert "CONDA_PREFIX" in script
    assert '--python "$TARGET_PYTHON"' in script
    # Fails fast instead of looping when the interpreter is not 3.12.
    assert "grep -q ' 3.12'" in script
    assert "exit 1" in script


def test_venv_script_preserves_ojd_macros() -> None:
    script = build_venv_script()
    assert "{{Param.LocationToRemap}}" in script
    assert "{{Param.PipInstallFlags}}" in script


def test_generate_job_template_bakes_flags_and_uv() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        template = DeadlineCloudJobTemplateGenerator.generate_job_template(
            Path(tmp),
            "My Workflow",
            ["/tmp/lib"],
            pip_install_flags=["--preview", "--torch-backend=auto"],
        )

    params = {p["name"]: p for p in template["parameterDefinitions"]}
    assert "uv" in params["CondaPackages"]["default"].split()
    assert params["PipInstallFlags"]["default"] == "--preview --torch-backend=auto"


def test_generate_job_template_defaults_flags_to_empty_string() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        template = DeadlineCloudJobTemplateGenerator.generate_job_template(
            Path(tmp),
            "My Workflow",
            ["/tmp/lib"],
        )
    params = {p["name"]: p for p in template["parameterDefinitions"]}
    assert params["PipInstallFlags"]["default"] == ""
