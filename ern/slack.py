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

    def _get_user(self, user_name):
        result = ''
        if user_name:
            all_users = self.user_list['members']
            members = []
            for user in all_users:
                members.append(user['name'])
                if user_name == user['name']:
                    result = user['id']
            if user_name not in members:
                raise SlackChannelError('User {} not found'.format(user_name))
            return result
        else:
            return result

    def _get_channel(self, name):
        result = ''
        if name:
            all_channels = self.list['channels']
            chanel_names = []
            for channel in all_channels:
                chanel_names.append(channel['name'])
                if name == channel['name']:
                    result = channel['id']
            if name not in chanel_names:
                raise SlackChannelError('Channel {} not found'.format(name))
            return result
        else:
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

    def history(self, name, count=100):
        return self.get('channels.history',
                        params={
                            'channel': self._get_channel(name),
                            'count': count}
                        )

    def create(self, channel_name, validate=False):
        return self.post('channels.create',
                         params={'name': self._get_channel(channel_name),
                                 'validate': validate}
                         )

    def info(self, channel_name):
        return self.get('channels.info',
                        params={'channel': self._get_channel(channel_name)})

    def invite(self, channel_name, user_name):
        return self.post('channels.invite',
                         params={'channel': self._get_channel(channel_name),
                                 'user': self._get_user(user_name)}
                         )

    def join(self, channel_name, validate=True):
        return self.post('channels.join',
                         params={'name': self._get_channel(channel_name),
                                 'validate': validate}
                         )

    def kick(self, channel_name, user_name):
        return self.post('channels.kick',
                         params={'channel': self._get_channel(channel_name),
                                 'user': self._get_user(user_name)}
                         )

    def leave(self, channel_name):
        return self.post('channels.leave',
                         params={'channel': self._get_channel(channel_name)})

    def rename(self, old_name, new_channel_name,
               validate=True):
        return self.post('channels.rename',
                         params={
                             'channel': self._get_channel(old_name),
                             'name': new_channel_name,
                             'validate': validate}
                         )

    def open(self, channel_name):
        return self.post('groups.open',
                         params={'channel': self._get_channel(channel_name)}
                         )

    def mark(self, channel_name, time_stamp):
        return self.post('channels.mark',
                         params={'channel': self._get_channel(channel_name),
                                 'ts': time_stamp}
                         )

    def replies(self, channel_name, thread_time_stamp):
        return self.post('channels.replies',
                         params={'channel': self._get_channel(channel_name),
                                 'thread_ts': thread_time_stamp})

    def set_purpose(self, channel_name, purpose):
        return self.post('channels.setPurpose',
                         params={'channel': self._get_channel(channel_name),
                                 'purpose': purpose}
                         )

    def set_topic(self, channel_name, topic):
        return self.post('channels.setTopic',
                         params={'channel': self._get_channel(channel_name),
                                 'topic': topic}
                         )

    def unarchive(self, channel_name):
        return self.post('channels.unarchive',
                         params={'channel': self._get_channel(channel_name)})


