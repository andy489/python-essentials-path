# Advanced Type Hinting & Annotation Management

A seven-part module on Python's type system — from precise domain modeling to annotation-driven frameworks — using the **Globomantics Telemetry Hub** as a running example.

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Thinking in Types: How Python's Type System Works](01-thinking-in-types-how-pythons-type-system-works/) | Orienting to the Globomantics domain; typing the telemetry domain precisely |
| 02 | [Mastering Generics and Callable Patterns](02-mastering-generics-and-callable-patterns/) | Generic processing pipelines; signature-preserving decorators and overloaded APIs |
| 03 | [Building Protocol-Oriented Architectures](03-building-protocol-oriented-architectures/) | Decoupling sources and sinks with `Protocol`; generic protocols and contract verification |
| 04 | [Orchestrating Annotations at Runtime](04-orchestrating-annotations-at-runtime/) | Reading annotations reliably with `get_type_hints`; building a validation engine driven by annotations |
| 05 | [Managing Annotations Across a Large Codebase](05-managing-annotations-across-a-large-codebase/) | Stubbing untyped dependencies; the strictness ratchet and API lifecycle |
| 06 | [Typing Tooling, CI, and Developer Experience](06-typing-tooling-ci-and-developer-experience/) | Typing gates in CI; testing the types themselves |
| 07 | [Designing an Annotation-Driven Framework](07-designing-an-annotation-driven-framework/) | Constraint metadata with `Annotated`; the declarative model base; annotation-driven dispatch |

## Requirements

- Python 3.10+
- [`mypy`](https://mypy.readthedocs.io/) for static type checking

```bash
pip install mypy
```
