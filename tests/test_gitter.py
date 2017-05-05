import json
import unittest

from mock import Mock, patch

from ern.gitter import Auth


class TestGitter(unittest.TestCase):
    def setUp(self):
        self.auth = Auth('MY COOL TOKEN')

    def tearDown(self): pass

    @patch('ern.gitter.r')
    def test_gitter_auth(self, request):
        text = [{'id': '1', 'name': 'Freshjelly'}]
        json_data = json.dumps(text)
        request.get.return_value = Mock(
            status_code=200, text=json_data
        )
        self.assertTrue(json_data, self.auth.check_auth)

if __name__ == '__main__':
    unittest.main()
