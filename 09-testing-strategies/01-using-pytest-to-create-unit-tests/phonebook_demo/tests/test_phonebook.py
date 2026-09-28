import pytest

from phonebook import Phonebook


# Look up by name
# Missing name
# Consistent
# Inconsistent

@pytest.fixture
def phonebook():
    return Phonebook()


# don't do this
def test_is_consistent(phonebook):
    assert phonebook.is_consistent()
    phonebook.add("Bob", "1234")
    assert phonebook.is_consistent()
    phonebook.add("Sue", "78955")
    assert phonebook.is_consistent()
    phonebook.add("Ann", "12345678")
    assert not phonebook.is_consistent()


def test_is_consistent_empty(phonebook):
    assert phonebook.is_consistent()


def test_is_consistent_one_entry(phonebook):
    phonebook.add("Bob", "1234")
    assert phonebook.is_consistent()


def test_is_consistent_multiple_entry(phonebook):
    phonebook.add("Bob", "1234")
    phonebook.add("Sue", "78955")
    assert phonebook.is_consistent()


def test_is_inconsistent_entry_prefix_of_another(phonebook):
    phonebook.add("Bob", "1234")
    phonebook.add("Ann", "12345678")
    assert not phonebook.is_consistent()


def test_is_inconsistent_entry_identical(phonebook):
    phonebook.add("Bob", "1234")
    phonebook.add("Ted", "1234")
    assert not phonebook.is_consistent()


@pytest.mark.parametrize(
    "entry1,entry2,is_consistent",
    [
        [("Bob", "1234"), ("Ted", "1234"), False],
        [("Bob", "1234"), ("Ann", "12345678"), False],
        [("Bob", "1234"), ("Sue", "78955"), True],
    ]
)
def test_is_consistent_two_entries(phonebook, entry1, entry2, is_consistent):
    phonebook.add(*entry1)
    phonebook.add(*entry2)
    assert phonebook.is_consistent() == is_consistent


def test_lookup_missing_name(phonebook):
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")


def test_names(phonebook):
    phonebook.add("Bob", "1234")

    names = phonebook.names()

    assert ["Bob"] == list(names)


def test_look_up_by_name(phonebook):
    phonebook.add("Bob", "1234")

    result = phonebook.lookup("Bob")

    assert result == "1234"


def test_look_up_by_name_longer_number(phonebook):
    phonebook.add("Ann", "12345678")

    result = phonebook.lookup("Ann")

    assert result == "12345678"
