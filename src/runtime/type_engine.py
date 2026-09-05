"""Advanced Python typing, protocols, variance inspection, and runtime structural subtyping."""

from __future__ import annotations

import typing
from typing import Any, Protocol, TypeVar, runtime_checkable

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
T_inv = TypeVar("T_inv")


@runtime_checkable
class Serializable(Protocol):
    """Structural protocol defining JSON-serializable capability."""
    def to_dict(self) -> dict[str, Any]: ...


@runtime_checkable
class Executable(Protocol):
    """Structural protocol defining callable task."""
    def execute(self) -> Any: ...


def verify_structural_subtyping(obj: Any, protocol: type) -> dict[str, Any]:
    """Validates whether an object fulfills a runtime Protocol via structural typing (duck typing)."""
    is_instance = isinstance(obj, protocol)
    required_attrs = [
        attr for attr in dir(protocol)
        if not attr.startswith("_") and callable(getattr(protocol, attr, None))
    ]
    missing_attrs = [attr for attr in required_attrs if not hasattr(obj, attr)]

    return {
        "satisfies_protocol": is_instance,
        "protocol_name": protocol.__name__,
        "target_type": type(obj).__name__,
        "required_methods": required_attrs,
        "missing_methods": missing_attrs,
    }


def inspect_type_variance(type_var: TypeVar) -> dict[str, Any]:
    """Inspects the covariance/contravariance variance of a TypeVar."""
    variance = "Invariant"
    if getattr(type_var, "__covariant__", False):
        variance = "Covariant (+T_co) [e.g. Read-Only Producers]"
    elif getattr(type_var, "__contravariant__", False):
        variance = "Contravariant (-T_contra) [e.g. Write-Only Consumers]"

    return {
        "name": type_var.__name__,
        "variance": variance,
        "bound": str(type_var.__bound__),
        "constraints": [str(c) for c in type_var.__constraints__],
    }
