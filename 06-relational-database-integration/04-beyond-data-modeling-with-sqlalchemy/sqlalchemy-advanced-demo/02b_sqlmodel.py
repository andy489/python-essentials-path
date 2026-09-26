from contextlib import asynccontextmanager
from faker import Faker
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///countdown.db"

engine = create_async_engine(DATABASE_URL, echo=True)
fake = Faker()


class CalendarEventBase(SQLModel):
    event_name: str = Field(...)
    event_date: str = Field(...)


class CalendarEvent(CalendarEventBase, table=True):
    __tablename__ = "calendar_event"

    id: int = Field(default=None, primary_key=True)


class CalendarEventRead(CalendarEventBase):
    id: int


def get_dates(num_dates: int):
    return [
        fake.date_between(start_date="today", end_date="+90d") for _ in range(num_dates)
    ]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db():
    async_session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield async_session
    finally:
        await async_session.close()


async def add_calendar_event(session: AsyncSession, name: str, date: str):
    new_event = CalendarEvent(event_name=name, event_date=date)
    session.add(new_event)
    await session.commit()


async def list_calendar_events(session: AsyncSession):
    query = select(CalendarEvent)
    events = await session.scalars(query)
    return events.all()


async def seed_data(session: AsyncSession, num_events: int = 5):
    for date in get_dates(num_events):
        await add_calendar_event(session, f"{fake.city()} Event", str(date))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    async with AsyncSession(engine) as session:
        await seed_data(session)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/events/")
async def create_event(name: str, date: str, db: AsyncSession = Depends(get_db)):
    await add_calendar_event(db, name, date)
    return {"message": "Event created successfully"}


@app.get("/events/", response_model=list[CalendarEventRead])
async def read_events(db: AsyncSession = Depends(get_db)):
    events = await list_calendar_events(db)
    return events
