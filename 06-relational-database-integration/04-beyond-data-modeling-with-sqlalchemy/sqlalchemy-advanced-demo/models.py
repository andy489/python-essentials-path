from sqlmodel import SQLModel, Field, Relationship


class CalendarEvent(SQLModel, table=True):
    __tablename__ = "calendar_event"

    id: int | None = Field(default=None, primary_key=True)
    event_name: str = Field(max_length=100)
    event_date: str = Field(max_length=50)

    priority: int
    private: bool = Field(default=False)

    calendar_id: int = Field(foreign_key="calendar.id")

    calendar: "Calendar" = Relationship(back_populates="events")


class Calendar(SQLModel, table=True):
    __tablename__ = "calendar"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)

    events: list["CalendarEvent"] = Relationship(
        back_populates="calendar", cascade_delete=True
    )
