# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.digitaltwins.dev.main import read_JSON_file, write_JSON_file
from azext_iot.digitaltwins.dev.constants import CONFIG_FILE
from knack.util import CLIError


def create_route(route_name, endpoint_name, route_filter="true", force=False):
    config_data = read_JSON_file(CONFIG_FILE)
    if "routes" not in config_data:
        config_data["routes"] = []
    route_data = config_data["routes"]

    if any("@id" in item and route_name == item["@id"] for item in route_data) and not force:
        raise CLIError("A route with that id already exists. Use --force to overwrite.")

    route_data = list(filter(lambda item: ("@id" in item and item["@id"] != route_name), route_data))
    route_data.append({
        '@id': route_name,
        'endpoint_name': endpoint_name,
        'filter': route_filter
    })

    config_data["routes"] = route_data
    write_JSON_file(CONFIG_FILE, config_data)


def delete_route(route_name):
    config_data = read_JSON_file(CONFIG_FILE)
    if "routes" not in config_data:
        return

    if not any("@id" in item and route_name == item["@id"] for item in config_data["routes"]):
        return
    route_data = list(filter(lambda item: ("@id" in item and item["@id"] != route_name), config_data["routes"]))
    config_data["routes"] = route_data
    write_JSON_file(CONFIG_FILE, config_data)
