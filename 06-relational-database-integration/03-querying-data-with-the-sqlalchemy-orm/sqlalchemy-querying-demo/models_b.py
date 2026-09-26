import datetime
from enum import Enum
from typing import List

from sqlalchemy import (
    CheckConstraint,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class ResponseStatus(Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    PENDING = "pending"
    TENTATIVE = "tentative"


class Base(DeclarativeBase):
    pass


class Calendar(Base):
    __tablename__ = "calendar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)

    events: Mapped[List["CalendarEvent"]] = relationship(
        back_populates="calendar",
        cascade="all",
    )


class CalendarEvent(Base):
    __tablename__ = "calendar_event"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date)
    priority: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("priority >= 1 and priority <= 10"),
        default=5,
    )
    private: Mapped[bool] = mapped_column(Boolean, default=False)

    calendar_id: Mapped[int] = mapped_column(
        ForeignKey("calendar.id", ondelete="CASCADE")
    )

    calendar: Mapped["Calendar"] = relationship(back_populates="events")

    attendees: Mapped[List["EventAttendee"]] = relationship(
        back_populates="event",
        cascade="all",
    )

    attendees_proxy: AssociationProxy = association_proxy(
        "attendees",
        "person",
        creator=lambda person: EventAttendee(person=person),
    )


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    events: Mapped[List["EventAttendee"]] = relationship(
        back_populates="person",
        cascade="all",
    )

    events_proxy: AssociationProxy = association_proxy(
        "events",
        "event",
        creator=lambda event: EventAttendee(event=event),
    )


class EventAttendee(Base):
    __tablename__ = "event_attendee"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("calendar_event.id", ondelete="CASCADE"),
        primary_key=True,
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey("person.id", ondelete="CASCADE"),
        primary_key=True,
    )

    response_status: Mapped[ResponseStatus] = mapped_column(
        SAEnum(ResponseStatus),
        default=ResponseStatus.PENDING,
        nullable=False,
    )

    event: Mapped["CalendarEvent"] = relationship(back_populates="attendees")
    person: Mapped["Person"] = relationship(back_populates="events")
