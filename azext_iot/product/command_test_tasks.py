# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from time import sleep
from azext_iot.product.shared import TaskType, DeviceTestTaskStatus as Status
from azext_iot.product.providers.provider import get_sdk
from azext_iot.common.utility import unpack_msrest_error
from msrestazure.azure_exceptions import CloudError
from knack.util import CLIError


def create(cmd, test_id, task_type=TaskType.QueueTestRun, wait=False, poll_interval=3):
    final_statuses = [
        Status.failed.value,
        Status.completed.value,
        Status.cancelled.value,
    ]
    status = None
    try:
        response = get_sdk(cmd).create_device_test_task(
            device_test_id=test_id, task_type=task_type
        )
        status = response.status
        task_id = response.id
        while all([wait, status, task_id]) and status not in final_statuses:
            sleep(poll_interval)
            response = get_sdk(cmd).get_device_test_task(
                task_id=task_id, device_test_id=test_id
            )
            status = response.status
        return response
    except CloudError as e:
        return CLIError(unpack_msrest_error(e))


def delete(cmd, test_id, task_id):
    try:
        return get_sdk(cmd).cancel_device_test_task(
            task_id=task_id, device_test_id=test_id
        )
    except CloudError as e:
        return CLIError(unpack_msrest_error(e))


def show(cmd, test_id, task_id=None, running=False):
    try:
        if task_id:
            return get_sdk(cmd).get_device_test_task(
                task_id=task_id, device_test_id=test_id
            )
        elif running:
            return get_sdk(cmd).get_running_device_test_tasks(device_test_id=test_id)
        else:
            raise CLIError(
                "Please provide a task-id for individual task details, or use the --running argument to list all running tasks"
            )
    except CloudError as e:
        return CLIError(unpack_msrest_error(e))
