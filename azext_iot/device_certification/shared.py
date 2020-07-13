# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from enum import Enum


class TaskType(Enum):
    QueueTestRun = "QueueTestRun"
    GenerateTestCases = "GenerateTestCases"


class BadgeType(Enum):
    IotDevice = "IotDevice"
    Pnp = "Pnp"
    IotEdgeCompatible = "IotEdgeCompatible"


class AuthType(Enum):
    symmetricKey = "symmetricKey"
    tpm = "tpm"
    x509 = "x509"


# BASE_URL = "https://test.certcvc.trafficmanager.net"
BASE_URL = "https://dev.certsvc.trafficmanager.net"
