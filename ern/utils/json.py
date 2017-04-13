import json

from .errors import ConvertError


def to_dict(obj=None):
    """
    :param obj: retrieve str object and convert to json
    :return: dict object
    example:

     Input data:
        obj = "{'key': 'value'}"
     Output data:
        obj = {'key': 'value}
    """
    if obj is None:
        raise ConvertError('Object not found')
    else:
        json_resp = json.loads(obj)
    return dict(json_resp)
