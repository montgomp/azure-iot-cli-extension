# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import six
import os
import shutil
import zipfile
from knack.util import CLIError
from azext_iot.digitaltwins.dev.constants import CONFIG_FILE, DIST_FILE, DIST_FOLDER, MODELS_FOLDER, MODELS_EXTENSION, TWINS_FILE, COOL_OFF
from azext_iot.digitaltwins.dev.template import activate_template
from azext_iot.digitaltwins.commands_resource import (
    create_instance,
    show_instance,
    delete_instance,
    add_endpoint_eventgrid,
    add_endpoint_eventhub,
    add_endpoint_servicebus
)
from azext_iot.digitaltwins.commands_models import add_models
from azext_iot.digitaltwins.commands_twins import create_twin, create_relationship
from azext_iot.digitaltwins.commands_routes import create_route
from enum import Enum
from time import sleep

class DeploymentStrategy(Enum):
    Append = "Append"
    Overwrite = "Overwrite"
    Safe = "Safe"


def init_workspace(cmd, name=None, resource_group_name=None, location=None, template=None, force=False):
    six.print_("Initializing workspace")
    get_models_folder_path()
    write_JSON_file(TWINS_FILE, [])
    build_config_file(name, resource_group_name, location, force)

    if template:
        activate_template(template)

    six.print_("Use az dt dev --help to get more information on building models, twins, and endpoints")


def build_config_file(name, resource_group_name, location, force):
    config_path = os.path.join('.', CONFIG_FILE)

    if os.path.exists(config_path):
        if not force:
            raise CLIError(
                'Configuration file found at "{}" already exists. Please use \'--force\' to overwrite.'.format(config_path))

    write_JSON_file(config_path, {
        'name': name,
        'resourceGroup': resource_group_name,
        'location': location
    })


def write_JSON_file(file, contents):
    with open(file, 'w+', encoding='utf-8')as f:
        json.dump(contents, f, indent=4, sort_keys=True)


def build_endpoints(config_data):
    if "endpoints" not in config_data:
        six.print_("No endpoints specified")
        return
    for endpoint in config_data["endpoints"]:
        if "@id" not in endpoint:
            raise CLIError("One or more endpoints are missing @id")
        if "@type" not in endpoint:
            raise CLIError("Endpoint '{}' is missing @type".format(endpoint["@id"]))
        if (endpoint["@type"] == "event_grid"):
            if "eventgrid_topic" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for eventgrid_topic".format(endpoint["@id"]))
        elif (endpoint["@type"] == "event_hub"):
            if "eventhub" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for eventhub".format(endpoint["@id"]))
            if "eventhub_policy" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for eventhub_policy".format(endpoint["@id"]))
        elif (endpoint["@type"] == "service_bus"):
            if "servicebus_namespace" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for servicebus_namespace".format(endpoint["@id"]))
            if "servicebus_topic" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for servicebus_topic".format(endpoint["@id"]))
            if "servicebus_policy" not in endpoint:
                raise CLIError("Endpoint '{}' is missing required configuration for servicebus_policy".format(endpoint["@id"]))


def build_routes(config_data):
    if "routes" not in config_data:
        six.print_("No routes configured")
        return
    six.print_('Building routes')
    route_data = config_data["routes"]
    if "endpoints" not in config_data and len(route_data) > 0:
        raise CLIError("No endpoints configured for specified routes")

    # get known endpoints to make sure all routes have their endpoint configured
    known_endpoints = list(map(lambda item: (item["@id"]), config_data["endpoints"]))
    for route in route_data:
        if "@id" not in route:
            raise CLIError("One or more routes are missing id property")
        if "endpoint_name" not in route:
            raise CLIError("Endpoint not specified in route {}".format(route["@id"]))
        if route["endpoint_name"] not in known_endpoints:
            raise CLIError(
                "Endpoint '{}' is required for route '{}' and is not configured.".format(
                    route["endpoint_name"], route["@id"]))


