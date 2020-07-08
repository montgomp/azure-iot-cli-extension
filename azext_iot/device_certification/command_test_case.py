# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.device_certification.shared import BadgeType

def list(test_id):
    # call to GET /deviceTests/{deviceTestId}/testCases
    return True

def update(test_id, configuration_file, badge_type=BadgeType.IotDevice):
# call to PATCH /deviceTests/{deviceTestId}/TestCases
    return True
