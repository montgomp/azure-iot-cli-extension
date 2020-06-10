# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
import azext_iot.digitaltwins.dev.models as dt_dev
from knack.util import CLIError


class ModelsTest(unittest.TestCase):
    @mock.patch('os.path.join')
    @mock.patch('azext_iot.digitaltwins.dev.models.get_models_folder_path')
    def test_get_model_file_path(self, mock_folder_path, mock_join):
        mock_folder_path.return_value = "test"
        mock_join.return_value = ""
        dt_dev.get_model_file_path("model_name")

        mock_join.assert_called_with("test", "model_name.json")

    @mock.patch('os.remove')
    @mock.patch('azext_iot.digitaltwins.dev.models.get_models_folder_path')
    def test_delete(self, mock_folder_path, mock_remove):
        mock_folder_path.return_value = "test"
        dt_dev.delete(self, "model_name")
        mock_remove.assert_called_with("test\\model_name.json")

    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.models.get_model_file_path')
    @mock.patch('azext_iot.digitaltwins.dev.models.write_JSON_file')
    def test_create(self, mock_write_json, mock_path, mock_exists):
        mock_path.return_value = "test_path"
        mock_exists.return_value = True
        with self.assertRaises(CLIError):
            dt_dev.create(self, "model_name", force=False)
        dt_dev.create(self, "model_name", force=True)
        mock_write_json.assert_called_with("test_path", {
            '@context': "dtmi:dtdl:context;2",
            '@type': "Interface",
            '@id': "dtmi:example:model_name;1",
            'displayName': "model_name",
            'contents': []
        })

    @mock.patch('azext_iot.digitaltwins.dev.models.createContent')
    def test_createProperty(self, mock_create):
        dt_dev.createProperty(self, "model_name", "name", "schema", "display_name")
        mock_create.assert_called_with(
            'model_name',
            'name',
            schema='schema',
            force=False,
            content_type='Property',
            display_name='display_name',
            writable=False
        )

    @mock.patch('azext_iot.digitaltwins.dev.models.createContent')
    def test_createRelationship(self, mock_create):
        dt_dev.createRelationship(self, "model_name", "name", "*", "display_name")
        mock_create.assert_called_with(
            'model_name',
            'name',
            target='*',
            force=False,
            content_type='Relationship',
            display_name='display_name'
        )

    @mock.patch('azext_iot.digitaltwins.dev.models.createContent')
    def test_createTelemetry(self, mock_create):
        dt_dev.createTelemetry(self, "model_name", "name", "schema", "display_name")
        mock_create.assert_called_with(
            'model_name',
            'name',
            schema='schema',
            force=False,
            content_type='Telemetry',
            display_name='display_name'
        )

    @mock.patch('azext_iot.digitaltwins.dev.models.deleteContent')
    def test_deleteProperty(self, mock_delete):
        dt_dev.deleteProperty(self, "model_name", "name")
        mock_delete.assert_called_with('model_name', 'name', content_type="Property")

    @mock.patch('azext_iot.digitaltwins.dev.models.deleteContent')
    def test_deleteRelationship(self, mock_delete):
        dt_dev.deleteRelationship(self, "model_name", "name")
        mock_delete.assert_called_with('model_name', 'name', content_type="Relationship")

    @mock.patch('azext_iot.digitaltwins.dev.models.deleteContent')
    def test_deleteTelemetry(self, mock_delete):
        dt_dev.deleteTelemetry(self, "model_name", "name")
        mock_delete.assert_called_with('model_name', 'name', content_type="Telemetry")

    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.models.get_model_file_path')
    @mock.patch('azext_iot.digitaltwins.dev.models.read_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.models.write_JSON_file')
    def test_deleteContent(self, mock_write_json, mock_read_file, mock_file_path, mock_exists):
        mock_file_path.return_value = "some_path"
        mock_exists.return_value = False
        with self.assertRaises(CLIError):
            dt_dev.deleteContent("some_model", "name", "content_type")

        mock_exists.return_value = True
        mock_read_file.return_value = {}

        dt_dev.deleteContent("some_model", "name", "content_type")
        mock_write_json.assert_called_with("some_path", {"contents": []})

        mock_read_file.return_value = {"contents": [
            {"name": "remainingValue"},
            {"name": "removedValue", "@type": "content_type"}
        ]}
        dt_dev.deleteContent("some_model", "removedValue", "content_type")
        mock_write_json.assert_called_with("some_path", {"contents": [
            {"name": "remainingValue"}
        ]})

    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.models.get_model_file_path')
    @mock.patch('azext_iot.digitaltwins.dev.models.read_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.models.write_JSON_file')
    def test_createContent(self, mock_write_json, mock_read_file, mock_file_path, mock_exists):
        mock_file_path.return_value = "some_path"
        mock_exists.return_value = False
        with self.assertRaises(CLIError):
            dt_dev.createContent("some_model", "name", "content_type")

        mock_exists.return_value = True
        mock_read_file.return_value = {}

        dt_dev.createContent("some_model", "addedValue", "content_type")
        mock_write_json.assert_called_with("some_path", {"contents": [
            {"name": "addedValue", "@type": "content_type"}
        ]})

        mock_read_file.return_value = {"contents": [
            {"name": "existingValue"}
        ]}
        dt_dev.createContent("some_model", "addedValue", "content_type")
        mock_write_json.assert_called_with("some_path", {"contents": [
            {"name": "existingValue"},
            {"name": "addedValue", "@type": "content_type"}
        ]})


if __name__ == '__main__':
    unittest.main()
