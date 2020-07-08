# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class C2DTest(Model):
    """C2DTest.

    :param message_to_send:
    :type message_to_send: str
    :param validation_timeout:
    :type validation_timeout: int
    :param is_mandatory:
    :type is_mandatory: bool
    :param should_validate:
    :type should_validate: bool
    """

    _attribute_map = {
        'message_to_send': {'key': 'messageToSend', 'type': 'str'},
        'validation_timeout': {'key': 'validationTimeout', 'type': 'int'},
        'is_mandatory': {'key': 'isMandatory', 'type': 'bool'},
        'should_validate': {'key': 'shouldValidate', 'type': 'bool'},
    }

    def __init__(self, *, message_to_send: str=None, validation_timeout: int=None, is_mandatory: bool=None, should_validate: bool=None, **kwargs) -> None:
        super(C2DTest, self).__init__(**kwargs)
        self.message_to_send = message_to_send
        self.validation_timeout = validation_timeout
        self.is_mandatory = is_mandatory
        self.should_validate = should_validate
