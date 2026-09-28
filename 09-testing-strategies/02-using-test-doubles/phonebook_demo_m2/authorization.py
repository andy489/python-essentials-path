import requests

class SecurityClearanceAuthorizer:

    def __init__(self, url):
        self.url = url

    def is_authorized(self):
        request = requests.get(self.url)
        # BUG: should be "request.status_code == 200"
        return not request.status_code == 403