def build_models():
    six.print_('Building models')
    known_models = []
    needed_models = {}

    for root, dirs, files in os.walk(MODELS_FOLDER):
        for dir in dirs:
            os.mkdir(os.path.join(DIST_FOLDER, root, dir))
        for model_file in files:
            if not model_file.endswith(MODELS_EXTENSION):
                continue
            model = read_JSON_file(os.path.join(root, model_file))

            if '@id' in model:
                six.print_('Found model "{}"'.format(model['@id']))
                if model['@id'] not in known_models:
                    known_models.append(model['@id'])
            else:
                six.print_(model)
                raise CLIError('Malformed model {}. Missing "@id" property in root.'.format(model_file))

    # Add check for any interface inheritance
            if 'extends' in model:
                extending = model['extends']
                needed_models = extend_needed_models(needed_models, extending, model['@id'], model_file)
    # Start checks of actual interface contents
            if 'contents' not in model:
                raise CLIError('Malformed models {}. Missing "contents" property in root.'.format(model_file))
            else:
                for content in model['contents']:
                    if '@type' not in content:
                        raise CLIError(
                            'Malformed content "{}" in {}. Required "@type" node is missing.'.format(content, model_file)
                        )
        # Add check for required relationship interfaces
                    if content['@type'] == "Relationship":
                        if 'target' not in content:
                            raise CLIError(
                                'Malformed content "{}" in {}. Required "target" node is missing in "Relationship" type.'.format(
                                    content, model_file))
                        else:
                            needed_models = extend_needed_models(needed_models, content['target'], model['@id'], model_file)
        # Add check for required component interfaces
                    elif content['@type'] == "Component":
                        if 'schema' not in content:
                            raise CLIError(
                                'Malformed content "{}" in {}. Required "schema" node is missing in "Component" type.'.format(
                                    content,
                                    model_file))
                        else:
                            needed_models = extend_needed_models(needed_models, content['schema'], model['@id'], model_file)
        # write model file to dist folder
            write_JSON_file(os.path.join(DIST_FOLDER, root, model_file), model)

    for needed in needed_models:
        if needed not in known_models:
            raise CLIError('Model "{}" is referenced by {} and is not found.'.format(needed, needed_models[needed]))

    return known_models


def extend_needed_models(needed_models, extending, model_id, model_file):
    if extending == "*":
        return needed_models
    extended = []
    if extending in needed_models:
        extended = needed_models[extending]
    if model_file not in extended:
        extended.append(model_file)
    needed_models[extending] = extended
    six.print_('{} requires model {}'.format(model_id, extending))
    return needed_models


def build_twins(known_models):
    twin_data = read_JSON_file(TWINS_FILE)
    known_ids = []
    for twin_item in twin_data:
        if "@id" not in twin_item:
            raise CLIError('Missing required @id field in twins.json')
        twin_id = twin_item["@id"]

        if twin_id in known_ids:
            raise CLIError('Duplicate twin with @id: "{}"'.format(twin_id))

        known_ids.append(twin_id)
        if "@model" in twin_item:
            model = twin_item["@model"]
            if not known_models or model not in known_models:
                raise CLIError('Model "{}" is referenced by twin "@id":"{}" and is not found.'.format(model, twin_id))

    write_JSON_file(os.path.join(DIST_FOLDER, TWINS_FILE), twin_data)


def build_workspace(cmd):
    # make sure all anticipated folders exist
    if os.path.exists(DIST_FILE):
        six.print_("Removing previous build file {}".format(DIST_FILE))
        os.remove(DIST_FILE)
    if os.path.exists(DIST_FOLDER):
        six.print_("Removing previous build folder {}".format(DIST_FOLDER))
        shutil.rmtree(DIST_FOLDER, ignore_errors=True)

    check_create_path(DIST_FOLDER)
    check_create_path(MODELS_FOLDER)
    check_create_path(os.path.join(DIST_FOLDER, MODELS_FOLDER))

    known_models = build_models()
    build_twins(known_models)

    config_data = read_JSON_file(CONFIG_FILE)

    write_JSON_file(os.path.join(DIST_FOLDER, CONFIG_FILE), config_data)

    build_endpoints(config_data)
    build_routes(config_data)

    if "noZip" not in config_data or not config_data["noZip"]:
        zip_distribution()


def zip_distribution():
    with zipfile.ZipFile(DIST_FILE, 'w', zipfile.ZIP_DEFLATED) as dist:
        for root, dirs, files in os.walk(DIST_FOLDER):
            for name in files:
                file_name = os.path.join(root, name)
                dist.write(file_name, arcname=file_name.replace(DIST_FOLDER, ""))
        dist.close()


def extract_distribution(file_name, working_folder):
    zip = zipfile.ZipFile(file_name)
    zip.extractall(path=working_folder)


