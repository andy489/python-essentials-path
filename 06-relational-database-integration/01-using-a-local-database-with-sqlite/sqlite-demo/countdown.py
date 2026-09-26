import csv
import datetime
import sqlite3
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich import box

from sqlqueries import QUERIES


DB_PATH = "countdown.db"

app = typer.Typer()
console = Console()


def check_table_exists(table_name):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        if cursor.fetchone() is None:
            console.print(
                f"[red]Table '{table_name}' does not exist. Creating it now...[/red]"
            )
            cursor.execute(QUERIES[table_name])
            cn.commit()
        cursor.close()


def get_default_event_date():
    default_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
    return default_date.strftime("%Y-%m-%d")


@app.command("add")
def add_event(
    event_name: Annotated[str, typer.Argument()],
    event_date: Annotated[str, typer.Argument(default_factory=get_default_event_date)],
    event_priority: Annotated[int, typer.Argument()] = 5,
    event_private: Annotated[bool, typer.Option("--private")] = False,
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        cursor.execute(
            """
        INSERT INTO events (event_name, event_date, priority, is_private)
        VALUES (?, ?, ?, ?)
        """,
            (event_name, event_date, event_private, event_priority),
        )
        cn.commit()
        cursor.close()
        console.print(f"[green]{event_name} added successfully![/green]")


@app.command("list")
def list_events(
    private: Annotated[bool, typer.Option("--private")] = False,
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        query = "SELECT * FROM events"
        if not private:
            query += " WHERE is_private = 0"
        query += ";"
        cursor.execute(query)
        events = cursor.fetchall()
        cursor.close()

        table = Table(
            title="Events",
            box=box.SIMPLE,
        )
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Priority", justify="right", style="blue")
        table.add_column("Private", justify="center", style="yellow")
        table.add_column("Time Remaining", justify="right")

        for event in events:
            event_date = datetime.datetime.strptime(event[2], "%Y-%m-%d").date()
            days_remaining = abs((event_date - datetime.date.today()).days)
            if days_remaining < 0:
                msg = f"[red]{days_remaining} days ago[/red]"
            elif days_remaining == 0:
                msg = "[yellow]Today[/yellow]"
            else:
                msg = f"[green]In {days_remaining} days[/green]"
            table.add_row(
                str(event[0]),
                event[1],
                event[2],
                str(event[3]),
                "Yes" if bool(event[4]) else "No",
                msg,
            )

        console.print(table)


@app.command("update")
def update_event(
    event_id: Annotated[
        int, typer.Argument(..., help="ID of the event to update (required)")
    ],
    event_name: Annotated[Optional[str], typer.Option("--name")] = None,
    event_date: Annotated[Optional[str], typer.Option("--date")] = None,
    event_priority: Annotated[Optional[int], typer.Option("--priority")] = None,
    event_private: Annotated[
        Optional[bool], typer.Option("--private", is_flag=True)
    ] = None,
    event_public: Annotated[
        Optional[bool], typer.Option("--public", is_flag=True)
    ] = None,
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        query = "UPDATE events SET "
        columns = []
        values = []
        if event_name is not None:
            columns.append("event_name = ?")
            values.append(event_name)
        if event_date is not None:
            columns.append("event_date = ?")
            values.append(event_date)
        if event_priority is not None:
            columns.append("priority = ?")
            values.append(event_priority)
        if event_private is not None:
            columns.append("is_private = ?")
            values.append(1)
        if event_public is not None:
            columns.append("is_private = ?")
            values.append(0)
        query += ", ".join(columns) + " WHERE id = ?"
        values.append(event_id)
        cursor.execute(query, values)
        cn.commit()
        cursor.close()
        console.print("[green]Event updated successfully![/green]")


@app.command("delete")
def delete_event(
    event_id: Annotated[
        int, typer.Argument(..., help="ID of the event to delete (required)")
    ],
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        result = cursor.fetchone()
        if not result:
            console.print(f"[red]No event found with ID {event_id}[/red]")
            return
        confirm = Confirm.ask(
            f"[yellow]Are you sure you want to delete the event '{result[1]}'?[/yellow]"
        )
        if not confirm:
            console.print("[yellow]Deletion cancelled.[/yellow]")
            return
        console.print(f"[red]Deleting event: {result[1]}[/red]")
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        cn.commit()
        cursor.close()


@app.command("export")
def export_events(
    filename: Annotated[str, typer.Argument()] = "events.csv",
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        event_count = 0
        cursor.execute("SELECT * FROM events;")
        events = cursor.fetchall()
        cursor.close()
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["id", "event_name", "event_date", "priority", "is_private"]
            )
            for event in events:
                writer.writerow(event)
                event_count += 1
    console.print(
        f"[bold yellow]{event_count}[/bold yellow] events exported to {filename}"
    )


@app.command("import")
def import_events(
    file_path: Annotated[str, typer.Argument()],
    skip_header: Annotated[bool, typer.Option("--skip-header")] = True,
):
    with sqlite3.connect(DB_PATH) as cn:
        cursor = cn.cursor()
        event_count = 0
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            if skip_header:
                next(reader)
            for row in reader:
                event_count += 1
                cursor.execute(
                    """
                    INSERT INTO events (id, event_name, event_date, priority, is_private)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (int(row[0]), row[1], row[2], bool(int(row[3])), int(row[4])),
                )
        cn.commit()
        cursor.close()
        console.print(
            f"[bold yellow]{event_count}[/bold yellow] events imported from {file_path}"
        )


if __name__ == "__main__":
    check_table_exists("events")
    app()
