# Universal Agent Instructions for Learn Python

## Identity & Scope
`learn-python` is an architectural learning platform and reference implementation of CPython 3.11-3.13 internals, advanced concurrency patterns, metaprogramming paradigms, and production design patterns.

## Rules for Autonomous Agents
1. **Preserve Compatibility**: Ensure all examples and tests run on CPython 3.11+. Avoid 3.14-only unstable features.
2. **Quality Guarantee**: All pytest test cases must pass 100% offline with zero external network access.
3. **CPython Truth**: Make clear distinctions between standard Python language specifications and CPython runtime implementation details (such as reference counting, GIL, and arena-based memory pooling).
4. **Safety**: Interactive code execution endpoints must sanitize input and enforce execution timeouts to prevent accidental infinite loops.
