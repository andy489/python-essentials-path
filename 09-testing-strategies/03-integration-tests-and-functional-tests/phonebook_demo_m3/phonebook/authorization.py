import requests

class SecurityClearanceAuthorizer:

    def __init__(self, url):
        self.url = url

    def is_authorized(self):
        request = requests.get(f"{self.url}/authenticate")
        # BUG: should be "request.status_code == 200"
        return request.status_code == 200
