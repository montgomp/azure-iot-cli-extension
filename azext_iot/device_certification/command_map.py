# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Load CLI commands
"""
from azure.cli.core.commands import CliCommandType

requirements_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_requirements#{}'
)

tests_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_tests#{}'
)

test_tasks_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_tasks#{}'
)

test_cases_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_cases#{}'
)

test_runs_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_runs#{}'
)

def load_device_certification_commands(self, _):
    with self.command_group(
        'iot device-certification requirements',
        command_type=requirements_ops
    ) as g:
        g.command('list', 'list')

    with self.command_group(
        'iot device-certification tests',
        command_type=tests_ops
    ) as g:
        g.command('create', 'create')
        g.command('update', 'update')
        g.command('show', 'show')
        g.command('search', 'search')
    with self.command_group(
        'iot device-certification test-tasks',
        command_type=tests_ops
    ) as g:
        g.command('create', 'create')
        g.command('delete', 'delete')
        g.command('list', 'list')
    with self.command_group(
        'iot device-certification test-runs',
        command_type=tests_ops
    ) as g:
        g.command('show', 'show')
        g.command('create', 'create')