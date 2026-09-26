import csv
import datetime
from typing import Annotated

import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from sqlalchemy import create_engine, delete, select, update, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models_b as models


DB_PATH = "sqlite:///countdown.db"

app = typer.Typer()
calendar_app = typer.Typer()
event_app = typer.Typer()
person_app = typer.Typer()
app.add_typer(calendar_app, name="calendar")
app.add_typer(event_app, name="event")
app.add_typer(person_app, name="person")

console = Console()
engine = create_engine(DB_PATH, echo=False)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(conn, _):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@person_app.command("update-response-status")
def update_response_status(
    person_id: Annotated[int, typer.Argument()],
    event_id: Annotated[int, typer.Argument()],
    response_status: Annotated[models.ResponseStatus, typer.Argument()],
):
    with Session(engine) as session:
        query = (
            update(models.EventAttendee)
            .where(
                models.EventAttendee.event_id == event_id,
                models.EventAttendee.person_id == person_id,
            )
            .values(response_status=response_status)
        )
        session.execute(query)
        session.commit()
        console.print("Update complete", style="green")


@person_app.command("list-events-by-proxy")
def list_events_by_proxy(person_id: Annotated[int, typer.Argument()]):
    with Session(engine) as session:
        person_query = select(models.Person).where(models.Person.id == person_id)
        person = session.scalars(person_query).first()
        if not person:
            console.print("Person not found", style="red")

        table = Table(title=f"Events {person.name} is Attending")
        table.add_column("")
        table.add_column("Event Name")
        table.add_column("Event Date")

        for index, event in enumerate(person.events_proxy):
            table.add_row(
                str(index + 1),
                event.name,
                event.due_date.strftime("%Y-%m-%d"),
            )

        console.print(table)


@person_app.command("list-events")
def list_events_for_person(person_id: Annotated[int, typer.Argument()]):
    with Session(engine) as session:
        person_query = select(models.Person).where(models.Person.id == person_id)
        person = session.scalars(person_query).first()
        if not person:
            console.print("Person not found", style="red")
            return

        table = Table(title=f"Events {person.name} is Attending")
        table.add_column("")
        table.add_column("Event Name")
        table.add_column("Event Date")

        for index, event_attendee in enumerate(person.events):
            table.add_row(
                str(index + 1),
                event_attendee.event.name,
                event_attendee.event.due_date.strftime("%Y-%m-%d"),
            )

        console.print(table)


@person_app.command("attend")
def attend_event(
    person_id: Annotated[int, typer.Argument()],
    event_id: Annotated[int, typer.Argument()],
    response_status: models.ResponseStatus = models.ResponseStatus.PENDING,
):
    with Session(engine) as session:
        person_query = select(models.Person).where(models.Person.id == person_id)
        person = session.scalars(person_query).first()
        if not person:
            console.print("Person not found", style="red")
            return

        event_query = select(models.CalendarEvent).where(
            models.CalendarEvent.id == event_id
        )
        event = session.scalars(event_query).first()
        if not event:
            console.print("Event not found", style="red")
            return

        event_attendee = models.EventAttendee(
            event=event,
            person=person,
            response_status=response_status,
        )
        session.add(event_attendee)
        session.commit()
        console.print(f"{person.name} is attending {event.name}", style="green")


@person_app.command("create")
def create_person(
    name: Annotated[str, typer.Argument()],
    email: Annotated[str, typer.Argument()],
):
    with Session(engine) as session:
        person = models.Person(name=name, email=email)
        session.add(person)
        session.commit()
        console.print(f"Created person {name}", style="green")


