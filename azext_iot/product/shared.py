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


class AttestationType(Enum):
    symmetricKey = "symmetricKey"
    tpm = "tpm"
    x509 = "x509"
    connectionString = "connectionString"


class DeviceType(Enum):
    FinishedProduct = "FinishedProduct"
    DevKit = "DevKit"


class DeviceTestTaskStatus(Enum):
    queued = "Queued"
    started = "Started"
    running = "Running"
    completed = "Completed"
    failed = "Failed"
    cancelled = "Cancelled"


BASE_URL = "https://canary.certsvc.trafficmanager.net"
# BASE_URL = "https://test.certsvc.trafficmanager.net"
# BASE_URL = "https://dev.certsvc.trafficmanager.net"
