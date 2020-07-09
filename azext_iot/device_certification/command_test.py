# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.device_certification.shared import AuthType

def initialize_workspace(cmd, product_name, working_folder="PnPCert", auth_type=AuthType.symmetricKey):
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

def create(configuration_file, provisioning=False):
    # call to POST /deviceTests
    return True

def show(test_id):
    # call to GET /deviceTests/{deviceTestId}
    return True

def update(configuration_file, provisioning=False):
    # call to POST /deviceTests
    return True

def search(product_id="", registration_id="", certificate_name=""):
    # call to POST /deviceTests/search
    return True
