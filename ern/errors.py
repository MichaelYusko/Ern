class ConvertError(Exception):
    pass


############################
# Error classes for Slack API
############################
class SlackApiError(Exception):
    pass


class SlackChannelError(Exception):
    def __init__(self, channel):
        self.channel = channel

    def __str__(self):
        return 'Channel {} nof found'.format(self.channel)


class SlackUserError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'User {} not found.'.format(self.name)


class SlackTokenError(Exception):
    def __str__(self): return 'Please provide your token'


############################
# Error classes for Gitter API
############################
class GitterTokenError(Exception):
    def __str__(self): return 'Please provide your token'
