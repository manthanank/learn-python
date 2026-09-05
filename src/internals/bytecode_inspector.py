"""Bytecode and AST inspection engine for CPython 3.11-3.13."""

from __future__ import annotations

import ast
import dis
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class BytecodeInstruction:
    """Represents a single disassembled CPython bytecode instruction."""
    opname: str
    opcode: int
    arg: int | None
    argval: Any
    argrepr: str
    offset: int
    starts_line: int | None
    is_jump_target: bool
    is_adaptive: bool


@dataclass
class CodeAnalysisResult:
    """Complete analysis output for a Python code block."""
    instructions: list[dict[str, Any]]
    constants: list[Any]
    varnames: list[str]
    names: list[str]
    stack_size: int
    flags: list[str]
    ast_node_count: int
    cyclomatic_complexity: int
    functions_defined: list[str]
    classes_defined: list[str]


class ComplexityVisitor(ast.NodeVisitor):
    """Calculates McCabe Cyclomatic Complexity by visiting decision points."""

    def __init__(self) -> None:
        self.complexity: int = 1

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.complexity += len(node.cases)
        self.generic_visit(node)


def disassemble_source(code_str: str) -> CodeAnalysisResult:
    """Disassembles Python source code into instructions and computes AST complexity."""
    compiled = compile(code_str, "<sandbox>", "exec")
    tree = ast.parse(code_str)

    # Calculate complexity
    complexity_visitor = ComplexityVisitor()
    complexity_visitor.visit(tree)

    # AST metrics
    node_count = sum(1 for _ in ast.walk(tree))
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    # Disassemble bytecode recursively
    instructions: list[dict[str, Any]] = []
    adaptive_prefixes = ("CACHE", "RESUME", "LOAD_GLOBAL_", "BINARY_OP_", "COMPARE_OP_")

    def collect_instructions(co: Any) -> None:
        for instr in dis.get_instructions(co):
            is_adaptive = any(instr.opname.startswith(p) for p in adaptive_prefixes)
            inst_dto = BytecodeInstruction(
                opname=instr.opname,
                opcode=instr.opcode,
                arg=instr.arg,
                argval=str(instr.argval) if not isinstance(instr.argval, (int, float, bool, str, type(None))) else instr.argval,
                argrepr=instr.argrepr,
                offset=instr.offset,
                starts_line=instr.starts_line,
                is_jump_target=instr.is_jump_target,
                is_adaptive=is_adaptive,
            )
            instructions.append(asdict(inst_dto))

        for const in getattr(co, "co_consts", ()):
            if hasattr(const, "co_code"):
                collect_instructions(const)

    collect_instructions(compiled)

    code_flags: list[str] = []
    flags_val = compiled.co_flags
    flag_names = {
        0x0001: "OPTIMIZED",
        0x0002: "NEWLOCALS",
        0x0004: "VARARGS",
        0x0008: "VARKEYWORDS",
        0x0010: "NESTED",
        0x0020: "GENERATOR",
        0x0080: "COROUTINE",
        0x0100: "ITERABLE_COROUTINE",
        0x0200: "ASYNC_GENERATOR",
    }
    for flag_bit, name in flag_names.items():
        if flags_val & flag_bit:
            code_flags.append(name)

    safe_constants = [
        str(c) if not isinstance(c, (int, float, bool, str, type(None))) else c
        for c in compiled.co_consts
    ]

    return CodeAnalysisResult(
        instructions=instructions,
        constants=safe_constants,
        varnames=list(compiled.co_varnames),
        names=list(compiled.co_names),
        stack_size=compiled.co_stacksize,
        flags=code_flags,
        ast_node_count=node_count,
        cyclomatic_complexity=complexity_visitor.complexity,
        functions_defined=funcs,
        classes_defined=classes,
    )
