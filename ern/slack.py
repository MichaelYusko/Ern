import requests as r

from ern.utils.const import SLACK_BASE_URL
from ern.utils.errors import SlackApiError


class BaseApi:
    def __init__(self, token):
        if not token:
            raise SlackApiError('Please provide your token')
        self.token = token

    BASE_URL = SLACK_BASE_URL

    def _get(self, method, **kwargs):
        return r.get(SLACK_BASE_URL + method, **kwargs).json()


class Channel(BaseApi):
    @property
    def list(self):
        return self._get('channels.list', params={'token': self.token})


class SlackApi(BaseApi):
    def __init__(self, token=None):
        super().__init__(token)
        self.channels = Channel(token)

    def request(self):
        result = self._get('auth.test', params={'token': self.token})
        return result
