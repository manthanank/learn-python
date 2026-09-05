"""Tests for CPython memory layout, object inspection, and generational GC."""

from src.internals.memory_model import (
    calculate_deep_size,
    get_gc_status,
    inspect_object,
    simulate_cyclic_garbage,
)


def test_deep_size_calculation():
    simple_int = 100
    assert calculate_deep_size(simple_int) > 0

    nested = {"a": [1, 2, 3], "b": {"nested_key": (4, 5, 6)}}
    deep_sz = calculate_deep_size(nested)
    assert deep_sz > 100


def test_inspect_object():
    test_obj = ["alpha", "beta", "gamma"]
    info = inspect_object(test_obj)

    assert info.type_name == "list"
    assert info.ref_count >= 1
    assert info.shallow_size_bytes > 0
    assert info.deep_size_bytes >= info.shallow_size_bytes
    assert info.memory_address.startswith("0x")


def test_gc_status_and_cyclic_collection():
    status = get_gc_status()
    assert status.is_enabled is True
    assert len(status.thresholds) == 3
    assert len(status.counts) == 3

    cycle_res = simulate_cyclic_garbage()
    assert "cycle_nodes" in cycle_res
    assert isinstance(cycle_res["unreachable_objects_collected"], int)
