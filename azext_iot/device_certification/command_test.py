# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.device_certification.shared import AuthType
from azext_iot.device_certification.providers.provider import get_sdk
from azext_iot.sdk.device_certification.version import VERSION
from knack.util import CLIError


def initialize_workspace(cmd, product_name, working_folder="PnPCert", auth_type=AuthType.symmetricKey):
    # https://prtnrsvcstortstcus.blob.core.windows.net/product-metadata-templates/product_template.json
    # create working folder if it doesn't exist
    # create a <product_name>.json file with details from Koichi
    # if x509, then
    # "x509EnrollmentInformation": {
    #   "scopeId": "string",
    #   "subject": "string",
    #   "thumbprint": "string",
    #   "registrationId": "string",
    #   "base64EncodedX509Certificate": "string"
    # },

    # if symmetric key then
    # "symmetricKeyEnrollmentInformation": {
    #   "registrationId": "string",
    #   "primaryKey": "string",
    #   "secondaryKey": "string",
    #   "scopeId": "string"
    # },

    # if tpm then
    # "tpmEnrollmentInformation": {
    #   "scopeId": "string",
    #   "registrationId": "string",
    #   "endorsementKey": "string",
    #   "storageRootKey": "string"
    # }
    return True


def create(cmd, configuration_file, provisioning=False):
    # call to POST /deviceTests
    return True


def show(cmd, test_id):
    # call to GET /deviceTests/{deviceTestId}
    return True


def update(cmd, test_id, configuration_file, provisioning=False):
    # call to POST /deviceTests
    return True


def search(cmd, product_id=None, registration_id=None, certificate_name=None):
    # call to POST /deviceTests/search
    if not any([product_id or registration_id or certificate_name]):
        raise CLIError('At least one search criteria must be specified')

    searchOptions = {
        'product_id': product_id,
        'dps_registration_id': registration_id,
        'dps_x509_certificate_common_name': certificate_name
    }
    return get_sdk(cmd).search_device_test(
        VERSION,
        searchOptions
    )
