import pytest

from phonebook import Phonebook


@pytest.fixture
def phonebook():
    return Phonebook()
