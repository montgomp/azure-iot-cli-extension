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
    operations_tmpl='azext_iot.device_certification.command_requirement#{}'
)

tests_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test#{}'
)

test_tasks_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_task#{}'
)

test_cases_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_case#{}'
)

test_runs_ops = CliCommandType(
    operations_tmpl='azext_iot.device_certification.command_test_run#{}'
)


def load_device_certification_commands(self, _):
    with self.command_group(
        'iot device-certification requirement',
        command_type=requirements_ops
    ) as g:
        g.command('list', 'list')

    with self.command_group(
        'iot device-certification test',
        command_type=tests_ops
    ) as g:
        g.command('init', 'initialize_workspace')
        g.command('create', 'create')
        g.command('update', 'update')
        g.command('show', 'show')
        g.command('search', 'search')
    with self.command_group(
        'iot device-certification test-case',
        command_type=test_cases_ops
    ) as g:
        g.command('list', 'list')
        g.command('update', 'update')
    with self.command_group(
        'iot device-certification test-task',
        command_type=test_tasks_ops
    ) as g:
        g.command('create', 'create')
        g.command('delete', 'delete')
        g.command('show', 'show')
    with self.command_group(
        'iot device-certification test-run',
        command_type=test_runs_ops
    ) as g:
        g.command('show', 'show')
        g.command('create', 'create')
