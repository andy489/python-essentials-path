from fastapi import FastAPI
from pydantic import BaseModel

from storage import store_alert, fetch_alerts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authenticate")
async def authenticate():
    return {"result": True}


class InconsistentPhonebookAlert(BaseModel):
    size: int
    new_entry: str
    clash: str


@app.put("/alert")
async def alert(inconsistency: InconsistentPhonebookAlert):
    # BUG: Should be inconsistency.clash
    store_alert(inconsistency.clash)
    return {"result": True}


class ClashFrequencies(BaseModel):
    entries: dict[str, int]


@app.get("/clash_frequencies")
async def clash_frequencies() -> ClashFrequencies:
    recorded_clashes = fetch_alerts()
    return ClashFrequencies(entries=recorded_clashes)
