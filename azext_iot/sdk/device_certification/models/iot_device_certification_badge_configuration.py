# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class IotDeviceCertificationBadgeConfiguration(Model):
    """IotDeviceCertificationBadgeConfiguration.

    :param type: Possible values include: 'IotDevice', 'Pnp',
     'IotEdgeCompatible'
    :type type: str or ~swagger.models.enum
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(IotDeviceCertificationBadgeConfiguration, self).__init__(**kwargs)
        self.type = kwargs.get('type', None)
