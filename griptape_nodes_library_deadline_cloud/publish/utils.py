"""Shared utilities for Deadline Cloud publishing."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from griptape_nodes.files.project_file import ProjectFileDestination
from griptape_nodes.retained_mode.events.project_events import (
    GetSituationRequest,
    GetSituationResultSuccess,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from typing import TextIO

    from griptape_nodes.node_library.library_registry import Dependencies

logger = logging.getLogger(__name__)

# The situation name that defines where metadata sidecars are saved.
METADATA_SITUATION_NAME = "save_griptape_nodes_metadata"


def write_library_deps(req_file: TextIO, deps: Dependencies) -> None:
    """Write a library's pip_dependencies into a requirements.txt file handle.

    Editable installs (``-e ...``) are skipped because they reference local
    checkouts that do not exist on the worker.

    ``pip_install_flags`` are intentionally NOT written here. They are uv-only
    CLI flags (e.g. ``--preview``, ``--torch-backend=auto``) that plain pip
    rejects, so they are passed on the ``uv pip install`` command line via the
    ``PipInstallFlags`` job parameter instead of being embedded in the file.
    """
    for dep in deps.pip_dependencies or []:
        if dep.startswith("-e"):
            continue
        req_file.write(f"{dep}\n")


def collect_pip_install_flags(deps_list: Iterable[Dependencies]) -> list[str]:
    """Collect unique pip_install_flags across a set of library dependencies.

    Order is preserved and duplicates are dropped so the flags can be passed on
    a single ``uv pip install`` command line.
    """
    flags: list[str] = []
    for deps in deps_list:
        for flag in deps.pip_install_flags or []:
            if flag not in flags:
                flags.append(flag)
    return flags


def ensure_conda_package(conda_packages: str, package: str) -> str:
    """Ensure a package name is present in a space-separated conda packages string.

    A package is considered present if its bare name matches (ignoring any
    ``=version`` suffix), so ``python=3.12`` counts as ``python`` already present.
    """
    present = {token.split("=", 1)[0] for token in conda_packages.split()}
    if package not in present:
        conda_packages = f"{conda_packages} {package}".strip()
    return conda_packages


def build_venv_script() -> str:
    """Return the worker environment setup script (Open Job Description onEnter).

    The script resolves the Python 3.12 interpreter from the conda queue
    environment, installs dependencies with uv (which understands the uv-only
    ``PipInstallFlags``), and symlinks that interpreter into each library's
    ``.venv/bin/python``.

    ``{{Param.*}}`` tokens are Open Job Description parameter macros and must be
    preserved verbatim.
    """
    return """#!/bin/env bash
set -e
echo 'Setting up Python virtual environment...'

# Resolve the Python 3.12 interpreter from the conda queue environment. The
# default worker AMI's system python is 3.11, which cannot resolve the engine
# (requires-python >=3.12,<3.13), so never trust a bare `python` on PATH.
if [ -n "$CONDA_PREFIX" ] && [ -x "$CONDA_PREFIX/bin/python" ]; then
    TARGET_PYTHON="$CONDA_PREFIX/bin/python"
else
    TARGET_PYTHON="$(command -v python3.12 || command -v python)"
fi
echo "Using Python interpreter: $TARGET_PYTHON"
if ! "$TARGET_PYTHON" --version 2>&1 | grep -q ' 3.12'; then
    echo "ERROR: expected Python 3.12 but found $("$TARGET_PYTHON" --version 2>&1)." >&2
    echo "Ensure the queue's conda environment provides python=3.12." >&2
    exit 1
fi

# Ensure uv is available. Prefer conda-provided uv; otherwise install the
# standalone binary so the default worker AMI still works.
if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
else
    echo 'uv not found; installing standalone uv...'
    export UV_INSTALL_DIR="{{Param.LocationToRemap}}/.uv-bin"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    UV_BIN="$UV_INSTALL_DIR/uv"
fi
echo "Using uv: $UV_BIN"

echo 'Installing dependencies...'
"$UV_BIN" pip install --python "$TARGET_PYTHON" {{Param.PipInstallFlags}} -r {{Param.LocationToRemap}}/assets/requirements.txt
mkdir -p {{Param.LocationToRemap}}/output

