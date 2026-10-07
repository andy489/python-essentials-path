import annotationlib
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, dataclass_transform

MODEL_REGISTRY: dict[str, type["TelemetryModel"]] = {}


@dataclass(frozen=True)
class Handler:
    fn: Callable[..., None]
    dependencies: dict[str, object]


HANDLER_REGISTRY: dict[type["TelemetryModel"], Handler] = {}
DEPENDENCIES: dict[object, object] = {}


@dataclass_transform(frozen_default=False, field_specifiers=(field,))
class TelemetryModel:
    def __init_subclass__(cls, *, frozen: bool = False, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        dataclass(frozen=frozen)(cls)
        MODEL_REGISTRY[cls.__name__] = cls


def register[F: Callable[..., None]](fn: F) -> F:
    annotations: dict[str, object] = annotationlib.get_annotations(fn)
    annotations.pop("return", None)
    if not annotations:
        raise TypeError(f"{fn.__qualname__} must annotate a model parameter")
    (_, model), *dependencies = annotations.items()
    if not (isinstance(model, type) and issubclass(model, TelemetryModel)):
        raise TypeError(f"{fn.__qualname__}: first parameter must be a TelemetryModel")
    HANDLER_REGISTRY[model] = Handler(fn, dict(dependencies))
    return fn


def provide(dependency: object, instance: object) -> None:
    DEPENDENCIES[dependency] = instance


def dispatch(model: TelemetryModel) -> None:
    handler = HANDLER_REGISTRY.get(type(model))
    if handler is None:
        raise LookupError(f"no handler registered for {type(model).__name__}")
    kwargs: dict[str, object] = {}
    for name, annotation in handler.dependencies.items():
        if annotation not in DEPENDENCIES:
            raise LookupError(f"no dependency provided for {name}: {annotation}")
        kwargs[name] = DEPENDENCIES[annotation]
    handler.fn(model, **kwargs)
