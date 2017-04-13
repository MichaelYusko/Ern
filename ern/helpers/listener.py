class ListInstance:
    """
    Class that provides a formatted print() or srt() instances
    via inheritance

    displays:
        class name of instance
        class attributes only
        id of instance

    Example:
        class SlackApi(ListInstance):
            do something...

        slack = SlackApi()

        print(slack)

        Output:
            <Instance of SlackApi, object id 4336260992:
                Data:
                url=https://slack.com/api/api.test
    """
    def __attrname(self):
        result = ''
        for attr in sorted(self.__dict__):
            result += '\tData:\n\t{}={}\n'.format(attr, self.__dict__[attr])
        return result

    def __str__(self):
        return '<Instance of {}, object id {}:\n {}'.format(
            self.__class__.__name__,
            id(self),
            self.__attrname()
        )
