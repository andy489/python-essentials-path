import csv

from alerts import BadPhonebookEntryEvent
from phonebook import Phonebook


class EnterprisePhonebook:
    def __init__(self, phonebook: Phonebook, authorizer, alerter, enterprise_logger):
        self.phonebook = phonebook
        self.authorizer = authorizer
        self.alerter = alerter
        self.logger = enterprise_logger

    def lookup(self, name):
        authorized = self.authorizer.is_authorized()
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
            self.phonebook.add(row[name], row[number])

    def add(self, name, number):
        clashes = self.phonebook.find_clashes(number)
        if not clashes:
            self.phonebook.add(name, number)
        else:
            for i in range(len(clashes)):
                entry = clashes[i]
                event = BadPhonebookEntryEvent(len(self.phonebook), name, number, entry)
                self.alerter.send_alert(event)


