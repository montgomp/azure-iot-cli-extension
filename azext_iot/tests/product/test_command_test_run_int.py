# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from azure.cli.testsdk import LiveScenarioTest
from azext_iot.product.shared import TaskType


class TestProductDeviceTestRuns(LiveScenarioTest):
    def __init__(self, _):
        super(TestProductDeviceTestRuns, self).__init__(_)
        self.kwargs.update(
            {
                "device_test_id": "3beb0e67-33d0-4896-b69b-91c7b7ce8fab",
                "generate_task": TaskType.GenerateTestCases.value,
                "run_task": TaskType.QueueTestRun.value,
            }
        )

    def setup(self):
        # setup test runs
        gen_task_id = self.cmd(
            "iot product test task create -t {device_test_id} --type {generate_task} --wait"
        ).get_output_in_json()["id"]
        queue_task_id = self.cmd(
            "iot product test task create -t {device_test_id} --type {run_task} --wait"
        ).get_output_in_json()["id"]
        self.kwargs.update(
            {"generate_task_id": gen_task_id, "queue_task_id": queue_task_id}
        )

    def teardown(self):
        self.cmd(
            "iot product test task delete -t {device_test_id} --task-id {generate_task_id}"
        )
        self.cmd(
            "iot product test task delete -t {device_test_id} --task-id {queue_task_id}"
        )

    def test_product_device_test_run(self):
        # get latest test run
        latest = self.cmd(
            "iot product test run show -t {device_test_id}"
        ).get_output_in_json()
        run_id = latest["id"]
        self.kwargs.update({"test_run_id": run_id})
        specific = self.cmd(
            "iot product test run show -t {device_test_id} -r {test_run_id}"
        ).get_output_in_json()

        assert latest == specific

        # bad test/run id
        self.cmd(
            "iot product test run show -t bad_test_id -r bad_run_id",
            expect_failure=True,
        )

        # submit (currently cannot submit failed test)
        self.cmd(
            "iot product test run submit -t {device_test_id} -r {test_run_id}",
            expect_failure=True,
        )
