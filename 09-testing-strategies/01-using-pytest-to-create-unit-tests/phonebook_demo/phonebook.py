class Phonebook:
    def __init__(self):
        self.storage = {}

    def add(self, name, number):
        self.storage[name] = number

    def lookup(self, name):
        return self.storage[name]

    def names(self):
        return self.storage.keys()

    def is_consistent(self):
        for name1, number1 in self.storage.items():
            for name2, number2 in self.storage.items():
                if name1 == name2:
                    continue
                if number1.startswith(number2):
                    return False
        return True
