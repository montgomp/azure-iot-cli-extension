# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from time import sleep
from azext_iot.product.shared import TaskType, DeviceTestTaskStatus as Status
from azext_iot.product.providers.aics import AICSProvider
from knack.util import CLIError


def create(cmd, test_id, task_type=TaskType.QueueTestRun, wait=False, poll_interval=3):
    ap = AICSProvider(cmd)
    return ap.create_test_task(
        test_id=test_id, task_type=task_type, wait=wait, poll_interval=poll_interval
    )


def delete(cmd, test_id, task_id):
    ap = AICSProvider(cmd)
    return ap.delete_test_task(test_id=test_id, task_id=task_id)


def show(cmd, test_id, task_id=None, running=False):
    ap = AICSProvider(cmd)
    return ap.show_test_task(test_id=test_id, task_id=task_id, running=running)
