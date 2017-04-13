import requests as r

from ern.utils.const import TEST_SLACK_API
from ern.utils.json import to_dict


class SlackApi:
    def __init__(self, url=None):
        if url is None:
            self.url = TEST_SLACK_API
        else:
            self.url = url

    def test_request(self):
        """
        :return: dict_, msg

          a tuple with response from slack,
          and message/status that api work fine

          example:
            ({'ok': True}, 'Slack work correct - <Response [200]>')
        """
        req = r.get(self.url)
        dict_ = to_dict(req.text)
        if 'ok' in dict_.keys():
            msg = 'Slack work correct - {}'.format(req)
        else:
            msg = 'Something wrong - {}'.format(req)
        return dict_, msg
