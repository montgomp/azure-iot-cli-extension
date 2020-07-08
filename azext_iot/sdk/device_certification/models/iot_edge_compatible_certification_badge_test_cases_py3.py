# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class IotEdgeCompatibleCertificationBadgeTestCases(Model):
    """IotEdgeCompatibleCertificationBadgeTestCases.

    :param type: Possible values include: 'IotDevice', 'Pnp',
     'IotEdgeCompatible'
    :type type: str or ~swagger.models.enum
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, *, type=None, **kwargs) -> None:
        super(IotEdgeCompatibleCertificationBadgeTestCases, self).__init__(**kwargs)
        self.type = type
