# Claude Development Guidelines for Learn Python

## Project Architecture
`learn-python` is an enterprise-grade Python 3.11-3.13 platform and architectural curriculum:
- `src/internals/`: CPython bytecode disassembler, memory allocation & GC explorer, GIL & concurrency benchmarks.
- `src/runtime/`: Custom micro-coroutine event loop scheduler, descriptor & metaclass systems, type validation.
- `src/patterns/`: Enterprise design patterns (Dependency Injection, Observer, Pipeline, Registry).
- `src/api/`: FastAPI REST endpoints and interactive playground router.
- `public/`: Dark-mode glassmorphic single-page visualizer dashboard.
- `tests/`: Pytest test suite covering 100% of core modules.

## Commands
- Run Tests: `pytest` or `pytest -v --cov=src`
- Start Web Server: `uvicorn src.api.app:app --reload --port 8000`
- Run CLI: `python -m src.cli --help`
- Lint Code: `ruff check .`

## Style Conventions
- Strict type hinting using `typing` and standard generic aliases (PEP 585 & 604).
- Adhere to PEP 8, snake_case for functions/variables, PascalCase for classes.
- Use async/await idiomatically with cancellation handling.