@person_app.command("import")
def import_persons(
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
                sess.add(
                    models.Person(
                        id=int(row[0]),
                        name=row[1],
                        email=row[2],
                    )
                )
        sess.commit()
    console.print(f"{event_count} persons imported from {file_path}", style="green")


@event_app.command("move-to-calendar-id")
def move_to_calendar_id(
    event_id: Annotated[int, typer.Argument()],
    calendar_id: Annotated[int, typer.Argument()],
):
    with Session(engine) as session:
        query = select(models.CalendarEvent).where(models.CalendarEvent.id == event_id)
        event = session.scalars(query).first()
        event.calendar_id = calendar_id
        session.commit()
        console.print(f"Moved {event.name} to calendar {calendar_id}", style="green")


@event_app.command("move-to-calendar")
def move_to_calendar(
    event_id: Annotated[int, typer.Argument()],
    calendar_id: Annotated[int, typer.Argument()],
):
    with Session(engine) as session:
        query = select(models.CalendarEvent).where(models.CalendarEvent.id == event_id)
        event = session.scalars(query).first()

        query = select(models.Calendar).where(models.Calendar.id == calendar_id)
        new_calendar = session.scalars(query).first()

        event.calendar = new_calendar
        session.commit()
        console.print(f"Moved {event.name} to calendar {calendar_id}", style="green")


@event_app.command("add-by-parent-id")
def add_by_parent_id(
    calendar_id: Annotated[int, typer.Argument()],
    event_name: Annotated[str, typer.Argument()],
    event_date: Annotated[str, typer.Argument()] = None,
    priority: Annotated[int, typer.Argument()] = 5,
    private: Annotated[bool, typer.Argument()] = False,
):
    with Session(engine) as session:
        event_date_dt = (
            datetime.datetime.fromisoformat(event_date)
            if event_date
            else datetime.datetime.now().date() + datetime.timedelta(days=7)
        )

        new_event = models.CalendarEvent(
            name=event_name,
            due_date=event_date_dt,
            priority=priority,
            private=private,
            calendar_id=calendar_id,
        )
        session.add(new_event)
        session.commit()
        console.print(f"Added {event_name}", style="green")


@event_app.command("add-by-parent-directly")
def add_by_parent_directly(
    calendar_id: Annotated[int, typer.Argument()],
    event_name: Annotated[str, typer.Argument()],
    event_date: Annotated[str, typer.Argument()] = None,
    priority: Annotated[int, typer.Argument()] = 5,
    private: Annotated[bool, typer.Argument()] = False,
):
    with Session(engine) as session:
        query = select(models.Calendar).where(models.Calendar.id == calendar_id)
        calendar = session.scalars(query).first()
        if not calendar:
            console.print(f"No calendar found with ID {calendar_id}", style="red")
            return

        event_date_dt = (
            datetime.datetime.fromisoformat(event_date)
            if event_date
            else datetime.datetime.now().date() + datetime.timedelta(days=7)
        )

        new_event = models.CalendarEvent(
            name=event_name,
            due_date=event_date_dt,
            priority=priority,
            private=private,
            calendar=calendar,
        )
        session.add(new_event)
        session.commit()
        console.print(f"Added {event_name}", style="green")


@event_app.command("add-by-parent-collection")
def add_by_parent_collection(
    calendar_id: Annotated[int, typer.Argument()],
    event_name: Annotated[str, typer.Argument()],
    event_date: Annotated[str, typer.Argument()] = None,
    priority: Annotated[int, typer.Argument()] = 5,
    private: Annotated[bool, typer.Argument()] = False,
):
    with Session(engine) as session:
        query = select(models.Calendar).where(models.Calendar.id == calendar_id)
        calendar = session.scalars(query).first()
        if not calendar:
            console.print(f"No calendar found with ID {calendar_id}", style="red")
            return

        event_date_dt = (
            datetime.datetime.fromisoformat(event_date)
            if event_date
            else datetime.datetime.now().date() + datetime.timedelta(days=7)
        )
        try:
            new_event = models.CalendarEvent(
                name=event_name,
                due_date=event_date_dt,
                priority=priority,
                private=private,
            )
            calendar.events.append(new_event)
            session.add(new_event)
            session.commit()
            console.print(f"Added {event_name}", style="green")
        except IntegrityError as e:
            console.print(f"{e.orig}", style="red")


@event_app.command("list")
def list_events(
    calendar_id: Annotated[int, typer.Argument()],
):
    with Session(engine) as session:
        query = select(models.Calendar).where(models.Calendar.id == calendar_id)
        calendar = session.scalars(query).first()
        if not calendar:
            console.print(f"Calendar with {calendar_id} not found", style="red")
            return

        table = Table(title="Events")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Date")
        table.add_column("Priority")
        table.add_column("Private")

        for event in calendar.events:
            table.add_row(
                str(event.id),
                event.name,
                event.due_date.strftime("%Y-%m-%d"),
                str(event.priority),
                "Yes" if event.private else "No",
            )
        console.print(table)


@event_app.command("query")
def query_events(
    calendar_id: Annotated[int, typer.Argument()],
    min_priority: Annotated[int, typer.Argument()] = 8,
    show_private: Annotated[bool, typer.Option("--show_private")] = False,
):
    print(f"{min_priority} {show_private}")
    with Session(engine) as session:
        query = select(models.CalendarEvent).where(
            models.CalendarEvent.calendar_id == calendar_id
        )
        if not show_private:
            query = query.where(models.CalendarEvent.private == False)
        query = query.where(
            models.CalendarEvent.priority >= min_priority,
        )
        events = session.scalars(query).all()

        table = Table(title="Events")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Date")
        table.add_column("Priority")
        table.add_column("Private")

        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.due_date.strftime("%Y-%m-%d"),
                str(event.priority),
                "Yes" if event.private else "No",
            )
        console.print(table)


@event_app.command("import-attendees")
def import_attendees(
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
                sess.add(
                    models.EventAttendee(
                        event_id=int(row[0]),
                        person_id=int(row[1]),
                        response_status=models.ResponseStatus(row[2].lower()),
                    )
                )
        sess.commit()
    console.print(f"{event_count} attendees imported from {file_path}", style="green")


@event_app.command("import")
def import_events(
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
                sess.add(
                    models.CalendarEvent(
                        id=int(row[0]),
                        name=row[1],
                        due_date=datetime.datetime.strptime(row[2], "%Y-%m-%d").date(),
                        priority=int(row[3]),
                        private=bool(int(row[4])),
                        calendar_id=int(row[5]),
                    )
                )
        sess.commit()
    console.print(f"{event_count} events imported from {file_path}", style="green")


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


@calendar_app.command("import")
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
    console.print(f"{event_count} calendars imported from {file_path}", style="green")


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


if __name__ == "__main__":
    app()
