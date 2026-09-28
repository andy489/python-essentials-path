from typing import List, Tuple


class Phonebook:
    def __init__(self):
        self.storage = {}

    def add(self, name, number):
        self.storage[name] = number

    def lookup(self, name):
        return self.storage[name]

    def names(self):
        return self.storage.keys()

    def __len__(self):
        return len(self.storage)

    def remove(self, name, number):
        del self.storage[name]

    def is_consistent(self):
        for name1, number1 in self.storage.items():
            for name2, number2 in self.storage.items():
                if name1 == name2:
                    continue
                if number1.startswith(number2):
                    return False
        return True

    def find_clashes(self, number_to_check) -> List[Tuple[str, str]]:
        entries = []
        for name, number in self.storage.items():
            if number.startswith(number_to_check) or number_to_check.startswith(number):
                entries.append((name, number))
        return entries
