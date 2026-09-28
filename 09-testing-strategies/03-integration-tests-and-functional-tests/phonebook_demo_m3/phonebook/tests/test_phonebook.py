import pytest

from tests.conftest import phonebook


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


def test_lookup_by_name(phonebook):
    phonebook.add("Bob", "12345")
    number = phonebook.lookup("Bob")
    assert number == "12345"


def test_no_clashes(phonebook):
    phonebook.add("Bob", "12345")
    phonebook.add("Sid", "6789")
    assert phonebook.find_clashes("0987") == []


def test_clash_identical(phonebook):
    phonebook.add("Bob", "12345")
    phonebook.add("Sid", "12346")
    assert phonebook.find_clashes("12345") == [("Bob", "12345")]


def test_several_clashes(phonebook):
    phonebook.add("Bob", "12345")
    phonebook.add("Sid", "12346")
    assert phonebook.find_clashes("1234") == [
        ("Bob", "12345"),
        ("Sid", "12346"),
    ]
