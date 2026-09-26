# Relational Database Integration

Hands-on notebooks covering relational database access in Python — from raw SQL with the built-in `sqlite3` module through the full SQLAlchemy ORM stack.

## Modules

| # | Module | Topics |
|---|--------|--------|
| 01 | [Using a Local Database with SQLite](01-using-a-local-database-with-sqlite/) | `sqlite3` connection lifecycle, cursors, `with` blocks, row factories, dataclasses |
| 02 | [Data Modeling with the SQLAlchemy ORM](02-data-modeling-with-the-sqlalchemy-orm/) | `create_engine`, `DeclarativeBase`, `Mapped`, `mapped_column`, constraints, one-to-many relationships |
| 03 | [Querying Data with the SQLAlchemy ORM](03-querying-data-with-the-sqlalchemy-orm/) | `Session`, `select`, `where`, `update`, `delete`, `scalars()` |
| 04 | [Beyond Data Modeling with SQLAlchemy](04-beyond-data-modeling-with-sqlalchemy/) | Transactions, rollback, database switching, Alembic migrations, async SQLAlchemy, SQLModel |

## Requirements

```bash
pip install sqlalchemy
```

For the async examples in module 04:

```bash
pip install aiosqlite
```

For the SQLModel examples in module 04:

```bash
pip install sqlmodel
```
