# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PropertyTest(Model):
    """PropertyTest.

    :param property:
    :type property: ~swagger.models.PropertyModel
    :param value_to_write:
    :type value_to_write: str
    :param value_to_report:
    :type value_to_report: str
    :param validation_timeout:
    :type validation_timeout: int
    :param is_mandatory:
    :type is_mandatory: bool
    :param should_validate:
    :type should_validate: bool
    """

    _attribute_map = {
        'property': {'key': 'property', 'type': 'PropertyModel'},
        'value_to_write': {'key': 'valueToWrite', 'type': 'str'},
        'value_to_report': {'key': 'valueToReport', 'type': 'str'},
        'validation_timeout': {'key': 'validationTimeout', 'type': 'int'},
        'is_mandatory': {'key': 'isMandatory', 'type': 'bool'},
        'should_validate': {'key': 'shouldValidate', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(PropertyTest, self).__init__(**kwargs)
        self.property = kwargs.get('property', None)
        self.value_to_write = kwargs.get('value_to_write', None)
        self.value_to_report = kwargs.get('value_to_report', None)
        self.validation_timeout = kwargs.get('validation_timeout', None)
        self.is_mandatory = kwargs.get('is_mandatory', None)
        self.should_validate = kwargs.get('should_validate', None)
