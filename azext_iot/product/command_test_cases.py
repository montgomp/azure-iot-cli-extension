# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.shared import BadgeType


def list(test_id):
    # call to GET /deviceTests/{deviceTestId}/testCases
    '61c5939c-bf0e-4116-b62c-fe43ea7f8dd5'
    return True


def update(test_id, configuration_file, badge_type=BadgeType.IotDevice):
    # call to PATCH /deviceTests/{deviceTestId}/TestCases
    return True
