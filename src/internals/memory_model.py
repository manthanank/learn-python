"""CPython memory model, object layout, reference counting, and generational GC inspector."""

from __future__ import annotations

import gc
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class PyObjectInspection:
    """Anatomy and memory footprint of a CPython PyObject."""
    memory_address: str
    type_name: str
    ref_count: int
    shallow_size_bytes: int
    deep_size_bytes: int
    is_gc_tracked: bool
    pyobject_header_size: int  # Typically 16 bytes on 64-bit: 8 bytes ob_refcnt + 8 bytes ob_type


@dataclass
class GCStatus:
    """Current state of CPython generational garbage collector."""
    is_enabled: bool
    thresholds: tuple[int, int, int]
    counts: tuple[int, int, int]
    total_objects_tracked: int


def calculate_deep_size(obj: Any, seen: set[int] | None = None) -> int:
    """Recursively computes the true memory size of a Python object including nested references."""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(calculate_deep_size(k, seen) + calculate_deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(calculate_deep_size(item, seen) for item in obj)
    elif hasattr(obj, "__dict__"):
        size += calculate_deep_size(getattr(obj, "__dict__"), seen)
    elif hasattr(obj, "__slots__"):
        slots = getattr(obj, "__slots__")
        if isinstance(slots, str):
            slots = [slots]
        for slot in slots:
            if hasattr(obj, slot):
                size += calculate_deep_size(getattr(obj, slot), seen)

    return size


def inspect_object(obj: Any) -> PyObjectInspection:
    """Inspects the runtime CPython representation of any Python object."""
    ref_count = sys.getrefcount(obj) - 1  # Subtract getrefcount temporary argument ref
    return PyObjectInspection(
        memory_address=hex(id(obj)),
        type_name=type(obj).__qualname__,
        ref_count=ref_count,
        shallow_size_bytes=sys.getsizeof(obj),
        deep_size_bytes=calculate_deep_size(obj),
        is_gc_tracked=gc.is_tracked(obj),
        pyobject_header_size=16 if sys.maxsize > 2**32 else 8,
    )


def get_gc_status() -> GCStatus:
    """Returns generational GC metrics and thresholds."""
    return GCStatus(
        is_enabled=gc.isenabled(),
        thresholds=gc.get_threshold(),
        counts=gc.get_count(),
        total_objects_tracked=len(gc.get_objects()),
    )


def simulate_cyclic_garbage() -> dict[str, Any]:
    """Demonstrates cyclic reference creation and generational GC collection."""
    gc.collect()  # Clean baseline
    initial_counts = gc.get_count()

    # Create cyclic reference
    node_a: list[Any] = [1, 2, 3]
    node_b: list[Any] = [4, 5, 6]
    node_a.append(node_b)
    node_b.append(node_a)

    id_a = hex(id(node_a))
    id_b = hex(id(node_b))

    # Sever external references
    del node_a
    del node_b

    # Run collection and collect stats
    unreachable_collected = gc.collect()
    post_counts = gc.get_count()

    return {
        "cycle_nodes": [id_a, id_b],
        "initial_counts": initial_counts,
        "post_counts": post_counts,
        "unreachable_objects_collected": unreachable_collected,
        "mechanism": "Generational Tracing Collector (Gen 0/1/2)",
    }
