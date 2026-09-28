import dataclasses
import json
from typing import Tuple

import requests


@dataclasses.dataclass
class BadPhonebookEntryEvent:
    size: int
    new_name: str
    new_number: str
    problem: Tuple[str, str]


def event_to_alert(event):
    return {
        # BUG: should be event.size
        'size': event.size,
        'new_entry': f"{event.new_name} cannot be added with number {event.new_number}",
        'clash': f"{event.problem[0]} with number {event.problem[1]}",
    }


class InconsistentPhonebookAlerter:
    def __init__(self, url):
        # BUG: should be f"{url}/alert"
        self.url = f"{url}/alert"

    def send_alert(self, event):
        data = event_to_alert(event)
        # BUG: should be "data=json.dumps(data).encode()"
        response = requests.put(self.url, data=json.dumps(data).encode())
        if not response.status_code == 200:
            raise RuntimeError(f"could not report alert to url {self.url}")