# Create .venv symlinks in libraries so library code that expects its own
# venv (e.g. _get_library_env_python) finds a working Python with all deps.
for lib_dir in {{Param.LocationToRemap}}/assets/libraries/*/; do
    if [ -f "${lib_dir}griptape-nodes-library.json" ] || [ -f "${lib_dir}griptape-nodes-library-cuda129.json" ]; then
        mkdir -p "${lib_dir}.venv/bin"
        ln -sf "$TARGET_PYTHON" "${lib_dir}.venv/bin/python"
        echo "Created .venv symlink in ${lib_dir}"
    fi
done

echo 'Virtual environment setup complete.'
"""


def get_metadata_dir_name() -> str | None:
    """Return the logical metadata directory name from the current project.

    Uses ``GetSituationRequest`` to look up the ``save_griptape_nodes_metadata``
    situation, then extracts the leading ``{directory}`` macro segment to
    determine the directory name used for metadata sidecars.

    Returns:
        The directory name (e.g. ``"griptape-nodes-metadata"``), or ``None``
        if the situation is not defined in the template.
    """
    result = GriptapeNodes.handle_request(GetSituationRequest(situation_name=METADATA_SITUATION_NAME))
    if not isinstance(result, GetSituationResultSuccess):
        return None

    macro = result.situation.macro
    # Extract the first {name} token from the macro string.
    if macro.startswith("{"):
        end = macro.index("}")
        return macro[1:end].split("?")[0]  # strip optional-format suffix

    return None


def collect_metadata_sidecars(downloaded_files: dict[str, Path]) -> dict[str, dict[str, Any]]:
    """Collect metadata sidecar JSON files from the downloaded output.

    Scans the downloaded files for metadata sidecars under the Deadline
    metadata directory and returns a mapping from the relative output file
    path they describe to the parsed sidecar content.

    For example, a sidecar at ``griptape-nodes-metadata/outputs/clown.png.json``
    maps to the key ``outputs/clown.png``.

    Args:
        downloaded_files: Map of relative paths within the output dir to
            their full local paths on disk.

    Returns:
        A dict mapping relative output file paths to their sidecar content.
    """
    metadata_dir_name = get_metadata_dir_name()
    if metadata_dir_name is None:
        return {}

    sidecars: dict[str, dict[str, Any]] = {}
    metadata_prefix = f"{metadata_dir_name}/"

    for relative_path, local_path in downloaded_files.items():
        if not relative_path.startswith(metadata_prefix):
            continue
        if not relative_path.endswith(".json"):
            continue

        # Derive the output file path this sidecar describes:
        # "griptape-nodes-metadata/outputs/clown.png.json" -> "outputs/clown.png"
        sidecar_subpath = relative_path[len(metadata_prefix) :]
        if sidecar_subpath.endswith(".json"):
            output_file_path = sidecar_subpath[: -len(".json")]
        else:
            continue

        try:
            with local_path.open(encoding="utf-8") as f:
                sidecar_content = json.load(f)
            sidecars[output_file_path] = sidecar_content
            logger.debug("Loaded metadata sidecar for '%s'", output_file_path)
        except Exception:
            logger.warning("Failed to parse metadata sidecar at '%s'", local_path)

    return sidecars


def write_sidecar_output_files(
    downloaded_files: dict[str, Path],
    metadata_sidecars: dict[str, dict[str, Any]],
) -> set[str]:
    """Write output files that have metadata sidecars using situation-aware saving.

    Iterates over the collected metadata sidecars and writes each corresponding
    downloaded file via ``ProjectFileDestination``, which re-resolves the
    situation against the client's project template (including collision handling).

    Args:
        downloaded_files: Map of relative paths to their downloaded local paths.
        metadata_sidecars: Map of relative output file paths to their sidecar content.

    Returns:
        The set of relative paths that were successfully written via sidecar,
        so that the caller can skip these during fallback macro-based writing.
    """
    written: set[str] = set()

    for relative_path, sidecar in metadata_sidecars.items():
        source_path = downloaded_files.get(relative_path)
        if source_path is None or not source_path.exists():
            continue

        situation_info = sidecar.get("situation", {})
        situation_name = situation_info.get("name")
        variables = situation_info.get("variables", {})

        if not situation_name:
            logger.warning("Sidecar for '%s' missing situation name, skipping", relative_path)
            continue

        # Build the filename from variables
        file_name_base = variables.get("file_name_base", "output")
        file_extension = variables.get("file_extension", "bin")
        filename = f"{file_name_base}.{file_extension}"

        # Pass all variables except file_name_base and file_extension as extra_vars,
        # since ProjectFileDestination extracts those from the filename.
        extra_vars = {k: v for k, v in variables.items() if k not in ("file_name_base", "file_extension")}

        try:
            file_bytes = source_path.read_bytes()
            dest = ProjectFileDestination.from_situation(filename, situation_name, **extra_vars)
            result_file = dest.write_bytes(file_bytes)
        except Exception as e:
            logger.warning(
                "Failed to write output via situation '%s' for '%s': %s",
                situation_name,
                relative_path,
                e,
            )
        else:
            written.add(relative_path)
            logger.info(
                "Wrote output via situation '%s' -> '%s'",
                situation_name,
                result_file.resolve() if result_file else relative_path,
            )

    return written
