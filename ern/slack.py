import requests as r

from ern.utils.const import SLACK_BASE_URL
from ern.utils.errors import SlackApiError


class BaseApi:
    """
    Default class for each classes
    get/post/delete methods need to put here
    """
    def __init__(self, token):
        if not token:
            raise SlackApiError('Please provide your token')
        self.token = token

    BASE_URL = SLACK_BASE_URL

    def get(self, method, **kwargs):
        kwargs.setdefault('params', {})['token'] = self.token
        return r.get(SLACK_BASE_URL + method, **kwargs).json()


class Channel(BaseApi):
    """
    Class which working with SLACK channels, that related to slack channels
    need to put here
    """
    @property
    def list(self):
        return self.get('channels.list')

    def history(self, name):
        return self.get('channels.history', params={'channel': name})


class SlackApi(BaseApi):
    """
    Slack client
    """
    def __init__(self, token=None):
        super().__init__(token)
        self.channels = Channel(token)

    def request(self):
        result = self.get('auth.test')
        return result
