"""Command line interface for Learn Python CPython internals platform."""

from __future__ import annotations

import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.internals.bytecode_inspector import disassemble_source
from src.internals.concurrency_lab import run_cpu_benchmark
from src.internals.memory_model import get_gc_status, simulate_cyclic_garbage

console = Console()


def cmd_disassemble(code: str) -> None:
    result = disassemble_source(code)
    console.print(Panel.fit(f"[bold cyan]Code Complexity:[/] {result.cyclomatic_complexity} | [bold cyan]AST Nodes:[/] {result.ast_node_count} | [bold cyan]Stack Size:[/] {result.stack_size}", title="CPython AST Metrics"))

    table = Table(title="Disassembled Bytecode Instructions")
    table.add_column("Offset", justify="right", style="cyan")
    table.add_column("Opname", style="magenta")
    table.add_column("Opcode", justify="right")
    table.add_column("Arg", justify="right")
    table.add_column("ArgVal / Repr", style="green")
    table.add_column("Adaptive", style="yellow")

    for instr in result.instructions:
        table.add_row(
            str(instr["offset"]),
            instr["opname"],
            str(instr["opcode"]),
            str(instr["arg"] or ""),
            str(instr["argval"]),
            "Yes" if instr["is_adaptive"] else "No",
        )

    console.print(table)


def cmd_gc() -> None:
    status = get_gc_status()
    table = Table(title="Generational GC Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("GC Enabled", str(status.is_enabled))
    table.add_row("Thresholds (Gen 0, 1, 2)", str(status.thresholds))
    table.add_row("Current Counts (Gen 0, 1, 2)", str(status.counts))
    table.add_row("Total Objects Tracked", str(status.total_objects_tracked))
    console.print(table)


def cmd_cycle() -> None:
    res = simulate_cyclic_garbage()
    console.print(Panel.fit(f"[bold green]Unreachable Objects Collected:[/] {res['unreachable_objects_collected']}\n[bold yellow]Initial Counts:[/] {res['initial_counts']}\n[bold cyan]Post Counts:[/] {res['post_counts']}", title="Cyclic Reference GC Collection"))


def cmd_benchmark() -> None:
    console.print("[yellow]Running CPU-bound concurrency benchmark (Single vs Thread vs Process)...[/]")
    results = run_cpu_benchmark(workers=2, iterations=100_000)
    table = Table(title="CPython Concurrency Benchmark")
    table.add_column("Paradigm", style="cyan")
    table.add_column("Workers", justify="right")
    table.add_column("Duration (s)", justify="right")
    table.add_column("Throughput (ops/s)", justify="right", style="green")
    table.add_column("GIL Impact", style="magenta")

    for r in results:
        table.add_row(r.paradigm, str(r.workers), f"{r.total_time_seconds:.4f}", f"{r.throughput_ops_per_sec:.2f}", r.gil_impact)

    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Learn Python: CPython Internals & Concurrency CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Disassemble
    dis_parser = subparsers.add_parser("dis", help="Disassemble Python source into bytecode")
    dis_parser.add_argument("code", nargs="?", default="def square(x):\n    return x * x\nres = square(10)", help="Python code snippet")

    # GC
    subparsers.add_parser("gc", help="Inspect generational GC status")
    subparsers.add_parser("cycle", help="Simulate circular reference garbage collection")
    subparsers.add_parser("benchmark", help="Run GIL & Concurrency benchmark")

    args = parser.parse_args()
    if args.command == "dis":
        cmd_disassemble(args.code)
    elif args.command == "gc":
        cmd_gc()
    elif args.command == "cycle":
        cmd_cycle()
    elif args.command == "benchmark":
        cmd_benchmark()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
