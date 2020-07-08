# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
CLI parameter definitions.
"""

from azure.cli.core.commands.parameters import get_three_state_flag

def load_device_certification_arguments(self, _):
    with self.argument_context('iot device-certification') as c:
        c.argument('test_id',
            options_list=['--test-id'],
            help='The Id of the Microsoft.Azure.IoT.TestKit.Models.DeviceTest',
            arg_group='IoT Device Certification'
        )
    with self.argument_context('iot device-certification test-task') as c:
        c.argument('task_id',
            options_list=['--task-id'],
            help='The Id of the Microsoft.Azure.IoT.TestKit.Models.DeviceTestTask',
            arg_group='IoT Device Certification'
        )
        c.argument('running',
            options_list=['--running'],
            help='Get the running tasks of a device test',
            arg_group='IoT Device Certification',
            arg_type=get_three_state_flag()
        )
    with self.argument_context('iot device-certification test-run') as c:
        c.argument('run_id',
            options_list=['--run-id'],
            help='The Id of a Microsoft.Azure.IoT.TestKit.Models.TestRun',
            arg_group='IoT Device Certification'
        )
        c.argument('latest',
            options_list=['--latest'],
            help='Retrieve the latest test runs',
            arg_group='IoT Device Certification',
            arg_type=get_three_state_flag()
        )
