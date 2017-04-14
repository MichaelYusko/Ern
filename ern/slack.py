import requests as r

from ern.utils.const import SLACK_BASE_URL
from ern.utils.errors import SlackApiError, SlackChannelError


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
    def _find_by_name(self, name):
        all_channels = self.list['channels']
        channel_id = ''
        for channel in all_channels:
            if name == channel['name']:
                channel_id = channel['id']
            if name not in all_channels:
                raise SlackChannelError('Please enter correct channel name')
        return channel_id

    @property
    def list(self):
        return self.get('channels.list')

    def history(self, name, count=100):
        name = self._find_by_name(name)
        return self.get('channels.history', params={'channel': name,
                                                    'count': count})


class SlackApi(BaseApi):
    """
    Slack client
    """
    def __init__(self, token=None):
        super().__init__(token)
        self.channels = Channel(token)

    def check_auth(self):
        result = self.get('auth.test')
        return result
