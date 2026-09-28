import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import pytest


class MockHandler(BaseHTTPRequestHandler):
    response_code = 200
    message = "OK"
    latest_request_type = None
    latest_request_body = None

    @staticmethod
    def reset():
        MockHandler.response_code = 200
        MockHandler.message = "OK"
        MockHandler.latest_request_type = None
        MockHandler.latest_request_body = None

    def do_GET(self):
        MockHandler.latest_request_type = "GET"
        if MockHandler.response_code == 200:
            self.send_response(200, message=MockHandler.message)
            self.end_headers()
        else:
            self.send_error(MockHandler.response_code, message=MockHandler.message)

    def do_PUT(self):
        MockHandler.latest_request_type = "PUT"
        length = int(self.headers['content-length'])
        MockHandler.latest_request_body = self.rfile.read(length)
        if MockHandler.response_code == 200:
            self.send_response(200, message=MockHandler.message)
            self.end_headers()
        else:
            self.send_error(MockHandler.response_code, message=MockHandler.message)


@pytest.fixture
def endpoint_handler():
    yield MockHandler
    MockHandler.reset()


@pytest.fixture
def host():
    return '127.0.0.1'


@pytest.fixture
def port():
    return 9998

@pytest.fixture
def url(host, port):
    return f"http://{host}:{port}"

@pytest.fixture(autouse=True)
def http_server(host, port, endpoint_handler):
    httpd = ThreadingHTTPServer((host, port), endpoint_handler)
    server_thread = threading.Thread(target=lambda: httpd.serve_forever(poll_interval=0.01))
    server_thread.start()

    yield httpd

    httpd.shutdown()
    httpd.server_close()
    server_thread.join()