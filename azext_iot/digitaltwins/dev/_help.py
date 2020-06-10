# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Help definitions for Azure Digital Twins local development CLI.
"""

from knack.help_files import helps


def load_help():
    helps["dt dev"] = """
        type: group
        short-summary: Manage the local development Digital Twin entities.
    """

    helps["dt dev init"] = """
        type: command
        short-summary: Initialize the current folder with settings and components to help create your Digital Twins Solution.
        examples:
        - name: Basic usage
          text: >
            az dt dev init --dt-name {name}
        - name: Basic usage with boilerplate code for a smart building solution.
          text: >
            az dt dev init --dt-name {name} --template SmartBuilding
        - name: Usage with specifying Resource Group.
          text: >
            az dt dev init --dt-name {name} --resource-group {resource_group}
        - name: Usage with specifying Region.
          text: >
            az dt dev init --dt-name {name} --location {location}
        - name: Complex usage specifying region, resource group, and template
          text: >
            az dt dev init --dt-name {name} --resource-group {resource_group} --location {location} --template SmartBuilding
    """

    helps["dt dev model"] = """
        type: group
        short-summary: Manage DTDL models in the solution.
    """

    helps["dt dev model create"] = """
        type: command
        short-summary: Creates a Digital Twins Definition Language (DTDL) file in the Models folder.
        examples:
        - name: Basic usage
          text: >
            az dt dev model create --model-name {model_name}
    """

    helps["dt dev model delete"] = """
        type: command
        short-summary: Removes a Digital Twins Definition Language (DTDL) file from the Models folder.
        examples:
        - name: Basic usage
          text: >
            az dt dev model delete --model-name {model_name}
    """

    helps["dt dev model telemetry"] = """
        type: group
        short-summary: Create or delete telementry contents from the DTDL model.
    """

    helps["dt dev model telemetry create"] = """
        type: command
        short-summary: Creates a Telemetry definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model telemetry create --model-name {model_name} --telemetry-name {telemetry_name} --schema {schema}
    """

    helps["dt dev model telemetry delete"] = """
        type: command
        short-summary: Removes a Telemetry definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model telemetry delete --model-name {model_name} --telemetry-name {telemetry_name}
    """

    helps["dt dev model property"] = """
        type: group
        short-summary: Create or delete property contents from the DTDL model.
    """

    helps["dt dev model property create"] = """
        type: command
        short-summary: Creates a Property definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model property create --model-name {model_name} --property-name {property_name} --schema {schema}
    """

    helps["dt dev model property delete"] = """
        type: command
        short-summary: Removes a Property definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model property delete --model-name {model_name} --property-name {property_name}
    """

    helps["dt dev model relationship"] = """
        type: group
        short-summary: Create or delete relationship contents from the DTDL model.
    """

    helps["dt dev model relationship create"] = """
        type: command
        short-summary: Creates a relationship definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model relationship create
              --model-name {model_name}
              --relationship-name {relationship_name}
              --target {target}
    """

    helps["dt dev model relationship delete"] = """
        type: command
        short-summary: Removes a Relationship definition in the specified model contents.
        examples:
        - name: Basic usage
          text: >
            az dt dev model relationship delete --model-name {model_name} --relationship-name {relationship_name}
    """

    helps["dt dev build"] = """
        type: command
        short-summary: Compiles a deployment payload into the ./dist folder for later deployment to Azure.
        examples:
        - name: Basic usage
          text: >
            az dt dev build
    """

    helps["dt dev deploy"] = """
        type: command
        short-summary: Runs the compiled deployment to create/update the specified Azure Digital Twin resource.
        examples:
        - name: Basic usage
          text: >
            az dt dev deploy
        - name: Usage with named configuration/variable set.
          text: >
            az dt dev deploy --config {configuration_name}
    """

    helps["dt dev twin"] = """
        type: group
        short-summary: Manage twin instances in the Digital Twins solution graph.
    """

    helps['dt dev twin create'] = """
        type: command
        short-summary: Creates a twin instance in the solution graph with specified properties.
        examples:
        - name: Basic usage
          text: >
            az dt dev twin create --dtmi {dtmi} --twin-id {twin_id}
        - name: Basic usage with properties
          text: >
            az dt dev twin create --dtmi {dtmi} --twin-id {twin_id} --properties {properties}
    """
    helps["dt dev twin delete"] = """
        type: command
        short-summary: Removes a twin instance from the solution graph.
        examples:
        - name: Basic usage
          text: >
            az dt dev twin delete --twin-id {twin_id}
    """

    helps["dt dev twin relationship"] = """
        type: group
        short-summary: Create or delete relationships twin instances.
    """

    helps["dt dev twin relationship create"] = """
        type: command
        short-summary: Creates a relationship of the given name between the specified twins.
        examples:
        - name: Basic usage
          text: >
            az dt dev twin relationship create
              --twin-id {twin_id}
              --relationship-name {relationship_name}
              --related-id {related_id}
    """
    helps["dt dev twin relationship delete"] = """
        type: command
        short-summary: Removes a relationship of the given name between the specified twins.
        examples:
        - name: Basic usage
          text: >
            az dt dev twin relationship delete
              --twin-id {twin_id}
              --relationship-name {relationship_name}
              --related-id {related_id}
    """
# Endpoints
    helps["dt dev endpoint"] = """
      type: group
      short-summary: Manage endpoint configurations for the Digital Twins solution.
    """
    helps["dt dev endpoint eventgrid"] = """
      type: group
      short-summary: Manage EventGrid Topic endpoint configurations for the Digital Twins solution.
    """
    helps["dt dev endpoint eventgrid create"] = """
      type: command
      short-summary: Create an EventGrid Topic endpoint configuration for the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint eventgrid create --endpoint-name {endpoint_name}
          --eventgrid-topic {eventgrid_topic_name}
    """
    helps["dt dev endpoint eventgrid delete"] = """
      type: command
      short-summary: Remove an EventGrid Topic endpoint configuration from the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint eventgrid delete --endpoint-name {endpoint_name}
      - name: Remove routes
        text: >
          az dt dev endpoint eventgrid delete --endpoint-name {endpoint_name} --remove-routes
    """
    helps["dt dev endpoint eventhub"] = """
      type: group
      short-summary: Manage EventHub endpoint configurations for the Digital Twins solution.
    """
    helps["dt dev endpoint eventhub create"] = """
      type: command
      short-summary: Create an EventHub endpoint configuration for the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint eventhub create --endpoint-name {endpoint_name}
          --eventhub-namespace {eventhub_namespace}
          --eventhub {eventhub_name}
          --eventhub-policy {eventhub_policy}
    """
    helps["dt dev endpoint eventhub delete"] = """
      type: command
      short-summary: Remove an EventHub endpoint configuration from the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint eventhub delete --endpoint-name {endpoint_name}
      - name: Remove routes
        text: >
          az dt dev endpoint eventhub delete --endpoint-name {endpoint_name} --remove-routes
    """
    helps["dt dev endpoint servicebus"] = """
      type: group
      short-summary: Manage ServiceBus Topic endpoint configurations for the Digital Twins solution.
    """
    helps["dt dev endpoint servicebus create"] = """
      type: command
      short-summary: Create a ServiceBus Topic endpoint configuration for the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint servicebus create --endpoint-name {endpoint_name}
          --servicebus-namespace {servicebus_namespace}
          --servicebus-topic {servicebus_topic_name}
          --servicebus-policy {servicebus_policy}
    """
    helps["dt dev endpoint servicebus delete"] = """
      type: command
      short-summary: Remove a ServiceBus Topic endpoint configuration from the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev endpoint servicebus delete --endpoint-name {endpoint_name}
      - name: Remove routes
        text: >
          az dt dev endpoint servicebus delete --endpoint-name {endpoint_name} --remove-routes
    """

    helps["dt dev route"] = """
      type: group
      short-summary: Manage route configurations for the Digital Twins solution.
    """

    helps["dt dev route create"] = """
      type: command
      short-summary: Create a route configuration for the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt route create --route-name {route_name}
          --endpoint-name {endpoint_name}
      - name: Usage with filter
        text: >
          az dt route create --route-name {route_name}
          --endpoint-name {endpoint_name}
          --filter "type = 'Microsoft.DigitalTwins.Twin.Create'"
    """

    helps["dt dev route delete"] = """
      type: command
      short-summary: Remove a route configuration from the Digital Twins solution.

      examples:
      - name: Basic usage
        text: >
          az dt dev route delete --route-name {route_name}
    """
