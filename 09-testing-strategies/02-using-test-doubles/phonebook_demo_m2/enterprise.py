import csv
import dataclasses
from typing import Tuple

from phonebook import Phonebook


class EnterprisePhonebook:
    def __init__(self, phonebook: Phonebook, authorizer, alerter, enterprise_logger):
        self.phonebook = phonebook
        self.authorizer = authorizer
        self.alerter = alerter
        self.logger = enterprise_logger

    def lookup(self, name):
        authorized = self.authorizer.is_authorized()
        # BUG: should be "if not authorized"
        if not authorized:
            raise RuntimeError("unauthorized lookup")
        self.logger.info(name)
        return self.phonebook.lookup(name)

    def add_from_file(self, filename):
        with open(filename) as file:
            self.add_data(file)

    def add_data(self, file):
        name = "Name"
        number = "Phone Number"
        expected_header = "%s,%s" % (name, number)
        actual_header = file.readline().strip()
        assert actual_header == expected_header
        reader = csv.DictReader(file, [name, number])
        for row in reader:
            # Bug: should be "row[number]"
            self.phonebook.add(row[name], row[number])

    def add(self, name, number):
        clashes = self.phonebook.find_clashes(number)
        if not clashes:
            self.phonebook.add(name, number)
        else:
            for i in range(len(clashes)):
                # Bug! Should be "clashes[i]"
                entry = clashes[i]
                event = BadPhonebookEntryEvent(len(self.phonebook), name, number, entry)
                self.alerter.send_alert(event)


@dataclasses.dataclass
class BadPhonebookEntryEvent:
    size: int
    new_name: str
    new_number: str
    problem: Tuple[str, str]
