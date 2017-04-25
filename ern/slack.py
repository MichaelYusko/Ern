import requests as r

from ern.const import SLACK_BASE_URL
from ern.utils.errors import SlackApiError, SlackChannelError


class BaseApi:
    """
    Default class for each classes
    get/post/delete methods need to put here
    also if method is using in two or more classes
    we need put here the method.
    """
    def __init__(self, token):
        if not token:
            raise SlackApiError('Please provide your token')
        self.token = token

    def _request_process(self, method, api, **kwargs):
        kwargs.setdefault('params', {})['token'] = self.token
        return method(SLACK_BASE_URL + api, **kwargs).json()

    def get(self, api, **kwargs):
        return self._request_process(r.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self._request_process(r.post, api, **kwargs)

    @property
    def user_list(self):
        return self.get('users.list')

    def find_by_user_name(self, user_name):
        """
        Method will be refactor
        """
        all_users = self.user_list['members']
        result = ''
        members = []
        for user in all_users:
            members.append(user['name'])
            if user_name == user['name']:
                result = user['id']
        if user_name not in members:
            raise SlackChannelError('User {} not found'.format(user_name))
        return result

    def _find_by_channel_name(self, name):
        all_channels = self.list['channels']
        result = ''
        chanel_names = []
        for channel in all_channels:
            chanel_names.append(channel['name'])
            if name == channel['name']:
                result = channel['id']
        if name not in chanel_names:
            raise SlackChannelError('Channel {} not found'.format(name))
        return result

    @property
    def list(self):
        return self.get('channels.list')


class Auth(BaseApi):
    def revoke(self, test=True):
        return self.post('auth.revoke', params={'test': test})

    def check_auth(self):
        return self.post('auth.test')


class Channel(BaseApi):
    """
    Class which working with SLACK channels, that related to slack channels
    need to put here
    """
    def _find_by_channel_name(self, name):
        all_channels = self.list['channels']
        result = ''
        chanel_names = []
        for channel in all_channels:
            chanel_names.append(channel['name'])
            if name == channel['name']:
                result = channel['id']
        if name not in chanel_names:
            raise SlackChannelError('Channel {} not found'.format(name))
        return result

    def history(self, name, count=100):
        name = self._find_by_channel_name(name)
        return self.get('channels.history', params={'channel': name,
                                                    'count': count})

    def create(self, channel_name, validate=False):
        return self.post('channels.create', params={'name': channel_name,
                                                    'validate': validate})

    def info(self, channel_name):
        name = self._find_by_channel_name(channel_name)
        return self.get('channels.info', params={'channel': name})

    def invite(self, channel_name, user_name):
        channel_n = self._find_by_channel_name(channel_name)
        user_n = self.find_by_user_name(user_name)
        return self.post('channels.invite', params={'channel': channel_n,
                                                    'user': user_n})

    def join(self, channel_name, validate=True):
        return self.post('channels.join', params={'name': channel_name,
                                                  'validate': validate})

    def kick(self, channel_name, user_name):
        channel_n = self._find_by_channel_name(channel_name)
        user_n = self.find_by_user_name(user_name)
        return self.post('channels.kick', params={'channel': channel_n,
                                                  'user': user_n})

    def leave(self, channel_name):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('channels.leave', params={'channel': channel_n})

    def rename(self, old_channel_name, new_channel_name,
               validate=True):
        old_name = self._find_by_channel_name(old_channel_name)
        return self.post('channels.rename', params={'channel': old_name,
                                                    'name': new_channel_name,
                                                    'validate': validate})

    def open(self, channel_name):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('groups.open', params={'channel': channel_n})

    def mark(self, channel_name, time_stamp):
        channel_name = self._find_by_channel_name(channel_name)
        return self.post('channels.mark', params={'channel': channel_name,
                                                  'ts': time_stamp})

    def replies(self, channel_name, thread_time_stamp):
        channel_name = self._find_by_channel_name(channel_name)
        return self.post('channels.replies',
                         params={'channel': channel_name,
                                 'thread_ts': thread_time_stamp})

    def set_purpose(self, channel_name, purpose):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('channels.setPurpose', params={'channel': channel_n,
                                                        'purpose': purpose})

    def set_topic(self, channel_name, topic):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('channels.setTopic', params={'channel': channel_n,
                                                      'topic': topic})

    def unarchive(self, channel_name):
        channel_n = self.find_by_user_name(channel_name)
        return self.post('channels.unarchive', params={'channel': channel_n})


class Chat(BaseApi):
    """
    Share a me message to a channel

    WARNING - all methods in the class will be refactor
        when be added converter for the time_stamp.

    you can find the issue: https://github.com/MichaelYusko/Ern/issues/17
    """

    def delete(self, channel_name, time_stamp, as_user=True):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('chat.delete', params={'channel': channel_n,
                                                'ts': time_stamp,
                                                'as_user': as_user})

    def me_message(self, channel_name, text='Test message'):
        channel_n = self._find_by_channel_name(channel_name)
        return self.post('chat.meMessage', params={'channel': channel_n,
                                                   'text': text})

    def post_message(self, channel_name,
                     text='Text message',
                     parse=None,
                     link_names=True,
                     unfurl_media=False,
                     username='My Bot',
                     as_user=True,
                     icon_url='http://lorempixel.com/48/48',
                     icon_emoji=':chart_with_upwards_trend:',
                     thread_ts=None,
                     reply_broadcast=False):

        channel_n = self._find_by_channel_name(channel_name)
        return self.post('chat.postMessage',
                         params={'channel': channel_n,
                                 'text': text,
                                 'parse': parse,
                                 'link_names': link_names,
                                 'unfurl_media': unfurl_media,
                                 'username': username,
                                 'as_user': as_user,
                                 'icon_url': icon_url,
                                 'icon_emoji': icon_emoji,
                                 'thread_ts': thread_ts,
                                 'reply_broadcast': reply_broadcast
                                 })

    def unfurl(self, channel_name, time_stamp,
               unfurls,
               user_auth_required=False):

        channel_n = self._find_by_channel_name(channel_name)
        return self.post('chat.unfurl',
                         params={'channel': channel_n,
                                 'ts': time_stamp,
                                 'unfurls': unfurls,
                                 'user_auth_required': user_auth_required})

    def update(self, channel_name, ts,
               text='Test update',
               parse=None,
               link_names=None,
               as_user=True):
        channel_n = self._find_by_channel_name(channel_name)

        return self.post('chat.update', params={'ts': ts,
                                                'channel': channel_n,
                                                'text': text,
                                                'parse': parse,
                                                'link_names': link_names,
                                                'as_user': as_user,
                                                })


class DnD(BaseApi):
    def team_info(self, users):
        """
        :param users: must be list type ['Freshjelly', 'MyFriend']
        """
        if isinstance(users, list):
            return self.post('dnd.teamInfo', params={'users': users})
        else:
            raise SlackApiError('Users argument must be list type.')

    def set_snooze(self, num_minutes):
        return self.post('dnd.setSnooze', params={'minutes': num_minutes})

    def end_snooze(self):
        return self.post('dnd.endSnooze')

    def end_dnd(self):
        return self.post('dnd.endDnd')

    def info(self, user_name):
        user_n = self.find_by_user_name(user_name)
        return self.get('dnd.info', params={'user': user_n})


class Emoji(BaseApi):
    def list(self):
        return self.get('emoji.list')


class SlackClient(BaseApi):
    """
    Slack client
    """
    def __init__(self, token=None):
        super().__init__(token)
        self.channels = Channel(token)
        self.chat = Chat(token)
        self.auth = Auth(token)
        self.dnd = DnD(token)
        self.emoji = Emoji(token)
