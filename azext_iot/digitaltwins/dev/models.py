# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.digitaltwins.dev.constants import MODELS_EXTENSION, MODELS_CONTEXT
from azext_iot.digitaltwins.dev.main import get_models_folder_path, read_JSON_file, write_JSON_file
from knack.util import CLIError
import os


def create(cmd, model_name, force=False, display_name=None):
    modelPath = get_model_file_path(model_name)
    # does the file alread exist
    if os.path.exists(modelPath):
        if not force:
            raise CLIError('The entered model "{}" already exists. Please use \'--force\' to overwrite.'.format(model_name))

    model_json = {
        '@context': MODELS_CONTEXT,
        '@type': "Interface",
        '@id': "dtmi:example:" + model_name + ";1",
        'displayName': display_name or model_name,
        'contents': []
    }

    write_JSON_file(modelPath, model_json)


def createProperty(cmd, model_name, property_name, schema, display_name=None, writable=False, force=False):
    createContent(
        model_name,
        property_name,
        schema=schema,
        writable=writable,
        force=force,
        content_type="Property",
        display_name=display_name
    )


def createRelationship(cmd, model_name, relationship_name, target="*", display_name=None, force=False):
    createContent(
        model_name,
        relationship_name,
        target=target,
        force=force,
        content_type="Relationship",
        display_name=display_name
    )


def createTelemetry(cmd, model_name, telemetry_name, schema, display_name=None, force=False):
    createContent(
        model_name,
        telemetry_name,
        schema=schema,
        force=force,
        content_type="Telemetry",
        display_name=display_name
    )


def createContent(
    model_name,
    content_name,
    content_type,
    schema=None,
    writable=None,
    target=None,
    force=False,
    display_name=None
):
    modelPath = get_model_file_path(model_name)

    if not os.path.exists(modelPath):
        raise CLIError('The entered model name "{}" does not exist.'.format(modelPath))

    model_json = read_JSON_file(modelPath)
    if "contents" not in model_json:
        model_json["contents"] = []

    if any((content_name == item["name"] and content_type == item["@type"]) for item in model_json["contents"]) and not force:
        raise CLIError('An item named "{}" already exists in "{}"'.format(content_name, modelPath))

    new_content = {
        "@type": content_type,
        "name": content_name
    }

    if schema:
        new_content["schema"] = schema
    if display_name:
        new_content["displayName"] = display_name
    if target:
        new_content["target"] = target
    if writable:
        new_content["writable"] = writable

    # remove existing item matching name and type
    model_json["contents"] = list(
        filter(
            lambda item: (content_name != item["name"] or content_type != item["@type"]), model_json["contents"]
        )
    )
    model_json["contents"].append(new_content)

    write_JSON_file(modelPath, model_json)


def deleteProperty(cmd, model_name, property_name):
    deleteContent(model_name, property_name, content_type="Property")


def deleteRelationship(cmd, model_name, relationship_name):
    deleteContent(model_name, relationship_name, content_type="Relationship")


def deleteTelemetry(cmd, model_name, telemetry_name):
    deleteContent(model_name, telemetry_name, content_type="Telemetry")


def deleteContent(model_name, content_name, content_type):
    modelPath = get_model_file_path(model_name)

    if not os.path.exists(modelPath):
        raise CLIError('The entered model name "{}" does not exist.'.format(modelPath))

    model_json = read_JSON_file(modelPath)
    if "contents" not in model_json:
        model_json["contents"] = []

    model_json["contents"] = list(
        filter(
            lambda item: (content_name != item["name"] or content_type != item["@type"]), model_json["contents"]
        )
    )

    write_JSON_file(modelPath, model_json)


def delete(cmd, model_name):
    os.remove(get_model_file_path(model_name))


def get_model_file_path(name):
    return os.path.join(get_models_folder_path(), name + '.' + MODELS_EXTENSION)
