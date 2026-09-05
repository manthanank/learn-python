"""Concurrency & GIL benchmark comparison suite for CPython."""

from __future__ import annotations

import asyncio
import concurrent.futures
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class ConcurrencyBenchmarkResult:
    paradigm: str
    task_type: str
    workers: int
    total_time_seconds: float
    throughput_ops_per_sec: float
    gil_impact: str


def _cpu_workload(iterations: int) -> int:
    """CPU-bound task: iterative arithmetic without releasing GIL."""
    count = 0
    for i in range(iterations):
        count += (i * 31) ^ (i >> 3)
    return count


def _io_workload(duration: float) -> float:
    """I/O-bound task: releases GIL during sleep."""
    time.sleep(duration)
    return duration


async def _async_io_workload(duration: float) -> float:
    """Async I/O-bound task: non-blocking coroutine yield."""
    await asyncio.sleep(duration)
    return duration


def run_cpu_benchmark(workers: int = 4, iterations: int = 150_000) -> list[ConcurrencyBenchmarkResult]:
    """Compares Single-Thread, Multi-Threading, and Multi-Processing on CPU-bound workloads."""
    results: list[ConcurrencyBenchmarkResult] = []

    # 1. Sequential Single-Thread
    start = time.perf_counter()
    for _ in range(workers):
        _cpu_workload(iterations)
    seq_time = time.perf_counter() - start
    results.append(
        ConcurrencyBenchmarkResult(
            paradigm="Single-Thread Sequential",
            task_type="CPU-Bound",
            workers=1,
            total_time_seconds=round(seq_time, 4),
            throughput_ops_per_sec=round(workers / max(seq_time, 1e-6), 2),
            gil_impact="Baseline execution without contention",
        )
    )

    # 2. Multi-Threading (Contending on CPython GIL)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(_cpu_workload, [iterations] * workers))
    thread_time = time.perf_counter() - start
    results.append(
        ConcurrencyBenchmarkResult(
            paradigm="Multithreading (ThreadPool)",
            task_type="CPU-Bound",
            workers=workers,
            total_time_seconds=round(thread_time, 4),
            throughput_ops_per_sec=round(workers / max(thread_time, 1e-6), 2),
            gil_impact="Constrained by GIL; thread context switching overhead",
        )
    )

    # 3. Multi-Processing (Bypasses GIL via separate OS processes)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        list(executor.map(_cpu_workload, [iterations] * workers))
    proc_time = time.perf_counter() - start
    results.append(
        ConcurrencyBenchmarkResult(
            paradigm="Multiprocessing (ProcessPool)",
            task_type="CPU-Bound",
            workers=workers,
            total_time_seconds=round(proc_time, 4),
            throughput_ops_per_sec=round(workers / max(proc_time, 1e-6), 2),
            gil_impact="Bypasses GIL; true multicore CPU parallelism",
        )
    )

    return results


async def run_io_benchmark(workers: int = 10, delay: float = 0.05) -> list[ConcurrencyBenchmarkResult]:
    """Compares Multi-Threading and Asyncio on I/O-bound workloads."""
    results: list[ConcurrencyBenchmarkResult] = []

    # 1. Multi-Threading for I/O
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(_io_workload, [delay] * workers))
    thread_time = time.perf_counter() - start
    results.append(
        ConcurrencyBenchmarkResult(
            paradigm="Multithreading (ThreadPool)",
            task_type="I/O-Bound",
            workers=workers,
            total_time_seconds=round(thread_time, 4),
            throughput_ops_per_sec=round(workers / max(thread_time, 1e-6), 2),
            gil_impact="GIL released during native C system I/O wait",
        )
    )

    # 2. Asyncio Cooperative Multitasking
    start = time.perf_counter()
    await asyncio.gather(*[_async_io_workload(delay) for _ in range(workers)])
    async_time = time.perf_counter() - start
    results.append(
        ConcurrencyBenchmarkResult(
            paradigm="Asyncio Event Loop",
            task_type="I/O-Bound",
            workers=workers,
            total_time_seconds=round(async_time, 4),
            throughput_ops_per_sec=round(workers / max(async_time, 1e-6), 2),
            gil_impact="Single-threaded non-blocking multiplexing; ultra-low overhead",
        )
    )

    return results
