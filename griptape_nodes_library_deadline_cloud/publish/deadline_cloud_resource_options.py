import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter
from griptape_nodes.traits.options import Options

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(eq=False)
class DeadlineCloudResourceOptions(Options):
    choices_value_lookup: dict[str, Any] = field(kw_only=True)
    value_field: str = field(kw_only=True, default="farmId")

    def __init__(self, choices: list, choices_value_lookup: dict[str, Any], value_field: str = "farmId") -> None:
        super().__init__(choices=choices)
        self.choices_value_lookup = choices_value_lookup
        self.value_field = value_field

    def converters_for_trait(self) -> list[Callable]:
        def converter(value: Any) -> Any:
            if value not in self.choices:
                attempt_to_get_value = next(
                    (key for key, val in self.choices_value_lookup.items() if val == value), None
                )
                if attempt_to_get_value is not None:
                    value = attempt_to_get_value
                else:
                    msg = f"Selection '{value}' is not in choices. Defaulting to first choice: '{self.choices[0]}'."
                    logger.warning(msg)
                    value = self.choices[0]
            value = self.choices_value_lookup.get(value, self.choices[0])
            msg = f"Converted choice for {self.value_field} into value: {value}"
            logger.info(msg)
            return value

        return [converter]

    def validators_for_trait(self) -> list[Callable[[Parameter, Any], Any]]:
        def validator(param: Parameter, value: Any) -> None:
            if value not in list(self.choices_value_lookup.values()):
                msg = f"Attempted to set Parameter '{param.name}' to value '{value}', but that was not one of the available choices."

                def raise_error() -> None:
                    raise ValueError(msg)

                raise_error()

        return [validator]
