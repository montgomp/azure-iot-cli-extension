# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.shared import TaskType


def create(test_id, type=TaskType.QueueTestRun, monitor=False, monitor_interval=3):
    # call POST to /deviceTests/{devicetestId}/tasks
    return True


def delete(test_id, task_id):
    # call DELETE to /deviceTests/{deviceTestId}/tasks/{taskId}
    return True


def show(test_id, task_id=None, running=False):
    # if task_id then GET /deviceTests/{deviceTestId}/tasks/{taskId}
    # else if running the GET /deviceTests/{deviceTestId}/tasks/running
    # else throw
    return True
