# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.digitaltwins.dev.main import read_JSON_file, write_JSON_file
from azext_iot.digitaltwins.dev.constants import CONFIG_FILE
from knack.util import CLIError


def delete_endpoint(endpoint_name, remove_routes=False):
    config_data = read_JSON_file(CONFIG_FILE)

    if "endpoints" not in config_data:
        return
    endpoint_data = config_data["endpoints"]

    if not any("@id" in item and endpoint_name == item["@id"] for item in endpoint_data):
        return
    endpoint_data = list(filter(lambda item: ("@id" in item and item["@id"] != endpoint_name), endpoint_data))
    config_data['endpoints'] = endpoint_data
    write_JSON_file(CONFIG_FILE, config_data)


def create_eventgrid(endpoint_name, eventgrid_topic, eventgrid_resource_group=None, force=False):
    config_data = read_JSON_file(CONFIG_FILE)

    if "endpoints" not in config_data:
        config_data["endpoints"] = []
    endpoint_data = config_data["endpoints"]

    if any("@id" in item and endpoint_name == item["@id"] for item in endpoint_data) and not force:
        raise CLIError('An endpoint with that id already exists. Use --force to overwrite')
    endpoint_data = list(filter(lambda item: ("@id" in item and item["@id"] != endpoint_name), endpoint_data))
    endpoint_data.append({
        '@id': endpoint_name,
        'resource_group': eventgrid_resource_group,
        'eventgrid_topic': eventgrid_topic,
        '@type': 'event_grid'
    })
    config_data['endpoints'] = endpoint_data
    write_JSON_file(CONFIG_FILE, config_data)


def create_eventhub(endpoint_name, eventhub_namespace, eventhub, eventhub_policy, eventhub_resource_group=None, force=False):
    config_data = read_JSON_file(CONFIG_FILE)

    if "endpoints" not in config_data:
        config_data["endpoints"] = []
    endpoint_data = config_data["endpoints"]

    if any("@id" in item and endpoint_name == item["@id"] for item in endpoint_data) and not force:
        raise CLIError('An endpoint with that id already exists. Use --force to overwrite')
    endpoint_data = list(filter(lambda item: ("@id" in item and item["@id"] != endpoint_name), endpoint_data))
    endpoint_data.append({
        '@id': endpoint_name,
        'resource_group': eventhub_resource_group,
        'eventhub_namespace': eventhub_namespace,
        'eventhub': eventhub,
        'eventhub_policy': eventhub_policy,
        '@type': 'event_hub'
    })
    config_data['endpoints'] = endpoint_data
    write_JSON_file(CONFIG_FILE, config_data)


def create_servicebus(
    endpoint_name,
    servicebus_namespace,
    servicebus_topic,
    servicebus_policy,
    servicebus_resource_group=None,
    force=False
):
    config_data = read_JSON_file(CONFIG_FILE)

    if "endpoints" not in config_data:
        config_data["endpoints"] = []
    endpoint_data = config_data["endpoints"]

    if any("@id" in item and endpoint_name == item["@id"] for item in endpoint_data) and not force:
        raise CLIError('An endpoint with that id already exists. Use --force to overwrite')
    endpoint_data = list(filter(lambda item: ("@id" in item and item["@id"] != endpoint_name), endpoint_data))
    endpoint_data.append({
        '@id': endpoint_name,
        'resource_group': servicebus_resource_group,
        'servicebus_namespace': servicebus_namespace,
        'servicebus_topic': servicebus_topic,
        'servicebus_policy': servicebus_policy,
        '@type': 'service_bus'
    })
    config_data['endpoints'] = endpoint_data
    write_JSON_file(CONFIG_FILE, config_data)
