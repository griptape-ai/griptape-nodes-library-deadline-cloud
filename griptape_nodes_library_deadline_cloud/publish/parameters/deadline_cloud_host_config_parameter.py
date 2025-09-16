from enum import StrEnum
from typing import Any, cast

from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode
from griptape_nodes.traits.multi_options import MultiOptions
from griptape_nodes.traits.numbers_selector import NumbersSelector


class WorkerOSFamily(StrEnum):
    """Status enum for worker operating systems."""

    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"


class WorkerCPUArchitecture(StrEnum):
    """Status enum for worker CPU architectures."""

    X86_64 = "x86_64"
    ARM64 = "arm64"


class DeadlineCloudHostConfigParameter:
    def __init__(self, node: BaseNode, allowed_modes: set[ParameterMode] | None = None) -> None:
        self.node = node
        # Add host config group
        with ParameterGroup(name="Host Config") as host_config_group:
            Parameter(
                name="run_on_all_worker_hosts",
                input_types=["bool"],
                type="bool",
                output_type="bool",
                default_value=True,
                tooltip="Whether to run the job on all worker hosts.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="operating_system",
                input_types=["list"],
                type="list",
                output_type="list",
                default_value=None,
                tooltip="The operating system to run the job on.",
                traits={
                    MultiOptions(
                        choices=[str(val.value) for val in WorkerOSFamily],
                        placeholder="Select operating systems for the job",
                        max_selected_display=5,
                    )
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="cpu_architecture",
                input_types=["list"],
                type="list",
                output_type="list",
                default_value=None,
                tooltip="The CPU architecture to run the job on.",
                traits={
                    MultiOptions(
                        choices=[str(val.value) for val in WorkerCPUArchitecture],
                        placeholder="Select CPU architectures for the job",
                        max_selected_display=5,
                    )
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="vcpu",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=None,
                tooltip="The vCPU configuration for the job.",
                traits={NumbersSelector(defaults={"min": 1, "max": 0}, step=1, overall_min=1, overall_max=10000)},
                ui_options={
                    "display_name": "vCPU",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="memory",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=None,
                tooltip="The memory configuration for the job.",
                traits={NumbersSelector(defaults={"min": 0, "max": 0}, step=1, overall_min=0, overall_max=10000)},
                ui_options={
                    "display_name": "Memory (GiB)",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="gpus",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=None,
                tooltip="The GPU configuration for the job.",
                traits={NumbersSelector(defaults={"min": 0, "max": 0}, step=1, overall_min=0, overall_max=20)},
                ui_options={
                    "display_name": "GPUs",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="gpu_memory",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=None,
                tooltip="The GPU memory configuration for the job.",
                traits={NumbersSelector(defaults={"min": 0, "max": 0}, step=1, overall_min=0, overall_max=10000)},
                ui_options={
                    "display_name": "GPU memory (GiB)",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="scratch_space",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=None,
                tooltip="The scratch space configuration for the job.",
                traits={NumbersSelector(defaults={"min": 0, "max": 0}, step=1, overall_min=0, overall_max=10000)},
                ui_options={
                    "display_name": "Scratch space",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="custom_amount_requirements",
                input_types=["list"],
                type="list",
                output_type="list",
                tooltip="The custom amount requirements for the job.",
                ui_options={
                    "display_name": "Custom amount requirements",
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="custom_attribute_requirements",
                input_types=["list"],
                type="list",
                output_type="list",
                tooltip="The custom attribute requirements for the job.",
                ui_options={
                    "display_name": "Custom attribute requirements",
                },
                allowed_modes=allowed_modes,
            )

        host_config_group.ui_options = {"collapsed": True}
        node.add_node_element(host_config_group)

    @classmethod
    def get_param_names(cls) -> list[str]:
        return [
            "run_on_all_worker_hosts",
            "operating_system",
            "cpu_architecture",
            "vcpu",
            "memory",
            "gpus",
            "gpu_memory",
            "scratch_space",
            "custom_amount_requirements",
            "custom_attribute_requirements",
        ]

    def _get_host_config_parameters(self) -> dict[str, Any]:
        """Get all host configuration parameters from the node."""
        return {
            "operating_system": self.node.get_parameter_value("operating_system"),
            "cpu_architecture": self.node.get_parameter_value("cpu_architecture"),
            "vcpu": self.node.get_parameter_value("vcpu"),
            "memory": self.node.get_parameter_value("memory"),
            "gpus": self.node.get_parameter_value("gpus"),
            "gpu_memory": self.node.get_parameter_value("gpu_memory"),
            "scratch_space": self.node.get_parameter_value("scratch_space"),
            "custom_amount_requirements": self.node.get_parameter_value("custom_amount_requirements"),
            "custom_attribute_requirements": self.node.get_parameter_value("custom_attribute_requirements"),
        }

    def _build_attribute_requirements(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        """Build attribute requirements for host configuration."""
        attributes = []

        if params["operating_system"]:
            attributes.append(
                {
                    "name": "attr.worker.os.family",
                    "anyOf": params["operating_system"],
                }
            )

        if params["cpu_architecture"]:
            attributes.append(
                {
                    "name": "attr.worker.cpu.arch",
                    "anyOf": params["cpu_architecture"],
                }
            )

        if params["custom_attribute_requirements"]:
            attributes.extend(params["custom_attribute_requirements"])

        return attributes

    def _create_amount_entry(
        self, name: str, config: dict[str, Any], multiplier: int = 1, default_min: int = 0
    ) -> dict[str, Any] | None:
        """Create an amount entry if config has valid min/max values."""
        if not config or (config.get("min", 0) <= 0 and config.get("max", 0) <= 0):
            return None

        entry = {"name": name}

        min_val = config.get("min", default_min)
        if min_val > default_min:
            entry["min"] = min_val * multiplier

        max_val = config.get("max", 0)
        if max_val > 0:
            entry["max"] = max_val * multiplier

        return entry

    def _build_amount_requirements(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        """Build amount requirements for host configuration."""
        amounts = []

        # vCPU (defaults to min of 1)
        vcpu_entry = self._create_amount_entry("amount.worker.vcpu", params["vcpu"], default_min=1)
        if vcpu_entry:
            amounts.append(vcpu_entry)

        # Memory (GiB to MiB conversion, defaults to min of 0)
        memory_entry = self._create_amount_entry("amount.worker.memory", params["memory"], 1024, default_min=0)
        if memory_entry:
            amounts.append(memory_entry)

        # GPUs (defaults to min of 0)
        gpu_entry = self._create_amount_entry("amount.worker.gpu", params["gpus"], default_min=0)
        if gpu_entry:
            amounts.append(gpu_entry)

        # GPU memory (GiB to MiB conversion, defaults to min of 0)
        gpu_memory_entry = self._create_amount_entry(
            "amount.worker.gpu.memory", params["gpu_memory"], 1024, default_min=0
        )
        if gpu_memory_entry:
            amounts.append(gpu_memory_entry)

        # Scratch space (GiB to MiB conversion, defaults to min of 0)
        scratch_entry = self._create_amount_entry("amount.worker.scratch", params["scratch_space"], 1024, default_min=0)
        if scratch_entry:
            amounts.append(scratch_entry)

        if params["custom_amount_requirements"]:
            amounts.extend(params["custom_amount_requirements"])

        return amounts

    # https://github.com/OpenJobDescription/openjd-specifications/wiki/2023-09-Template-Schemas#3311-amountcapabilityname
    def get_host_config_job_template_dict(self) -> dict[str, Any]:
        """Build host configuration dictionary for job template."""
        params = self._get_host_config_parameters()
        amounts = self._build_amount_requirements(params)
        attributes = self._build_attribute_requirements(params)

        host_config = {}

        if amounts:
            host_config["amounts"] = amounts
        if attributes:
            host_config["attributes"] = attributes

        return host_config

    def set_host_config_param_visibility(self, *, visible: bool) -> None:
        params = self.get_param_names()
        params.remove("run_on_all_worker_hosts")  # Always show this param
        for param in params:
            if visible:
                self.node.show_parameter_by_name(param)
            else:
                self.node.hide_parameter_by_name(param)

    def _validate_amount_entry(self, entry: dict[str, Any]) -> list[Exception] | None:
        errors = []
        if "name" not in entry:
            errors.append(ValueError("Missing 'name' in amount entry"))
        if "min" not in entry and "max" not in entry:
            errors.append(ValueError("Missing both 'min' and 'max' in amount entry"))
        return errors if errors else None

    def _validate_attribute_entry(self, entry: dict[str, Any]) -> list[Exception] | None:
        errors = []
        if "name" not in entry:
            errors.append(ValueError("Missing 'name' in attribute entry"))
        if "anyOf" not in entry and "allOf" not in entry:
            errors.append(ValueError("Missing 'anyOf' and 'allOf' in attribute entry"))
        return errors if errors else None

    def validate_custom_host_config(self) -> list[Exception] | None:
        custom_amount_requirements = self.node.get_parameter_value("custom_amount_requirements")
        custom_attribute_requirements = self.node.get_parameter_value("custom_attribute_requirements")

        if custom_amount_requirements is not None:
            custom_amount_requirements = cast("list", custom_amount_requirements)
            for entry in custom_amount_requirements:
                if not isinstance(entry, dict):
                    continue

                # Validate each entry in the custom amount requirements
                errors = self._validate_amount_entry(entry)
                if errors:
                    return errors

        if custom_attribute_requirements is not None:
            custom_attribute_requirements = cast("list", custom_attribute_requirements)
            for entry in custom_attribute_requirements:
                if not isinstance(entry, dict):
                    continue

                # Validate each entry in the custom attribute requirements
                errors = self._validate_attribute_entry(entry)
                if errors:
                    return errors

        return None
