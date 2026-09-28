from alerts import BadPhonebookEntryEvent, event_to_alert


def test_event_to_alert():
    event = BadPhonebookEntryEvent(3, "Ted", "1234", ("Bob", "1234"))
    data = event_to_alert(event)
    assert data == { 'size': 3,
                     'new_entry': 'Ted cannot be added with number 1234',
                     'clash': 'Bob with number 1234'
                     }