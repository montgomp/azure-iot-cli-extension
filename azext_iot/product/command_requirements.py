# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.shared import BadgeType
from azext_iot.product.providers.aics import AICSProvider


def list(cmd, badge_type=BadgeType.IotDevice):
    ap = AICSProvider(cmd)
    return ap.list_requirements(badge_type=badge_type)