def deploy_workspace(
    cmd,
    name=None,
    file_name=DIST_FILE,
    working_folder=DIST_FOLDER,
    config=None,
    location=None,
    resource_group_name=None,
    deployment_strategy=None
):
    if os.path.exists(file_name):
        shutil.rmtree(working_folder, ignore_errors=True)  # zip will override this folder
        extract_distribution(file_name, working_folder)

    should_build = False
    if not os.path.exists(working_folder):
        if DIST_FOLDER != working_folder:
            raise CLIError("Working folder does not exist. Please rebuild and ensure value specified in --working_folder exists.")
        should_build = True  #  if it hasn't been built yet, build it
    config_data = get_configuration_data(working_folder, config)

    #  if user always wants to rebuild, build it
    should_build = should_build or ("rebuild" in config_data and "always" == config_data["rebuild"])

    if should_build:
        build_workspace(cmd)

    if location is not None:
        config_data["location"] = location
    if "location" not in config_data or config_data["location"] is None:
        raise CLIError("Location has not been specified for deployment. Please complete configuration or use --location argument")

    if resource_group_name is not None:
        config_data["resourceGroup"] = resource_group_name
    if "resourceGroup" not in config_data or config_data["resourceGroup"] is None:
        raise CLIError(
            "Resource Group has not been specified for deployment. Please complete configuration or use --resource-group argument"
        )

    if name is not None:
        config_data["name"] = name
    if "name" not in config_data:
        raise CLIError("Name has not been configured")
    if "deployment_strategy" not in config_data:
        if deployment_strategy is None:
            deployment_strategy = DeploymentStrategy.Safe
        else:
            config_data["deployment_strategy"] = deployment_strategy

    check_create_instance(cmd, config_data)

    deploy_models(cmd, config_data)
    deploy_twins(cmd, config_data)
    deploy_endpoints(cmd, config_data)
    deploy_routes(cmd, config_data)


def check_create_instance(cmd, config_data):
    instance_data = None
    try:
        instance_data = show_instance(cmd, config_data["name"], config_data["resourceGroup"])
        # do we remove the existing instance or fail here?
    except Exception:
        instance_data = None

    if instance_data is None:
        six.print_("Not found, creating")
        if "tags" in config_data:
            six.print_("With tags")
            instance_data = create_instance(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                location=config_data["location"],
                tags=config_data["tags"])
        else:
            six.print_("No tags")
            instance_data = create_instance(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                location=config_data["location"])
        sleep(COOL_OFF)
        return

    if "deployment_strategy" in config_data and config_data["deployment_strategy"] == "Overwrite":
        six.print_("Found resource, using overwrite deployment strategy. Deleting exsting instance...")
        delete_instance(
            cmd,
            name=config_data["name"],
            resource_group_name=config_data["resourceGroup"])
        six.print_("Instance {} has been deleted".format(config_data["name"]))
        sleep(COOL_OFF)
        if "location" not in config_data:
            raise CLIError("Location is not configured")

        if "tags" in config_data:
            six.print_("Recreating instance with specified tags...")
            instance_data = create_instance(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                location=config_data["location"],
                tags=config_data["tags"])
        else:
            six.print_("Recreating instance...")
            instance_data = create_instance(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                location=config_data["location"])
        sleep(COOL_OFF)
        return
    elif "deployment_strategy" not in config_data or config_data["deployment_strategy"] != "Append":
        raise CLIError("Instance has already been created and will not be changed using a safe deployment strategy.")


def deploy_twins(cmd, config_data):
    six.print_("Uploading twins")
    twins_data = read_JSON_file(os.path.join(config_data["directory"], TWINS_FILE))

    for twin in twins_data:
        twin_id = twin["@id"]
        model_id = twin["@model"]

        if "properties" in twin:
            create_twin(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                twin_id=twin_id,
                model_id=model_id,
                properties=twin["properties"]
            )
        else:
            create_twin(
                cmd,
                name=config_data["name"],
                resource_group_name=config_data["resourceGroup"],
                twin_id=twin_id,
                model_id=model_id,
            )
        if "relationships" in twin:
            for relationship in twin["relationships"]:
                for related_item in twin["relationships"][relationship]:
                    if "properties" in related_item:
                        create_relationship(
                            cmd,
                            name=config_data["name"],
                            resource_group_name=config_data["resourceGroup"],
                            source_twin_id=twin_id,
                            target_twin_id=related_item["@id"],
                            relationship_id="{}_{}_{}".format(twin_id, relationship, related_item["@id"]),
                            relationship=relationship,
                            properties=related_item["properties"]
                        )
                    else:
                        create_relationship(
                            cmd,
                            name=config_data["name"],
                            resource_group_name=config_data["resourceGroup"],
                            source_twin_id=twin_id,
                            target_twin_id=related_item["@id"],
                            relationship_id="{}_{}_{}".format(twin_id, relationship, related_item["@id"]),
                            relationship=relationship
                        )


def deploy_models(cmd, config_data):
    six.print_("Uploading models")
    models_path = os.path.join(config_data["directory"], MODELS_FOLDER)
    add_models(cmd, config_data["name"], resource_group_name=config_data["resourceGroup"], from_directory=models_path)


