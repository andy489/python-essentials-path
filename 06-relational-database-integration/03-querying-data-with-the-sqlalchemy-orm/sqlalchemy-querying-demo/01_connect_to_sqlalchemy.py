import csv
from typing import Annotated

import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.text import Text

from sqlalchemy import create_engine

from sqlalchemy.orm import Session

import models_b as models


DB_PATH = "sqlite:///countdown.db"

app = typer.Typer()
console = Console()
engine = create_engine(DB_PATH, echo=False)


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
