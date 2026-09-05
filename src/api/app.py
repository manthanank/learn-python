"""FastAPI web platform providing CPython internals exploration and interactive runtime execution."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.internals.bytecode_inspector import disassemble_source
from src.internals.concurrency_lab import run_cpu_benchmark, run_io_benchmark
from src.internals.memory_model import get_gc_status, inspect_object, simulate_cyclic_garbage
from src.runtime.event_loop import MicroEventLoop
from src.runtime.metaprogramming import calculate_mro_c3
from src.runtime.type_engine import Serializable, verify_structural_subtyping

app = FastAPI(
    title="Learn Python Enterprise Platform",
    description="CPython Internals, Bytecode Disassembler, Concurrency Lab, and Metaprogramming Sandbox",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_DIR = Path(__file__).resolve().parent.parent.parent / "public"


class CodeDisassembleRequest(BaseModel):
    code: str = Field(..., description="Python source code to compile and disassemble")


class CodeExecuteRequest(BaseModel):
    code: str = Field(..., description="Python code to safely evaluate in sandbox")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": "2.0.0", "python": sys.version}


@app.post("/api/bytecode/disassemble")
def api_disassemble(req: CodeDisassembleRequest) -> dict[str, Any]:
    try:
        result = disassemble_source(req.code)
        return {
            "success": True,
            "instructions": result.instructions,
            "constants": result.constants,
            "varnames": result.varnames,
            "names": result.names,
            "stack_size": result.stack_size,
            "flags": result.flags,
            "ast_node_count": result.ast_node_count,
            "cyclomatic_complexity": result.cyclomatic_complexity,
            "functions_defined": result.functions_defined,
            "classes_defined": result.classes_defined,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Compilation/Disassembly Error: {exc}") from exc


@app.get("/api/memory/gc")
def api_gc_status() -> dict[str, Any]:
    status = get_gc_status()
    return {
        "is_enabled": status.is_enabled,
        "thresholds": status.thresholds,
        "counts": status.counts,
        "total_objects_tracked": status.total_objects_tracked,
    }


@app.post("/api/memory/cyclic-garbage")
def api_cyclic_garbage() -> dict[str, Any]:
    return simulate_cyclic_garbage()


@app.get("/api/concurrency/benchmark")
async def api_concurrency_benchmark() -> dict[str, Any]:
    cpu_results = run_cpu_benchmark(workers=2, iterations=80_000)
    io_results = await run_io_benchmark(workers=4, delay=0.02)
    return {
        "cpu_benchmarks": [r.__dict__ for r in cpu_results],
        "io_benchmarks": [r.__dict__ for r in io_results],
    }


@app.post("/api/runtime/eventloop-demo")
def api_eventloop_demo() -> dict[str, Any]:
    loop = MicroEventLoop()

    def task_generator(name: str, steps: int):
        for i in range(steps):
            yield f"{name} step {i+1}/{steps}"
        return f"{name} completed"

    loop.create_task(task_generator("Worker-A", 3), "Worker-A")
    loop.create_task(task_generator("Worker-B", 2), "Worker-B")
    loop.call_later(0.01, lambda: None)

    summary = loop.run_until_complete(max_ticks=50)
    return summary


@app.get("/api/runtime/mro")
def api_mro_demo() -> dict[str, Any]:
    class O: pass
    class A(O): pass
    class B(O): pass
    class C(O): pass
    class D(O): pass
    class E(O): pass
    class K1(A, B, C): pass
    class K2(D, B, E): pass
    class K3(D, A): pass
    class Z(K1, K2, K3): pass

    return {
        "class_name": "Z(K1, K2, K3)",
        "linearization_order": calculate_mro_c3(Z),
        "algorithm": "C3 Superclass Linearization (PEP 275)",
    }


@app.post("/api/sandbox/execute")
def api_execute(req: CodeExecuteRequest) -> dict[str, Any]:
    # Guard against destructive or network operations in sandbox
    forbidden = ["os.system", "subprocess", "shutil.rmtree", "__import__('os')", "open("]
    for word in forbidden:
        if word in req.code:
            raise HTTPException(status_code=400, detail=f"Execution blocked: prohibited call '{word}'")

    buffer = io.StringIO()
    globals_env: dict[str, Any] = {"__builtins__": __builtins__}
    locals_env: dict[str, Any] = {}

    try:
        with redirect_stdout(buffer):
            exec(req.code, globals_env, locals_env)
        output = buffer.getvalue()
        return {
            "success": True,
            "stdout": output,
            "variables": {
                k: str(v) for k, v in locals_env.items()
                if not k.startswith("_") and not callable(v)
            },
        }
    except Exception as exc:
        return {"success": False, "stdout": buffer.getvalue(), "error": f"{type(exc).__name__}: {exc}"}


# Mount static assets if public directory exists
if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")

    @app.get("/")
    def serve_root() -> FileResponse:
        index_file = PUBLIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"message": "Learn Python 2.0.0 API Online"})