def deploy_endpoints(cmd, config_data):
    six.print_("Deploying endpoints")
    if "endpoints" in config_data:
        for endpoint in config_data["endpoints"]:
            if "@id" not in endpoint:
                raise CLIError("One or more endpoints are missing id property")
            endpoint_name = endpoint["@id"]
            if "@type" not in endpoint:
                raise CLIError("Endpoint '{}' is missing type property")
            endpoint_type = endpoint["@type"]

            resource_group = config_data["resourceGroup"]
            if "resource_group" in endpoint and endpoint["resource_group"]:
                resource_group = endpoint["resource_group"]

            six.print_("Deploying endpoint '{}'".format(endpoint_name))

            if "event_grid" == endpoint_type:
                add_endpoint_eventgrid(
                    cmd,
                    name=config_data["name"],
                    endpoint_name=endpoint_name,
                    eventgrid_topic_name=endpoint["eventgrid_topic"],
                    eventgrid_resource_group=resource_group,
                    resource_group_name=config_data["resourceGroup"]
                )
            elif "service_bus" == endpoint_type:
                add_endpoint_servicebus(
                    cmd,
                    name=config_data["name"],
                    endpoint_name=endpoint_name,
                    resource_group_name=config_data["resourceGroup"],
                    servicebus_topic_name=endpoint["servicebus_topic"],
                    servicebus_resource_group=resource_group,
                    servicebus_policy=endpoint["servicebus_policy"],
                    servicebus_namespace=endpoint["servicebus_namespace"]
                )
            elif "event_hub" == endpoint_type:
                add_endpoint_eventhub(
                    cmd,
                    name=config_data["name"],
                    endpoint_name=endpoint_name,
                    resource_group_name=config_data["resourceGroup"],
                    eventhub_resource_group=resource_group,
                    eventhub_name=endpoint["eventhub"],
                    eventhub_policy=endpoint["eventhub_policy"],
                    eventhub_namespace=endpoint["eventhub_namespace"]
                )
            else:
                raise CLIError("Invalid enpoint type '{}' in endpoint '{}'".format(endpoint_type, endpoint_name))


def deploy_routes(cmd, config_data):
    six.print_("Deploying routes")
    if "routes" in config_data:
        for route in config_data["routes"]:
            if "@id" not in route or not route["@id"]:
                raise CLIError("One of more routes are missing id property")
            if "endpoint_name" not in route or not route["endpoint_name"]:
                raise CLIError("Route '{}' is missing endpoint_name property")
            if "filter" not in route:
                filter_value = "true"
            else:
                filter_value = route["filter"]

            six.print_("deploying route: '{}'".format(route["@id"]))
            create_route(
                cmd,
                resource_group_name=config_data["resourceGroup"],
                name=config_data["name"],
                route_name=route["@id"],
                endpoint_name=route["endpoint_name"],
                filter=filter_value)


def check_create_path(path):
    path = os.path.join('.', path)

    if not os.path.exists(path):
        six.print_('Creating ' + path)
        os.mkdir(path)

    return path


def get_models_folder_path():
    return check_create_path(MODELS_FOLDER)


def get_configuration_file_path(folder=None, configType=None):
    if not folder:
        folder = '.'

    configFile = CONFIG_FILE
    if configType:
        configFile = configType + "." + configFile
        if not os.path.exists(configFile):
            raise CLIError("Specified config path '{}' not found.".format(configFile))

    return os.path.join(folder, configFile)


def get_configuration_data(directory=None, config=None):
    config_file = get_configuration_file_path(directory)
    json_content = read_JSON_file(config_file)

    if config:
        json_content = apply_additional_config_json(json_content, directory, config)

    json_content["directory"] = directory
    json_content["config"] = config

    return json_content


def apply_additional_config_json(json_content, directory=None, config=None):
    additional_config = get_configuration_file_path(directory, config)
    six.print_("Applying config changes for '{}'".format(config))
    additional_json = read_JSON_file(additional_config)
    json_content = {**json_content, **additional_json}
    if "variables" in json_content and config in json_content["variables"]:
        variables = json_content["variables"][config]
        json_string = json.dumps(json_content, indent=4, sort_keys=True)
        for variable in variables:
            json_string = json_string.replace("{" + variable + "}", variables[variable])
        json_content = json.loads(json_string)

    return json_content


def read_JSON_file(file):
    with open(file, "a+", encoding="utf-8") as f:  # open file for append so we create if not there
        f.seek(0)  # seek to start of file
        data = f.read()
        f.close()  # we are done reading the file will have to re-open w+ later to replace contents

        if data == "":
            data = "{}"

        config = json.loads(data)

        return config


def write_config(config):
    config_file = get_configuration_file_path()
    with open(config_file, "w+", encoding="utf-8") as f:
        json.dump(config, f, indent=4, sort_keys=True)
        f.close()
