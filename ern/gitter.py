import requests as r

from ern.const import GITTER_BASE_URL
from ern.errors import GitterTokenError


class BaseApi:
    def __init__(self, token):
        if not token:
            raise GitterTokenError
        self.token = token

    def request_process(self, method, api, **kwargs):
        headers = {
            'Authorization': 'Bearer ' + self.token,
        }
        return method(GITTER_BASE_URL + api, headers=headers, **kwargs).json()

    def get(self, api, **kwargs):
        return self.request_process(r.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self.request_process(r.post, api, **kwargs)

    @property
    def groups_list(self):
        return self.get('groups')


class Auth(BaseApi):

    def check_auth(self):
        return self.get('user')

    @property
    def get_my_id(self):
        user_id = self.check_auth()[0]['id']
        name = self.check_auth()[0]['username']
        return 'User {}, id: {}'.format(name, user_id)


class Groups(BaseApi):
    @property
    def list(self):
        return self.groups_list


class Rooms(BaseApi):
    @property
    def list(self):
        return self.get('rooms')

    def grab_room(self, uri_name):
        return self.post('rooms', data={'uri': uri_name})

    def get_room_id(self, uri_name):
        room = self.post('rooms', data={'uri': uri_name})
        return 'Room {}, id: {}'.format(room['name'], room['id'])


class GitterClient(BaseApi):
    def __init__(self, token=None):
        super().__init__(token)
        self.auth = Auth(token)
        self.groups = Groups(token)
        self.rooms = Rooms(token)
