# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
CLI parameter definitions for Azure Digital Twins developer plane CLI.
"""

from azure.cli.core.commands.parameters import get_three_state_flag
from azext_iot.digitaltwins.dev.main import DeploymentStrategy
from azure.cli.core.commands.parameters import get_enum_type


def load_dt_dev_arguments(self, _):
    with self.argument_context('dt dev init') as c:  # Init
        c.argument('template', options_list=['--template', '-t'],
                   help='Optionally download a pre-configured solution from GitHub.')
        c.argument('force', help='Overwrite any existing config.json and twins.json')

# Deploy
    with self.argument_context('dt dev deploy') as c:
        c.argument(
            'config',
            help='Specify a configuration name defined in {config}.config.json containing overrides to base configuration'
        )
        c.argument('file_name', help="Zipped deployment file to extract and deploy.")
        c.argument('working_folder', help="Folder to contain unzipped deployment.")
        c.argument(
            'deployment_strategy',
            options_list=['--deployment-strategy, --ds'],
            help="Specifies the deployment strategy.",
            arg_type=get_enum_type(DeploymentStrategy)
        )

# Models
    with self.argument_context('dt dev model') as c:
        c.argument('model_name',
                   options_list=['--model-name', '--mn'],
                   help='The name of the DTDL model')
        c.argument('display_name',
                   options_list=['--display-name', '--dn'],
                   help="A display value for consuming applications")
        c.argument('schema',
                   options_list=['--schema', '-s'],
                   help='The simple schema type of the content. Complex types must be modeled manually')

    with self.argument_context('dt dev model property') as c:
        c.argument('property_name',
                   options_list=['--property-name', '--pn'],
                   help='The name of the property definition')
        c.argument('writable',
                   options_list=['--writable', '-w'],
                   help='Specifies that this is a property that can be set from the cloud',
                   arg_type=get_three_state_flag())
        c.argument('force',
                   help='Overwrite any existing property matching --model-name and --property-name')

    with self.argument_context('dt dev model relationship') as c:
        c.argument('relationship_name',
                   options_list=['--relationship-name', '--rn'],
                   help='The name of the relationship definition')
        c.argument('target',
                   options_list=['--target', '-t'],
                   help='Specifies the model type constraints for the related twin')
        c.argument('force',
                   help='Overwrite any existing relationship matching --model-name and --relationship-name')

    with self.argument_context('dt dev model telemetry') as c:
        c.argument('telemetry_name',
                   options_list=['--telemetry-name', '--tn'],
                   help='The name of the telemetry definition')
        c.argument('force',
                   help='Overwrite any existing telemetry matching --model-name and --telemetry-name')

    with self.argument_context('dt dev model create') as c:
        c.argument('force',
                   help='Overwrite any existing DTDL matching --model-name')

# Twins
    with self.argument_context('dt dev twin') as c:
        c.argument('twin_id',
                   options_list=['--twin-id', '-t'],
                   help="The twin unique identifier for the Digital Twin solution")
        c.argument('model',
                   options_list=['--model-id', '--dtmi', '-m'],
                   help="The Digital Twin Model Identifier (DTMI, '@id') for the model definition")
        c.argument('properties',
                   options_list=['--properties', '-p'],
                   help="JSON payload for assigning simple values to twin properties")
        c.argument('force',
                   help='Overwrite any existing twin matching --twin-id')
        c.argument('related_id',
                   options_list=['--related-id', '-r'],
                   help="The twin unique identifier of the related twin")
        c.argument('relationship_name',
                   options_list=["--relationship", "--kind"],
                   help="Relationship name or kind. For example: 'contains'")
        c.argument('remove_empty',
                   options_list=['--remove-empty', '--re'],
                   help="Removes empty nodes and arrays",
                   arg_type=get_three_state_flag())
# Endpoint
    with self.argument_context('dt dev endpoint') as c:
        c.argument(
            "remove_routes",
            options_list=["--remove-routes"],
            help="Remove any route configuration that references --endpoint-name within config.json",
            arg_type=get_three_state_flag()
        )
    with self.argument_context('dt dev endpoint eventgrid') as c:
        c.argument(
            "eventgrid_topic",
            options_list=["--eventgrid-topic", "--egt"],
            help="Name of EventGrid Topic to integrate with.",
            arg_group="Event Grid Topic",
        )
        c.argument(
            "eventgrid_resource_group",
            options_list=["--eventgrid-resource-group", "--egg"],
            help="Name of EventGrid Topic resource group.",
            arg_group="Event Grid Topic",
        )
        c.argument(
            "force",
            help="Overwrite any existing EventGrid endpoint with matching --endpoint-name within config.json"
        )

    with self.argument_context('dt dev endpoint eventhub') as c:
        c.argument(
            "eventhub",
            options_list=["--eventhub", "--eh"],
            help="Name of EventHub to integrate with.",
            arg_group="Event Hub",
        )
        c.argument(
            "eventhub_policy",
            options_list=["--eventhub-policy", "--ehp"],
            help="EventHub policy to use for endpoint configuration.",
            arg_group="Event Hub",
        )
        c.argument(
            "eventhub_namespace",
            options_list=["--eventhub-namespace", "--ehn"],
            help="EventHub Namespace identifier.",
            arg_group="Event Hub",
        )
        c.argument(
            "eventhub_resource_group",
            options_list=["--eventhub-resource-group", "--ehg"],
            help="Name of EventHub resource group.",
            arg_group="Event Hub",
        )
        c.argument(
            "force",
            help="Overwrite any existing EventHub endpoint with matching --endpoint-name within config.json"
        )

    with self.argument_context('dt dev endpoint servicebus') as c:
        c.argument(
            "servicebus_topic_name",
            options_list=["--servicebus-topic", "--sbt"],
            help="Name of ServiceBus Topic to integrate with.",
            arg_group="Service Bus Topic",
        )
        c.argument(
            "servicebus_policy",
            options_list=["--servicebus-policy", "--sbp"],
            help="ServiceBus Topic policy to use for endpoint configuration.",
            arg_group="Service Bus Topic",
        )
        c.argument(
            "servicebus_namespace",
            options_list=["--servicebus-namespace", "--sbn"],
            help="ServiceBus Namespace identifier.",
            arg_group="Service Bus Topic",
        )
        c.argument(
            "servicebus_resource_group",
            options_list=["--servicebus-resource-group", "--sbg"],
            help="Name of ServiceBus resource group.",
            arg_group="Service Bus Topic",
        )
        c.argument(
            "force",
            help="Overwrite any existing ServiceBus endpoint with matching --endpoint-name within config.json"
        )
# Routes
    with self.argument_context('dt dev route') as c:
        c.argument(
            "route_filter",
            options_list=["--filter"],
            help="Route filter"
        )
        c.argument(
            "force",
            help="Overwrite any existing route with matching --route-name within config.json"
        )
