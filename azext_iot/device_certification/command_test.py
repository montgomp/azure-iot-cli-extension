# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def initialize_workspace(cmd, product_name, working_folder="PnPCert"):
    # create working folder if it doesn't exist
    # create a <product_name>.json file with details from Koichi
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
