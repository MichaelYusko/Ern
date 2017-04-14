
from .errors import ConvertError


def to_dict(obj=None):
    """
    :param obj: retrieve json object and convert into dict
    """
    if obj is None:
        raise ConvertError('Object not found')
    else:
        resp = dict(obj)
    return resp
