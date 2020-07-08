# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.device_certification.shared import BadgeType

def list(badge_type=BadgeType.IotDevice):
    # call to GET /certificationRequirements
    return True
