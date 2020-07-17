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


class ModelSearchOptions(Model):
    """Model Search Options.

    :param search_keyword: Gets or sets keyword for model search. Searches
     within pre-defined properties.
    :type search_keyword: str
    :param model_type: Gets or sets the type of the model. Possible values
     include: 'Interface', 'Undetermined'
    :type model_type: str or ~pnp.models.enum
    :param model_state: Gets or sets the state of the model. Possible values
     include: 'Created', 'Listed'
    :type model_state: str or ~pnp.models.enum
    :param publisher_id: Gets or sets the publisher identifier.
    :type publisher_id: str
    :param created_by: Gets or sets the created by.
    :type created_by: str
    """

    _attribute_map = {
        'search_keyword': {'key': 'searchKeyword', 'type': 'str'},
        'model_type': {'key': 'modelType', 'type': 'str'},
        'model_state': {'key': 'modelState', 'type': 'str'},
        'publisher_id': {'key': 'publisherId', 'type': 'str'},
        'created_by': {'key': 'createdBy', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ModelSearchOptions, self).__init__(**kwargs)
        self.search_keyword = kwargs.get('search_keyword', None)
        self.model_type = kwargs.get('model_type', None)
        self.model_state = kwargs.get('model_state', None)
        self.publisher_id = kwargs.get('publisher_id', None)
        self.created_by = kwargs.get('created_by', None)
