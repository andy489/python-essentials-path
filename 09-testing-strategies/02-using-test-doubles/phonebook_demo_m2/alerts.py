
import http.client
import json
from urllib.parse import urlparse

import requests


class InconsistentPhonebookAlerter:
    def __init__(self, url):
        self.url = url

    def format_event(self, event):
        return {
            # BUG: should be event.size
            'size': len(event.problem),
            'new_entry': f"{event.new_name} cannot be added with number {event.new_number}",
            'clash': f"{event.problem[0]} with number {event.problem[1]}",
        }

    def send_alert(self, event):
        data = self.format_event(event)
        # BUG: should be "data=json.dumps(data).encode()"
        response = requests.put(self.url, data=data)
        if not response.status_code == 200:
            raise RuntimeError(f"could not report alert to url {self.url}")