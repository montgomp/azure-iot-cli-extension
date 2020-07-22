# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from azure.cli.testsdk import LiveScenarioTest


class TestProductDeviceTestTasks(LiveScenarioTest):
    def __init__(self, _):
        super(TestProductDeviceTestTasks, self).__init__(_)
        self.kwargs.update(
            {"device_test_id": "4afc5755-3167-4c72-84f5-14b136e376e0"}
        )

    def setup(self):
        return True

    def teardown(self):
        return True

    def test_product_device_test_tasks(self):

        # create task
        created = self.cmd(
            "iot product test task create -t {device_test_id}"
        ).get_output_in_json()
        assert created["deviceTestId"] == self.kwargs["device_test_id"]
        assert json.dumps(created)

        test_task_id = created["id"]
        self.kwargs.update({"device_test_task_id": test_task_id})

        # show task
        show = self.cmd(
            "iot product test task show -t {device_test_id} --task-id {device_test_task_id}"
        ).get_output_in_json()
        assert json.dumps(show)
        assert show["deviceTestId"] == self.kwargs["device_test_id"]
        assert show["id"] == self.kwargs["device_test_task_id"]

        # show running tasks
        show = self.cmd("iot product test task show -t {device_test_id} --running")

        # error - show requires task-id or --running
        show = self.cmd(
            "iot product test task show -t {device_test_id}", expect_failure=True
        )

        # delete test task
        self.cmd(
            "iot product test task delete -t {device_test_id} --task-id {device_test_task_id}"
        )
