def test_request(slack_client):
    success = ({'ok': True}, 'Slack work correct - <Response [200]>')
    assert slack_client.test_request() == success
