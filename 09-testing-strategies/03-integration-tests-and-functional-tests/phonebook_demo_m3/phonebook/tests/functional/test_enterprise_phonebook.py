import pytest
import requests

from enterprise import EnterprisePhonebook


@pytest.mark.slow
def test_add_entry_and_lookup_successfully(enterprise_phonebook: EnterprisePhonebook):
    """
    Add an entry and look it up successfully

    Given an empty phonebook, and I am an authorized user
    When I add an entry: 'Bob', '1234'
    Then I can look up 'Bob' and get '1234'
    """
    enterprise_phonebook.add('Bob', '1234')
    result = enterprise_phonebook.lookup('Bob')
    assert result == '1234'


@pytest.mark.slow
def test_trigger_an_alert(enterprise_phonebook: EnterprisePhonebook, server_url):
    """
    Trigger an alert and ensure it is recorded

    Given a phonebook with one entry, 'Bob', '1234' and no previous clashes for 'Bob'
    When I try to add two new entries with the same number
    Then the number of clashes recorded for 'Bob' is 2
    """
    enterprise_phonebook.add('Bob', '1234')

    enterprise_phonebook.add('Sid', '1234')
    enterprise_phonebook.add('Ali', '1234')

    clashes = requests.get(f"{server_url}/clash_frequencies")
    assert clashes.json() == {'entries': {'Bob with number 1234': 2}}
