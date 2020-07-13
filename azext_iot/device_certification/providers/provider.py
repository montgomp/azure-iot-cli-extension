# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.device_certification.providers.auth import AICSAuthentication
from azext_iot.sdk.device_certification import AICSAPI
from azext_iot.device_certification.shared import BASE_URL
from azext_iot.constants import VERSION as cli_version
from knack.log import get_logger

logger = get_logger(__name__)


def get_sdk(cmd):

    creds = AICSAuthentication(cmd=cmd, base_url=BASE_URL)
    api = AICSAPI(base_url=BASE_URL, credentials=creds)

    api.config.add_user_agent("azcli/aics/{}".format(cli_version))

    return api
