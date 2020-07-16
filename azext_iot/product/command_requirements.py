# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.shared import BadgeType
from azext_iot.product.providers.provider import get_sdk


def list(cmd, badge_type=BadgeType.IotDevice):
    # call to GET /certificationRequirements
    return get_sdk(cmd).get_device_certification_requirements(badge_type=badge_type)
