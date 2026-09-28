import datetime

TODAY = datetime.datetime(2025, 4, 1)  # for reproducibility
DAY_SECONDS = 86400
HOUR_SECONDS = 3600
MINUTE_SECONDS = 60


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
                "Valid precisions are 'days', 'hours' and 'minutes' (default is 'days')",
                precision=precision,
            )
