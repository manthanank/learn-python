"""Tests for event loop, descriptors, metaclasses, and structural typing."""

import pytest

from src.runtime.event_loop import MicroEventLoop
from src.runtime.metaprogramming import (
    BasePlugin,
    RegistryMeta,
    SubclassRegistryBase,
    ValidatedField,
    calculate_mro_c3,
)
from src.runtime.type_engine import (
    Serializable,
    T_co,
    T_contra,
    inspect_type_variance,
    verify_structural_subtyping,
)


def test_validated_field_descriptor():
    class UserAccount:
        age = ValidatedField(expected_type=int, min_value=0, max_value=120)

    user = UserAccount()
    user.age = 25
    assert user.age == 25

    with pytest.raises(TypeError):
        user.age = "not-an-int"  # type: ignore

    with pytest.raises(ValueError):
        user.age = 150


def test_metaclass_and_init_subclass():
    class CustomAuthPlugin(BasePlugin):
        pass

    plugins = RegistryMeta.get_registered_plugins()
    assert "CustomAuthPlugin" in plugins

    class WorkerPlugin(SubclassRegistryBase, category="compute"):
        pass

    subclasses = SubclassRegistryBase.get_subclasses()
    assert WorkerPlugin in subclasses
    assert WorkerPlugin.category == "compute"


def test_c3_linearization():
    class X: pass
    class Y(X): pass
    class Z(Y): pass

    mro = calculate_mro_c3(Z)
    assert mro == ["Z", "Y", "X", "object"]


def test_micro_event_loop():
    loop = MicroEventLoop()
    results = []

    def task_a():
        results.append("A1")
        yield
        results.append("A2")

    def task_b():
        results.append("B1")
        yield
        results.append("B2")

    loop.create_task(task_a(), "A")
    loop.create_task(task_b(), "B")
    stats = loop.run_until_complete(max_ticks=20)

    assert stats["total_ticks"] > 0
    assert results == ["A1", "B1", "A2", "B2"]


def test_structural_subtyping_and_variance():
    class ValidReport:
        def to_dict(self):
            return {"title": "Annual Report"}

    class InvalidReport:
        pass

    valid_res = verify_structural_subtyping(ValidReport(), Serializable)
    assert valid_res["satisfies_protocol"] is True

    invalid_res = verify_structural_subtyping(InvalidReport(), Serializable)
    assert invalid_res["satisfies_protocol"] is False
    assert "to_dict" in invalid_res["missing_methods"]

    v_co = inspect_type_variance(T_co)
    assert "Covariant" in v_co["variance"]
    v_contra = inspect_type_variance(T_contra)
    assert "Contravariant" in v_contra["variance"]
