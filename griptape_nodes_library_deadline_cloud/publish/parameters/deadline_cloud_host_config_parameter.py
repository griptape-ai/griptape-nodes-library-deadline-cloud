from enum import StrEnum
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode
from griptape_nodes.traits.button import Button, ButtonDetailsMessagePayload
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
        self.allowed_modes = allowed_modes
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
                name="add_custom_amount_requirement",
                input_types=["str"],
                type="str",
                output_type="str",
                tooltip="Add a custom amount requirement for the job with a provided capability name.",
                ui_options={
                    "display_name": "Add custom amount capability",
                    "placeholder_text": "amount.custom_capability_name",
                },
                traits={
                    Button(
                        full_width=False,
                        icon="plus",
                        size="icon",
                        variant="secondary",
                        on_click=self._add_custom_amount_parameter,
                    ),
                },
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="add_custom_attribute_requirement",
                input_types=["str"],
                type="str",
                output_type="str",
                tooltip="Add a custom attribute requirement for the job with a provided capability name.",
                ui_options={
                    "display_name": "Add custom attribute capability",
                    "placeholder_text": "attr.custom_capability_name",
                },
                traits={
                    Button(
                        full_width=False,
                        icon="plus",
                        size="icon",
                        variant="secondary",
                        on_click=self._add_custom_attribute_parameter,
                    ),
                },
                allowed_modes=allowed_modes,
            )

        host_config_group.ui_options = {"collapsed": True}
        node.add_node_element(host_config_group)

    def _is_valid_capability_name(self, name: str, capability_type: str) -> None:
        # Format must match: [<Identifier>:]capability_type.<Identifier>[.<Identifier>]*, where the [] is optional
        min_parts = 2
        msg = f"Invalid {capability_type} capability name: '{name}'. Must follow format [<Identifier>:]{capability_type}.<Identifier>[.<Identifier>]*"
        parts = name.split(".")
        if len(parts) < min_parts or not parts[0].endswith(capability_type):
            raise ValueError(msg)

    def _add_custom_amount_parameter(self, button: Button, button_details: ButtonDetailsMessagePayload) -> None:  # noqa: ARG002
        name = self.node.get_parameter_value("add_custom_amount_requirement")
        self._is_valid_capability_name(name, "amount")
        new_param = Parameter(
            name=name,
            input_types=["dict"],
            type="dict",
            output_type="dict",
            tooltip=f"The custom amount requirement for {name}.",
            traits={NumbersSelector(defaults={"min": 0, "max": 0}, step=1, overall_min=0, overall_max=10000)},
            allowed_modes=self.allowed_modes,
            user_defined=True,
            parent_element_name="Host Config",
        )
        self.node.add_parameter(new_param)

    def _add_custom_attribute_parameter(self, button: Button, button_details: ButtonDetailsMessagePayload) -> None:  # noqa: ARG002
        name = self.node.get_parameter_value("add_custom_attribute_requirement")
        self._is_valid_capability_name(name, "attr")
        parent_group_name = "Host Config"

        new_attr_anyof_param = Parameter(
            name=f"{name}.anyOf",
            input_types=["list"],
            type="list",
            output_type="list",
            tooltip=f"The custom attribute anyOf requirement for {name}.",
            ui_options={
                "display_name": f"{name}.anyOf",
                "placeholder_text": 'E.g., "value1, value2"',
            },
            traits={
                MultiOptions(
                    choices=[],
                    placeholder="Enter acceptable values",
                    max_selected_display=5,
                    allow_user_created_options=True,
                )
            },
            user_defined=True,
            allowed_modes=self.allowed_modes,
            parent_element_name=parent_group_name,
        )
        new_attr_allof_param = Parameter(
            name=f"{name}.allOf",
            input_types=["list"],
            type="list",
            output_type="list",
            tooltip=f"The custom attribute allOf requirement for {name}.",
            traits={
                MultiOptions(
                    choices=[],
                    placeholder="Enter acceptable values",
                    max_selected_display=5,
                    allow_user_created_options=True,
                )
            },
            user_defined=True,
            allowed_modes=self.allowed_modes,
            parent_element_name=parent_group_name,
        )
        self.node.add_parameter(new_attr_anyof_param)
        self.node.add_parameter(new_attr_allof_param)

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
            "add_custom_amount_requirement",
            "add_custom_attribute_requirement",
        ]

    @classmethod
    def _get_host_config_parameters_for_node(cls, node: BaseNode) -> dict[str, Any]:
        """Get all host configuration parameters from a node.

        Args:
            node: The node to get parameters from

        Returns:
            Dictionary of host configuration parameter names to values
        """
        param_names = [
            name
            for name in cls.get_param_names()
            if name
            not in ["run_on_all_worker_hosts", "add_custom_amount_requirement", "add_custom_attribute_requirement"]
        ]
        params = {name: node.get_parameter_value(name) for name in param_names}

        # Merge in custom amount requirements
        custom_amount_parameters = cls._get_custom_requirement_parameters_by_type_for_node(node, "amount")
        for entry in (
            [{p.name: node.get_parameter_value(p.name)} for p in custom_amount_parameters]
            if custom_amount_parameters
            else []
        ):
            params.update(entry)

        # Merge in custom attribute requirements
        custom_attribute_parameters = cls._get_custom_requirement_parameters_by_type_for_node(node, "attr")
        for parameter in [c for c in custom_attribute_parameters if c.type == "list"]:
            if parameter.name.endswith(".anyOf"):
                attribute_type = "anyOf"
            elif parameter.name.endswith(".allOf"):
                attribute_type = "allOf"
            else:
                continue
            attribute_name = parameter.name.split(f".{attribute_type}")[0]
            if attribute_name not in params:
                params[attribute_name] = {}
            param_value = node.get_parameter_value(parameter.name)
            if param_value:
                params[attribute_name][attribute_type] = param_value
        return params

    def _get_host_config_parameters(self) -> dict[str, Any]:
        """Get all host configuration parameters from the node."""
        return self._get_host_config_parameters_for_node(self.node)

    @classmethod
    def _build_attribute_requirements(cls, params: dict[str, Any]) -> list[dict[str, Any]]:
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

        for param in [p for p in params.items() if "attr." in p[0] and p[0] not in [a["name"] for a in attributes]]:
            custom_attribute_entry = cls._create_attribute_entry(param[0], param[1])
            if custom_attribute_entry:
                attributes.append(custom_attribute_entry)

        return attributes

    @classmethod
    def _create_attribute_entry(cls, name: str, config: dict[str, Any]) -> dict[str, Any] | None:
        """Create an attribute entry if config has valid anyOf/allOf values."""
        if not config or (not config.get("anyOf") and not config.get("allOf")):
            return None

        entry = {"name": name}

        any_of = config.get("anyOf", [])
        if any_of:
            entry["anyOf"] = any_of

        all_of = config.get("allOf", [])
        if all_of:
            entry["allOf"] = all_of

        return entry

    @classmethod
    def _create_amount_entry(
        cls, name: str, config: dict[str, Any], multiplier: int = 1, default_min: int = 0
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

    @classmethod
    def _get_custom_requirement_parameters_by_type_for_node(
        cls, node: BaseNode, custom_requirement_type: str
    ) -> list[Parameter]:
        """Get custom requirement parameters of a specific type from a node.

        Args:
            node: The node to get parameters from
            custom_requirement_type: The type of custom requirement ("amount" or "attr")

        Returns:
            List of Parameter objects matching the custom requirement type
        """
        parameters = node.parameters
        return [
            p
            for p in parameters
            if p.name not in cls.get_param_names()
            and f"{custom_requirement_type}." in p.name
            and p.parent_group_name == "Host Config"
        ]

    def _get_custom_requirement_parameters_by_type(self, custom_requirement_type: str) -> list[Parameter]:
        return self._get_custom_requirement_parameters_by_type_for_node(self.node, custom_requirement_type)

    @classmethod
    def _build_amount_requirements(cls, params: dict[str, Any]) -> list[dict[str, Any]]:
        """Build amount requirements for host configuration."""
        amounts = []

        # vCPU (defaults to min of 1)
        vcpu_entry = cls._create_amount_entry("amount.worker.vcpu", params["vcpu"], default_min=1)
        if vcpu_entry:
            amounts.append(vcpu_entry)

        # Memory (GiB to MiB conversion, defaults to min of 0)
        memory_entry = cls._create_amount_entry("amount.worker.memory", params["memory"], 1024, default_min=0)
        if memory_entry:
            amounts.append(memory_entry)

        # GPUs (defaults to min of 0)
        gpu_entry = cls._create_amount_entry("amount.worker.gpu", params["gpus"], default_min=0)
        if gpu_entry:
            amounts.append(gpu_entry)

        # GPU memory (GiB to MiB conversion, defaults to min of 0)
        gpu_memory_entry = cls._create_amount_entry(
            "amount.worker.gpu.memory", params["gpu_memory"], 1024, default_min=0
        )
        if gpu_memory_entry:
            amounts.append(gpu_memory_entry)

        # Scratch space (GiB to MiB conversion, defaults to min of 0)
        scratch_entry = cls._create_amount_entry("amount.worker.scratch", params["scratch_space"], 1024, default_min=0)
        if scratch_entry:
            amounts.append(scratch_entry)

        for param in [p for p in params.items() if "amount." in p[0] and p[0] not in [a["name"] for a in amounts]]:
            custom_amount_entry = cls._create_amount_entry(param[0], param[1], default_min=0)
            if custom_amount_entry:
                amounts.append(custom_amount_entry)

        return amounts

    # https://github.com/OpenJobDescription/openjd-specifications/wiki/2023-09-Template-Schemas#3311-amountcapabilityname
    @classmethod
    def get_host_config_job_template_dict_for_node(cls, node: BaseNode) -> dict[str, Any]:
        """Build host configuration dictionary for job template from a node's parameters.

        Args:
            node: The node to get host configuration parameters from

        Returns:
            Dictionary containing 'amounts' and/or 'attributes' for host requirements
        """
        params = cls._get_host_config_parameters_for_node(node)
        amounts = cls._build_amount_requirements(params)
        attributes = cls._build_attribute_requirements(params)

        host_config: dict[str, Any] = {}

        if amounts:
            host_config["amounts"] = amounts
        if attributes:
            host_config["attributes"] = attributes

        return host_config

    def get_host_config_job_template_dict(self) -> dict[str, Any]:
        """Build host configuration dictionary for job template."""
        return self.get_host_config_job_template_dict_for_node(self.node)

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
