import unittest
from io import StringIO
from textwrap import dedent
from unittest.mock import create_autospec, Mock

import pytest

from alerts import InconsistentPhonebookAlerter
from authorization import SecurityClearanceAuthorizer
from enterprise import EnterprisePhonebook, BadPhonebookEntryEvent


# - lookup when authorized
# - lookup when not authorized - raise error
# - batch update phonebook entries from a file
# - don't add inconsistent entries
# - report attempts to add inconsistent entries - publish an event
# - record names that are looked up in a log file


@pytest.fixture
def stub_authorizer():
    stub = create_autospec(SecurityClearanceAuthorizer)
    stub.is_authorized = Mock(return_value=True)
    return stub


@pytest.fixture
def spy_alerter():
    spy = create_autospec(InconsistentPhonebookAlerter)
    return spy


@pytest.fixture
def enterprise_phonebook(phonebook, stub_authorizer, spy_alerter):
    return EnterprisePhonebook(phonebook, stub_authorizer, spy_alerter, Mock())


def test_alert_inconsistent_entry_attempts(enterprise_phonebook, spy_alerter):
    enterprise_phonebook.add("Bob", "12345")
    enterprise_phonebook.add("Sid", "12346")
    enterprise_phonebook.add("Ted", "1234")
    expected_calls = [
        unittest.mock.call(BadPhonebookEntryEvent(2, "Ted", "1234", ("Bob", "12345"))),
        unittest.mock.call(BadPhonebookEntryEvent(2, "Ted", "1234", ("Sid", "12346"))),
    ]
    spy_alerter.send_alert.assert_has_calls(expected_calls)


def test_do_not_add_inconsistent_entry(enterprise_phonebook):
    enterprise_phonebook.add("Bob", "12345")
    enterprise_phonebook.add("Sid", "12346")
    enterprise_phonebook.add("Ted", "1234")
    assert enterprise_phonebook.phonebook.storage == {"Bob": "12345", "Sid": "12346"}


def test_update_from_file(enterprise_phonebook):
    fake_file = StringIO(
        dedent("""\
        Name,Phone Number
        Bob,1234
        Ann,6789""")
    )
    enterprise_phonebook.add_data(fake_file)
    assert enterprise_phonebook.phonebook.storage == {"Bob": "1234", "Ann": "6789"}


def test_lookup_authorized(phonebook, stub_authorizer, enterprise_phonebook):
    phonebook.add("Bob", "1234")
    assert enterprise_phonebook.lookup("Bob") == "1234"


def test_lookup_not_authorized(phonebook, stub_authorizer, enterprise_phonebook):
    phonebook.add("Bob", "1234")
    stub_authorizer.is_authorized = Mock(return_value=False)

    with pytest.raises(RuntimeError):
        enterprise_phonebook.lookup("Bob")
