from authorization import SecurityClearanceAuthorizer


# auth ok - 200
# auth not ok - 404 not found

def test_auth_ok(url, endpoint_handler):
    authorizer = SecurityClearanceAuthorizer(url)
    endpoint_handler.response_code = 200

    result = authorizer.is_authorized()

    assert result is True

def test_auth_not_found(url, endpoint_handler):
    authorizer = SecurityClearanceAuthorizer(url)
    endpoint_handler.response_code = 404

    result = authorizer.is_authorized()

    assert result is False