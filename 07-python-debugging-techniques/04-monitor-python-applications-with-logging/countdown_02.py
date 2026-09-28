import datetime
import logging

TODAY = datetime.datetime(2025, 4, 1)  # for reproducibility
DAY_SECONDS = 86400
HOUR_SECONDS = 3600
MINUTE_SECONDS = 60

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

error_logger = logging.getLogger("error_logger")
info_logger = logging.getLogger("info_logger")

error_logger.setLevel(logging.ERROR)
info_logger.setLevel(logging.INFO)

info_formatter = logging.Formatter("%(levelname)s - %(message)s")
error_formatter = logging.Formatter("%(asctime)s - %(message)s")

file_handler = logging.FileHandler("errors.log")
file_handler.setFormatter(error_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(info_formatter)

info_logger.addHandler(stream_handler)
error_logger.addHandler(file_handler)


class InvalidPrecisionError(Exception):
    def __init__(self, message, precision):
        self.message = message
        self.precision = precision
        super().__init__(message)


class CountdownEvent:
    def __init__(self, name, dt=None, priority=5):
        self.name = name
        self.priority = priority
        if dt is None:
            self.dt = TODAY + datetime.timedelta(days=7)
        else:
            self.dt = dt

    def __str__(self):
        return f"{self.name} on {self.dt.strftime('%B %d, %Y')}"

    def __repr__(self):
        return f"{self.name} on {self.dt.strftime('%B %d, %Y')}"

    def time_remaining(self, precision="days", from_date=TODAY):
        delta = self.dt - from_date
        seconds = delta.total_seconds()
        days = delta.days
        if precision == "days":
            return {"days": days}
        elif precision == "hours":
            hours = int((seconds - (days * DAY_SECONDS)) // HOUR_SECONDS)
            return {"days": days, "hours": hours}
        elif precision == "minutes":
            hours = int((seconds - (days * DAY_SECONDS)) // HOUR_SECONDS)
            minutes = int(
                (seconds - (days * DAY_SECONDS) - (hours * HOUR_SECONDS))
                // MINUTE_SECONDS
            )
            return {"days": days, "hours": hours, "minutes": minutes}
        else:
            raise InvalidPrecisionError(
                f"'{precision}' is not a valid precision. (only 'days', 'hours' and 'minutes' are supported)",
                precision=precision,
            )


class CountdownApp:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        info_logger.info("New event (%s) added to the 'database'", event.name)
        self.events.append(event)

    def get_event(self, idx):
        if idx < 0 or idx >= len(self.events):
            error_logger.error(
                "Index must be between 0 and %d inclusive",
                len(self.events) - 1,
            )
            return None
        return self.events[idx]

    def list_events(self):
        for event in self.events:
            time_left = event.time_remaining()
            event_name = event.name
            print(f"{event_name} is in {time_left['days']} days")

    def prioritize_events(self, minimum=1, maximum=10):
        for event in self.events:
            if event.priority >= minimum and event.priority <= maximum:
                print(f"{event.name} - {event.priority}")


if __name__ == "__main__":
    event_1 = CountdownEvent("My First Event")
    event_2 = CountdownEvent(
        "My Other Event", dt=datetime.datetime(2025, 5, 1, 12, 0, 0)
    )
    app = CountdownApp()
    app.add_event(event_1)
    app.add_event(event_2)
    app.add_event(CountdownEvent("My Third Event"))
    app.add_event(CountdownEvent("My Fourth Event"))
    app.list_events()

    print(app.get_event(100))

    try:
        tr = event_1.time_remaining(precision="seconds")
        print(f"Time remaining {tr['seconds']}")
    except InvalidPrecisionError as e:
        error_logger.exception("Invalid precision of %s", e.precision)
