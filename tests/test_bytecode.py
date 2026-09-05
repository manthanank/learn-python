"""Tests for CPython bytecode disassembly and AST metrics."""

from src.internals.bytecode_inspector import disassemble_source


def test_disassemble_simple_math():
    code = "def add(a, b):\n    return a + b\nres = add(10, 20)"
    res = disassemble_source(code)

    assert res.cyclomatic_complexity == 1
    assert "add" in res.functions_defined
    assert len(res.instructions) > 0
    assert any(inst["opname"] in ("BINARY_OP", "BINARY_ADD") for inst in res.instructions)


def test_cyclomatic_complexity_branches():
    code = """
def complex_decision(x, y):
    if x > 0 and y > 0:
        return 1
    elif x < 0 or y < 0:
        return -1
    else:
        for i in range(5):
            while x < 10:
                x += 1
    return 0
"""
    res = disassemble_source(code)
    # Decision points: if, and (+1), elif, or (+1), for (+1), while (+1) => baseline 1 + 6 = 7
    assert res.cyclomatic_complexity >= 5
    assert "complex_decision" in res.functions_defined
    assert res.ast_node_count > 10


def test_code_flags_and_constants():
    code = "x = 42\ny = 'hello'\nz = [1, 2, 3]"
    res = disassemble_source(code)
    assert 42 in res.constants
    assert "hello" in res.constants
    assert "x" in res.names
