# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from time import sleep
from azext_iot.product.shared import TaskType, DeviceTestTaskStatus as Status
from azext_iot.product.providers.aics import AICSProvider
from knack.util import CLIError


def create(
    cmd, test_id, task_type=TaskType.QueueTestRun.value, wait=False, poll_interval=3
):
    ap = AICSProvider(cmd)
    final_statuses = [
        Status.failed.value,
        Status.completed.value,
        Status.cancelled.value,
    ]
    response = ap.create_test_task(
        test_id=test_id, task_type=task_type, wait=wait, poll_interval=poll_interval
    )
    if not response:
        raise CLIError(
            "Failed to create device test task - please ensure a device test exists with Id {}".format(
                test_id
            )
        )
    status = response.status
    task_id = response.id
    while all([wait, status, task_id]) and status not in final_statuses:
        sleep(poll_interval)
        response = ap.show_test_task(test_id=test_id, task_id=task_id)
        status = response.status

    # if a task of 'queueTestRun' is awaited, return the run results
    if all(
        [
            wait,
            status in final_statuses,
            task_type == TaskType.QueueTestRun.value,
            response.result_link
        ]
    ):
            run_id = response.result_link.split('/')[-1]
            return ap.show_test_run(test_id=test_id, run_id=run_id) if run_id else response

    return response


def delete(cmd, test_id, task_id):
    ap = AICSProvider(cmd)
    return ap.delete_test_task(test_id=test_id, task_id=task_id)


def show(cmd, test_id, task_id=None, running=False):
    ap = AICSProvider(cmd)
    if task_id:
        return ap.show_test_task(test_id=test_id, task_id=task_id)
    elif running:
        return ap.show_running_test_task(test_id=test_id)
    raise CLIError(
        "Please provide a task-id for individual task details, or use the --running argument to list all running tasks"
    )
