import json

from alerts import InconsistentPhonebookAlerter, BadPhonebookEntryEvent, event_to_alert


def test_generate_alert(url, endpoint_handler):
    alerter = InconsistentPhonebookAlerter(url)
    event = BadPhonebookEntryEvent(3, "Ted", "1234", ("Bob", "1234"))

    alerter.send_alert(event)

    assert endpoint_handler.latest_request_type == "PUT"
    assert endpoint_handler.latest_request_body is not None
    json_str = endpoint_handler.latest_request_body.decode('utf-8')
    assert json.loads(json_str) == event_to_alert(event)
