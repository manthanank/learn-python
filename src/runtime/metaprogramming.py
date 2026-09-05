"""Metaprogramming, Descriptor protocol, Metaclasses, and C3 Linearization."""

from __future__ import annotations

from typing import Any


class ValidatedField:
    """A robust data descriptor enforcing type and bounds validation with __set_name__."""

    def __init__(self, expected_type: type, min_value: float | None = None, max_value: float | None = None) -> None:
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value
        self.storage_name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_field_{name}"

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Field '{self.storage_name[7:]}' must be of type {self.expected_type.__name__}, got {type(value).__name__}"
            )
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Field '{self.storage_name[7:]}' must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Field '{self.storage_name[7:]}' must be <= {self.max_value}")
        setattr(instance, self.storage_name, value)

    def __delete__(self, instance: Any) -> None:
        if hasattr(instance, self.storage_name):
            delattr(instance, self.storage_name)


class RegistryMeta(type):
    """Metaclass that automatically catalogs subclasses into an internal registry."""

    _registry: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        # Avoid registering abstract base
        if name != "BasePlugin":
            mcs._registry[name] = cls
        return cls

    @classmethod
    def get_registered_plugins(mcs) -> dict[str, type]:
        return dict(mcs._registry)


class BasePlugin(metaclass=RegistryMeta):
    """Abstract base class using RegistryMeta for auto-discovery."""
    pass


class SubclassRegistryBase:
    """Modern Python 3.6+ alternative to metaclasses via __init_subclass__."""
    _subclasses: list[type] = []

    def __init_subclass__(cls, category: str = "default", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.category = category  # type: ignore[attr-defined]
        cls._subclasses.append(cls)

    @classmethod
    def get_subclasses(cls) -> list[type]:
        return list(cls._subclasses)


def calculate_mro_c3(cls: type) -> list[str]:
    """Inspects the C3 Linearization Method Resolution Order (MRO) for a given class."""
    return [c.__name__ for c in cls.__mro__]
