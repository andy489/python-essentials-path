from dataclasses import dataclass, field
from typing import Any, dataclass_transform

MODEL_REGISTRY: dict[str, type["TelemetryModel"]] = {}


@dataclass_transform(frozen_default=False, field_specifiers=(field,))
class TelemetryModel:
    def __init_subclass__(cls, *, frozen: bool = False, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        dataclass(frozen=frozen)(cls)
        MODEL_REGISTRY[cls.__name__] = cls
