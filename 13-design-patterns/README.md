# Design Patterns

A series of Jupyter notebooks covering the classic Gang of Four design patterns in Python, with before/after demos for each.

## Creational Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 02 | [Factory & Abstract Factory](02-creational-patterns-factory-and-abstract-factory/) | Decouple object creation from usage so client code never calls constructors directly |
| 03 | [Builder](03-creational-patterns-builder/) | Separate the construction of a complex object from its representation |
| 04 | [Prototype](04-creational-patterns-prototype/) | Create new objects by cloning an existing instance |
| 05 | [Singleton](05-creational-patterns-singleton/) | Ensure a class has only one instance and provide a global point of access |

## Structural Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 06 | [Adapter](06-structural-patterns-adapter/) | Convert the interface of a class into another interface that clients expect |
| 07 | [Bridge](07-structural-patterns-bridge/) | Decouple an abstraction from its implementation so the two can vary independently |
| 08 | [Composite](08-structural-patterns-composite/) | Compose objects into tree structures to represent part-whole hierarchies |
| 09 | [Decorator](09-structural-patterns-decorator/) | Attach additional responsibilities to an object dynamically at runtime |
| 10 | [Facade](10-structural-patterns-facade/) | Provide a simplified interface to a complex subsystem |
| 11 | [Flyweight](11-structural-patterns-flyweight/) | Minimise memory use by sharing data between many similar objects |
| 12 | [Proxy](12-structural-patterns-proxy/) | Provide a surrogate or placeholder for another object to control access to it |

## Behavioral Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 13 | [Strategy](13-behavioral-patterns-strategy/) | Define a family of algorithms, encapsulate each one, and make them interchangeable |
| 14 | [Command](14-behavioral-patterns-command/) | Encapsulate a request as an object, enabling undo, queuing, and logging |
| 15 | [State](15-behavioral-patterns-state/) | Allow an object to alter its behaviour when its internal state changes |
| 16 | [Observer](16-behavioral-patterns-observer/) | Define a one-to-many dependency so dependents update automatically on state change |
| 17 | [Visitor](17-behavioral-patterns-visitor/) | Add new operations to an object structure without modifying its classes |
| 18 | [Chain of Responsibility](18-behavioral-patterns-chain-of-responsibility/) | Pass a request along a chain of handlers, each deciding to handle or forward it |
| 19 | [Mediator](19-behavioral-patterns-mediator/) | Encapsulate how a set of objects interact, reducing direct dependencies between them |
| 20 | [Memento](20-behavioral-patterns-memento/) | Capture and externalise an object's internal state so it can be restored later |
| 21 | [Null Object](21-behavioral-patterns-null/) | Provide a default object with do-nothing behaviour to eliminate null checks |
| 22 | [Template Method](22-behavioral-patterns-template/) | Define the skeleton of an algorithm in a base class, deferring steps to subclasses |
| 23 | [Iterator](23-behavioral-patterns-iterator/) | Sequentially access elements of a collection without exposing its representation |
| 24 | [Interpreter](24-behavioral-patterns-interpreter/) | Define a grammar for a language and provide an interpreter to deal with that grammar |

## Requirements

- Python 3.8+
- Jupyter Notebook or JupyterLab

```bash
pip install notebook
jupyter notebook
```
