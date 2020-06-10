# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import CliCommandType

dtdev_ops = CliCommandType(
    operations_tmpl='azext_iot.digitaltwins.dev.main#{}'
)

dtdev_model_ops = CliCommandType(
    operations_tmpl='azext_iot.digitaltwins.dev.models#{}'
)

dtdev_twin_ops = CliCommandType(
    operations_tmpl='azext_iot.digitaltwins.dev.twins#{}'
)

dtdev_endpoint_ops = CliCommandType(
    operations_tmpl='azext_iot.digitaltwins.dev.endpoints#{}'
)

dtdev_route_ops = CliCommandType(
    operations_tmpl='azext_iot.digitaltwins.dev.routes#{}'
)


def load_commands(self, _):
    with self.command_group('dt dev', command_type=dtdev_ops) as g:
        g.command('init', 'init_workspace')
        g.command('build', 'build_workspace')
        g.command('deploy', 'deploy_workspace')

    with self.command_group('dt dev model', command_type=dtdev_model_ops) as g:
        g.command('create', 'create')
        g.command('delete', 'delete')

    with self.command_group('dt dev model property', command_type=dtdev_model_ops) as g:
        g.command('create', 'createProperty')
        g.command('delete', 'deleteProperty')

    with self.command_group('dt dev model relationship', command_type=dtdev_model_ops) as g:
        g.command('create', 'createRelationship')
        g.command('delete', 'deleteRelationship')

    with self.command_group('dt dev model telemetry', command_type=dtdev_model_ops) as g:
        g.command('create', 'createTelemetry')
        g.command('delete', 'deleteTelemetry')

    with self.command_group('dt dev twin', command_type=dtdev_twin_ops) as g:
        g.command('create', 'create')
        g.command('delete', 'delete')

    with self.command_group('dt dev twin relationship', command_type=dtdev_twin_ops) as g:
        g.command('create', 'createRelationship')
        g.command('delete', 'deleteRelationship')

    with self.command_group('dt dev endpoint', command_type=dtdev_endpoint_ops) as g:
        g.command('delete', 'delete_endpoint')

    with self.command_group('dt dev endpoint eventgrid', command_type=dtdev_endpoint_ops) as g:
        g.command('create', 'create_eventgrid')
        g.command('delete', 'delete_endpoint')  # aliased for consistency
    with self.command_group('dt dev endpoint eventhub', command_type=dtdev_endpoint_ops) as g:
        g.command('create', 'create_eventhub')
        g.command('delete', 'delete_endpoint')  # aliased for consistency
    with self.command_group('dt dev endpoint servicebus', command_type=dtdev_endpoint_ops) as g:
        g.command('create', 'create_servicebus')
        g.command('delete', 'delete_endpoint')  # aliased for consistency

    with self.command_group('dt dev route', command_type=dtdev_route_ops) as g:
        g.command('create', 'create_route')
        g.command('delete', 'delete_route')
