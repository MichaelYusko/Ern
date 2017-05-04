import json
import unittest

from mock import Mock, patch

from ern.slack import Channel


class TestChannels(unittest.TestCase):
    def setUp(self):
        self.channel = Channel('MY_COOL_TOKEN')

    def tearDown(self):
        pass

    @patch('ern.slack.r')
    def test_list_channel(self, request):
        text = [
            {'name': 'Cool room', 'id': '1'},
            {'name': 'Cool room2', 'id': '2'}
        ]
        json_data = json.dumps(text)
        request.get.return_value = Mock(
            status_code=200, text=json_data
        )
        self.assertTrue(json_data, self.channel.list)


if __name__ == '__main__':
    unittest.main()
