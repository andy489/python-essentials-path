import csv
from typing import Annotated

import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text


from sqlalchemy import create_engine, delete, select, update

from sqlalchemy.orm import Session

import models_b as models


DB_PATH = "sqlite:///countdown.db"

app = typer.Typer()
calendar_app = typer.Typer()
app.add_typer(calendar_app, name="calendar")

console = Console()
engine = create_engine(DB_PATH, echo=False)


@calendar_app.command("add")
def add_calendar(name: Annotated[str, typer.Argument()]):
    with Session(engine) as session:
        new_calendar = models.Calendar(name=name)
        session.add(new_calendar)
        session.commit()
        console.print(f"Added calendar {name}", style="green")


@calendar_app.command("list")
def list_calendars():
    with Session(engine) as session:
        query = select(models.Calendar)
        calendars = session.scalars(query).all()
        if not calendars:
            console.print("No calendars found", style="yellow")
            return

    table = Table(title="Calendars")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    for calendar in calendars:
        table.add_row(str(calendar.id), calendar.name)
    console.print(table)


@calendar_app.command("update")
def update_calendar(
    calendar_id: Annotated[int, typer.Argument()],
    new_name: Annotated[str, typer.Argument()],
):
    with Session(engine) as session:
        query = (
            update(models.Calendar)
            .where(models.Calendar.id == calendar_id)
            .values(name=new_name)
        )
        result = session.execute(query)
        session.commit()
        if result.rowcount > 0:
            console.print(
                f"Updated calendar ID {calendar_id} to new name '{new_name}'",
                style="green",
            )
        else:
            console.print(f"No calendar found with ID {calendar_id}", style="red")


@calendar_app.command("delete")
def delete_calendar(calendar_id: Annotated[int, typer.Argument()]):
    with Session(engine) as session:
        query = delete(models.Calendar).where(models.Calendar.id == calendar_id)
        result = session.execute(query)
        session.commit()
        if result.rowcount > 0:
            console.print(f"Deleted calendar ID {calendar_id}", style="green")
        else:
            console.print(f"No calendar found with ID {calendar_id}", style="red")


@app.command()
def init_db():
    models.Base.metadata.create_all(bind=engine)
    console.print("Database tables created.", style="green")


@app.command()
def drop_db():
    console.print("This will delete ALL tables.", style="yellow")
    if Confirm.ask(Text("Are you sure?", style="yellow"), default=False):
        models.Base.metadata.drop_all(bind=engine)
        console.print("Database tables deleted.", style="red")


@app.command("import-calendars")
def import_calendars(
    file_path: Annotated[str, typer.Argument()],
    skip_header: Annotated[bool, typer.Option("--skip-header")] = True,
):
    event_count = 0
    with Session(engine) as sess:
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            if skip_header:
                next(reader)
            for row in reader:
                event_count += 1
                sess.add(models.Calendar(id=int(row[0]), name=row[1]))
        sess.commit()
    console.print("f{event_count} calendars imported from {file_path}")


if __name__ == "__main__":
    app()
