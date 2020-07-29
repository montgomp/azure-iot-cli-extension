# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PnpCertificationBadgeConfiguration(Model):
    """PnpCertificationBadgeConfiguration.

    :param digital_twin_model_definitions:
    :type digital_twin_model_definitions: list[str]
    :param type: Possible values include: 'IotDevice', 'Pnp',
     'IotEdgeCompatible'
    :type type: str or ~product.models.enum
    """

    _attribute_map = {
        'digital_twin_model_definitions': {'key': 'digitalTwinModelDefinitions', 'type': '[str]'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(PnpCertificationBadgeConfiguration, self).__init__(**kwargs)
        self.digital_twin_model_definitions = kwargs.get('digital_twin_model_definitions', None)
        self.type = kwargs.get('type', None)