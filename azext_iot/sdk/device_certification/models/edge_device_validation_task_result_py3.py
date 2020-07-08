# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EdgeDeviceValidationTaskResult(Model):
    """EdgeDeviceValidationTaskResult.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param name:
    :type name: str
    :param timeout:
    :type timeout: int
    :param start_time:
    :type start_time: datetime
    :param end_time:
    :type end_time: datetime
    :param status: Possible values include: 'Created', 'Running', 'Failed',
     'Passed', 'Cancelled', 'Aborted'
    :type status: str or ~swagger.models.enum
    :ivar message:
    :vartype message: str
    :ivar logs:
    :vartype logs: list[~swagger.models.CertificationTaskLog]
    :ivar raw_data:
    :vartype raw_data: list[str]
    """

    _validation = {
        'message': {'readonly': True},
        'logs': {'readonly': True},
        'raw_data': {'readonly': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'timeout': {'key': 'timeout', 'type': 'int'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'status': {'key': 'status', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
        'logs': {'key': 'logs', 'type': '[CertificationTaskLog]'},
        'raw_data': {'key': 'rawData', 'type': '[str]'},
    }

    def __init__(self, *, name: str=None, timeout: int=None, start_time=None, end_time=None, status=None, **kwargs) -> None:
        super(EdgeDeviceValidationTaskResult, self).__init__(**kwargs)
        self.name = name
        self.timeout = timeout
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.message = None
        self.logs = None
        self.raw_data = None
