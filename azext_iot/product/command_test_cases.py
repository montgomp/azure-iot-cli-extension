# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.shared import BadgeType
from azext_iot.product.providers.aics import AICSProvider


def list(cmd, test_id):
    ap = AICSProvider(cmd)
    return ap.show_test_cases(test_id=test_id)


def update(cmd, test_id, configuration_file, badge_type=BadgeType.IotDevice):
    ap = AICSProvider(cmd)
    return ap.update_test_cases(test_id=test_id, patch=configuration_file)