class Chat(BaseApi):
    """
    WARNING - all methods in the class will be refactor
        when be added converter for the time_stamp.

    you can find the issue: https://github.com/MichaelYusko/Ern/issues/17
    """

    def delete(self, channel_name, time_stamp, as_user=True):
        return self.post('chat.delete',
                         params={'channel': self._get_channel(channel_name),
                                 'ts': time_stamp,
                                 'as_user': as_user})

    def me_message(self, channel_name, text='Test message'):
        return self.post('chat.meMessage',
                         params={'channel': self._get_channel(channel_name),
                                 'text': text}
                         )

    def post_message(self, channel_name, text='Text message',
                     parse=None, link_names=True,
                     unfurl_media=False, username='My Bot',
                     as_user=True, icon_url='http://lorempixel.com/48/48',
                     icon_emoji=':chart_with_upwards_trend:',
                     thread_ts=None, reply_broadcast=False):

        return self.post('chat.postMessage',
                         params={'channel': self._get_channel(channel_name),
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
               unfurls, user_auth_required=False):

        return self.post('chat.unfurl',
                         params={'channel': self._get_channel(channel_name),
                                 'ts': time_stamp,
                                 'unfurls': unfurls,
                                 'user_auth_required': user_auth_required})

    def update(self, channel_name, ts, text='Test update',
               parse=None, link_names=None, as_user=True):

        return self.post('chat.update',
                         params={'ts': ts,
                                 'channel': self._get_channel(channel_name),
                                 'text': text,
                                 'parse': parse,
                                 'link_names': link_names,
                                 'as_user': as_user}
                         )


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
        return self.get('dnd.info', params={'user': self._get_user(user_name)})


class Emoji(BaseApi):
    def list(self):
        return self.get('emoji.list')


class File(BaseApi):
    """
    Will be added next functions for the channel:
         upload
    """
    def file_list(self, user_name=None, channe_name=None,
                  ts_from=None, ts_to=None,
                  types=None, count=None,
                  page=None):

        return self.get('files.list',
                        params={'user': self._get_user(user_name),
                                'channel': self._get_channel(channe_name),
                                'ts_from': ts_from,
                                'ts_to': ts_to,
                                'types': types,
                                'page': page,
                                'count': count}
                        )

    def delete(self, file):
        return self.post('files.delete', params={'file': file})

    def info(self, file, count=None, page=None):
        return self.get('files.info', params={'file': file,
                                              'count': count,
                                              'page': page})

    def revoke_public_url(self, file):
        return self.post('files.revokePublicURL', params={'file': file})

    def shared_public_url(self, file):
        return self.post('files.sharedPublicURL', params={'file': file})

    def upload(self, file):
        pass


class Group(BaseApi):
    def archive(self, channel_name):
        return self.post('groups.archive',
                         params={'channel': self._get_channel(channel_name)})

    def close(self, channel_name):
        return self.post('groups.close',
                         params={'channel': self._get_channel(channel_name)})

    def create(self, name, validate=True):
        return self.post('groups.create', params={'name': name,
                                                  'validate': validate})

    def create_child(self, channel_name):
        return self.post('groups.createChild',
                         params={'channel': self._get_channel(channel_name)}
                         )

    def history(self, channel_name, latest=None, oldest=None,
                inclusive=None, count=None, unreads=None):
        return self.post('groups.history',
                         params={'channel': self._get_channel(channel_name),
                                 'latest': latest,
                                 'oldest': oldest,
                                 'inclusive': inclusive,
                                 'count': count,
                                 'unreads': unreads}
                         )

    def info(self, channel_name):
        return self.get('groups.info',
                        params={'channel': self._get_channel(channel_name)})

    def invite(self, channel_name, user_name):
        return self.post('groups.invite',
                         params={'channel': self._get_channel(channel_name),
                                 'user': self._get_user(user_name)}
                         )

    def kick(self, channel_name, user_name):
        return self.post('groups.kick',
                         params={'channel': self._get_channel(channel_name),
                                 'user': self._get_user(user_name)}
                         )

    def leave(self, channel_name):
        return self.post('groups.kick',
                         params={'channel': self._get_channel(channel_name)})

    def list(self, exclude_archived=None):
        return self.get('groups.list',
                        params={'exclude_archived': exclude_archived})

    def mark(self, channel_name, time_stamp):
        return self.post(
            'groups.mark',
            params={
                'channel_name': self._get_channel(channel_name),
                'ts': time_stamp
            }
        )

    def open(self, channel_name):
        return self.post(
            'groups.open',
            params={
                'channel_name': self._get_channel(channel_name)
            }
        )


class Team(BaseApi):
    def access_logs(self, count=100, page=1):
        return self.get('team.accessLogs',
                        params={'count': count, 'page': page})

    def billable_info(self, user_name):
        return self.get('team.billableInfo',
                        params={'user': self._get_user(user_name)})

    @property
    def info(self):
        return self.get('team.info')

    def integration_logs(self, user_name='', count=100, page=1,
                         service_id=None, app_id=None,
                         change_type=None):
        return self.get(
            'team.integrationLogs',
            params={
                'user': self._get_user(user_name),
                'count': count,
                'page': page,
                'service_id': service_id,
                'app_id': app_id,
                'change_type': change_type
            }
        )


class TeamProfile(BaseApi):
    def get_profile(self, visibility=None):
        return self.get('team.profile.get', params={'visibility': visibility})


class RTM(BaseApi):
    @property
    def connect(self):
        return self.get('rtm.connect')

    def start(self, simple_latest=False, no_unreads=False,
              mpim_aware=None, no_latest=False):

        return self.post(
            'rtm.start',
            params={
                'simple_latest': simple_latest,
                'no_unreads': no_unreads,
                'mpim_aware': mpim_aware,
                'no_latest': no_latest
            }
        )


class SlackClient(BaseApi):
    """
    Slack client
    """
    def __init__(self, token=None):
        super().__init__(token)
        self.channel = Channel(token)
        self.chat = Chat(token)
        self.auth = Auth(token)
        self.dnd = DnD(token)
        self.emoji = Emoji(token)
        self.file = File(token)
        self.group = Group(token)
        self.team = Team(token)
        self.team_profile = TeamProfile(token)
        self.rtm = RTM(token)
