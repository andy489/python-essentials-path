import logging
import os
import subprocess
import time
from pathlib import Path

import pytest

from alerts import InconsistentPhonebookAlerter
from authorization import SecurityClearanceAuthorizer
from enterprise import EnterprisePhonebook
from phonebook import Phonebook


@pytest.fixture
def enterprise_phonebook(real_authorizer, real_alerter):
    enterprise_logger = logging.Logger("Enterprise Phonebook")
    return EnterprisePhonebook(Phonebook(), real_authorizer, real_alerter, enterprise_logger)


@pytest.fixture
def real_authorizer(server_url):
    return SecurityClearanceAuthorizer(server_url)


@pytest.fixture
def real_alerter(server_url, auth_service_code_folder):
    alert_filepath = auth_service_code_folder / "alert_log.txt"
    if os.path.exists(alert_filepath):
        os.remove(alert_filepath)

    return InconsistentPhonebookAlerter(server_url)


@pytest.fixture
def server_url():
    return f"http://{server_host()}:{server_port()}"


def server_host():
    return "127.0.0.1"


def server_port():
    return "8000"


@pytest.fixture(autouse=True, scope="session")
def auth_alert_server(auth_service_code_folder):
    cmd = [
        ".venv/bin/fastapi",
        "run",
        "--host", server_host(),
        "--port", server_port(),
    ]
    server_process = subprocess.Popen(
        cmd,
        cwd=str(auth_service_code_folder),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    wait_for_server_to_start(server_process)

    yield server_process

    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()


@pytest.fixture(scope="session")
def auth_service_code_folder():
    return Path(__file__).parent / ".." / ".." / ".." / "AuthAndAlertService"


def wait_for_server_to_start(server_process):
    expected_text = "Application startup complete"
    deadline = time.time() + 500
    captured = []
    while not time.time() > deadline:
        line = server_process.stdout.readline()
        captured.append(line)
        if expected_text in line:
            return
    raise RuntimeError("Timeout before server startup completed.\nOutput:\n" +
                       "\n".join(captured))
