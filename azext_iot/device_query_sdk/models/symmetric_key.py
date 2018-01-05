# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SymmetricKey(Model):
    """Primary and secondary shared access signature symmetric keys of a device.
    If specified, both primary key and secondary key are required. The keys
    must be in valid base-64 format with a key length between 16 bytes and 64
    bytes. They can be identical. If they are not specified, the Iot Hub
    generates both keys for the device with a default key length of 32 bytes.

    :param primary_key:
    :type primary_key: str
    :param secondary_key:
    :type secondary_key: str
    """

    _attribute_map = {
        'primary_key': {'key': 'primaryKey', 'type': 'str'},
        'secondary_key': {'key': 'secondaryKey', 'type': 'str'},
    }

    def __init__(self, primary_key=None, secondary_key=None):
        self.primary_key = primary_key
        self.secondary_key = secondary_key