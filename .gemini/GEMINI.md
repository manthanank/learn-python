# Gemini Code Guidelines for Learn Python

- **Architecture Integrity**: Keep internal CPython inspection separated from web API layers.
- **Asyncio Standards**: Avoid blocking calls in async def routines; use `asyncio.to_thread` for blocking CPU or I/O work.
- **Error Handling**: Use custom exception hierarchies inheriting from standard Python built-ins with structured error payloads in API responses.
- **Documentation**: Write clear docstrings in Google style formatting.
