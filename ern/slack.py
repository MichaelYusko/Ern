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

    def _request_process(self, method, api, **kwargs):
        kwargs.setdefault('params', {})['token'] = self.token
        return method(SLACK_BASE_URL + api, **kwargs).json()

    def get(self, api, **kwargs):
        return self._request_process(r.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self._request_process(r.post, api, **kwargs)


class Channel(BaseApi):
    """
    Class which working with SLACK channels, that related to slack channels
    need to put here
    """
    def _find_by_name(self, name):
        all_channels = self.list['channels']
        result = ''
        chanel_names = []
        for channel in all_channels:
            chanel_names.append(channel['name'])
            if name == channel['name']:
                result = channel['id']
        if name not in chanel_names:
            raise SlackChannelError('Channel not found')
        return result

    @property
    def list(self):
        return self.get('channels.list')

    def history(self, name, count=100):
        name = self._find_by_name(name)
        return self.get('channels.history', params={'channel': name,
                                                    'count': count})

    def create(self, channel_name, validate=False):
        return self.post('channels.create', params={'name': channel_name,
                                                    'validate': validate})

    def info(self, channel_name):
        name = self._find_by_name(channel_name)
        return self.get('channels.info', params={'channel': name})


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
