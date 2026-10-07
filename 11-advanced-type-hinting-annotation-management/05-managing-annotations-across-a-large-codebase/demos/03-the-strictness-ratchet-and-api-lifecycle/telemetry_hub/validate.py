from dataclasses import MISSING, fields, is_dataclass
from typing import Literal, NewType, TypeAliasType, Union, get_args, get_origin

from annotationlib import Format

from telemetry_hub.introspect import annotations_of


def validate_payload(model: type, payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return [f"payload: expected dict, got {type(payload).__name__}"]
    required = _required_keys(model)
    errors: list[str] = []
    for name, annotation in annotations_of(model, Format.VALUE).items():
        if name not in payload:
            if name in required:
                errors.append(f"{name}: missing required key")
            continue
        errors.extend(_check(name, payload[name], annotation))
    return errors


def _required_keys(model: type) -> set[str]:
    if not is_dataclass(model):
        return set()
    return {
        spec.name
        for spec in fields(model)
        if spec.default is MISSING and spec.default_factory is MISSING
    }


def _check(path: str, value: object, annotation: object) -> list[str]:
    if isinstance(annotation, TypeAliasType):
        return _check(path, value, annotation.__value__)
    if isinstance(annotation, NewType):
        return _check(path, value, annotation.__supertype__)
    origin = get_origin(annotation)
    if origin is Union:
        return _check_union(path, value, get_args(annotation))
    if origin is Literal:
        allowed = get_args(annotation)
        if value in allowed:
            return []
        choices = ", ".join(repr(arm) for arm in allowed)
        return [f"{path}: expected one of {choices}, got {value!r}"]
    if origin is list:
        if not isinstance(value, list):
            return [f"{path}: expected list, got {type(value).__name__}"]
        (item_annotation,) = get_args(annotation)
        errors: list[str] = []
        for index, item in enumerate(value):
            errors.extend(_check(f"{path}[{index}]", item, item_annotation))
        return errors
    if isinstance(annotation, type):
        if is_dataclass(annotation):
            if not isinstance(value, dict):
                return [
                    f"{path}: expected {annotation.__name__}, "
                    f"got {type(value).__name__}"
                ]
            nested = validate_payload(annotation, value)
            return [f"{path}.{error}" for error in nested]
        if annotation is float and type(value) is int:
            return []
        if isinstance(value, annotation):
            return []
        return [f"{path}: expected {_describe(annotation)}, got {type(value).__name__}"]
    return [f"{path}: unsupported annotation {annotation!r}"]


def _check_union(path: str, value: object, arms: tuple[object, ...]) -> list[str]:
    results = [_check(path, value, arm) for arm in arms]
    if any(not result for result in results):
        return []
    for arm, result in zip(arms, results):
        if is_dataclass(arm) and isinstance(value, dict):
            return result
    expected = " | ".join(_describe(arm) for arm in arms)
    return [f"{path}: expected {expected}, got {type(value).__name__}"]


def _describe(annotation: object) -> str:
    if annotation is type(None):
        return "None"
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation)
