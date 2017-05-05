import requests as r

from ern.errors import GitterTokenError


class BaseApi:
    def __init__(self, token):
        if not token:
            raise GitterTokenError
        self.token = token

    def request_process(self, method, api, **kwargs):
        kwargs.setdefault('Authorization', 'Bearer ' + self.token)
        return method('https://api.gitter.im/v1/' + api, headers=kwargs).json()

    def get(self, api, **kwargs):
        return self.request_process(r.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self.request_process(r.post, api, **kwargs)


class Auth(BaseApi):
    @property
    def check_auth(self):
        return self.get('user')


class GitterClient(BaseApi):
    def __init__(self, token=None):
        super().__init__(token)
        self.auth = Auth(token)
