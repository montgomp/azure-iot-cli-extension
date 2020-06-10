# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.digitaltwins.dev.constants import TWINS_FILE
from azext_iot.digitaltwins.dev.main import read_JSON_file, write_JSON_file
from knack.util import CLIError
import json
import six


def create(model, twin_id, properties=None, force=False):
    twin_data = read_JSON_file(TWINS_FILE)

    if any(twin_id == item["@id"] for item in twin_data):
        if not force:
            raise CLIError('A twin with @id of "{}" already exists in {}'.format(twin_id, TWINS_FILE))
        twin_data = list(filter(lambda item: (item["@id"] != twin_id), twin_data))

    twin = {
        '@model': model,
        '@id': twin_id
    }
    if properties:
        twin['properties'] = json.loads(properties)
    twin_data.append(twin)
    write_JSON_file(TWINS_FILE, twin_data)


def delete(twin_id):
    twin_data = read_JSON_file(TWINS_FILE)
    twin_data = list(filter(lambda item: (item["@id"] != twin_id), twin_data))

    write_JSON_file(TWINS_FILE, twin_data)


def createRelationship(twin_id, relationship_name, related_id, properties=None):
    six.print_(properties)
    twin_data = read_JSON_file(TWINS_FILE)

    twin = list(filter(lambda item: item["@id"] == twin_id, twin_data))
    if not twin:
        raise CLIError('Unable to find twin with @id = "{}"'.format(twin_id))
    if not list(filter(lambda item: item["@id"] == related_id, twin_data)):
        raise CLIError('Unable to find twin with @id = "{}"'.format(related_id))

    twin = twin[0]

    if "relationships" not in twin:
        twin["relationships"] = {}

    if relationship_name not in twin["relationships"]:
        twin["relationships"][relationship_name] = []

    twin["relationships"][relationship_name] = list(
        filter(
            lambda item: item["@id"] != related_id, twin["relationships"][relationship_name]
        )
    )

    if not properties:
        twin["relationships"][relationship_name].append(
            {
                '@id': related_id
            })
    else:
        twin["relationships"][relationship_name].append(
            {
                '@id': related_id,
                'properties': json.loads(properties)
            })

    write_JSON_file(TWINS_FILE, twin_data)


def deleteRelationship(twin_id, relationship_name, related_id, remove_empty=True):
    twin_data = read_JSON_file(TWINS_FILE)

    twin = list(filter(lambda item: item["@id"] == twin_id, twin_data))
    if not twin or len(twin) < 1:
        six.print_('Unable to find twin with @id = "{}"'.format(twin_id))  # don't raise an error because there is nothing to do
        return

    twin = twin[0]

    if "relationships" not in twin:
        return

    if relationship_name not in twin["relationships"]:
        return

    twin["relationships"][relationship_name] = list(
        filter(
            lambda item: item["@id"] != related_id, twin["relationships"][relationship_name]
        )
    )

    if remove_empty:
        if not twin["relationships"][relationship_name] or twin["relationships"][relationship_name] == []:
            del twin["relationships"][relationship_name]
        if not twin["relationships"] or not twin["relationships"]:
            del twin["relationships"]

    write_JSON_file(TWINS_FILE, twin_data)
