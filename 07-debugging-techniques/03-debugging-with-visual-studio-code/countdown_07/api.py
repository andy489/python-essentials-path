import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from countdown import CountdownEvent


app = FastAPI()

db = [
    CountdownEvent("My First Event"),
]


class CountdownEventSchema(BaseModel):
    name: str = Field(..., description="The name of the event")
    dt: datetime.datetime = Field(..., description="The date of the event")
    priority: int = Field(..., description="The priority of the event")


@app.post("/add_event")
def add_event(event: CountdownEventSchema):
    new_event = CountdownEvent(
        name=event.name,
        dt=event.dt,
        priority=event.priority,
    )
    db.append(new_event)
    return {"event": new_event}


@app.get("/list_events/{precision}")
def list_events(precision):
    events = []
    for event in db:
        tr = event.time_remaining(precision)
        event_data = {"name": event.name, "days": tr["days"]}
        if precision == "hours":
            event_data["hours"] = tr["hours"]
        if precision == "minutes":
            event_data["minutes"] = tr["minutes"]
        events.append(event_data)
    return events
