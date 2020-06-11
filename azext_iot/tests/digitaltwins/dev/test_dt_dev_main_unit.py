# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
import azext_iot.digitaltwins.dev.main as dt_dev
from knack.util import CLIError


class MainTest(unittest.TestCase):
    @mock.patch('azext_iot.digitaltwins.dev.main.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.zip_distribution')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_twins')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_models')
    @mock.patch('os.path.join')
    @mock.patch('os.list')
    @mock.patch('azext_iot.digitaltwins.dev.main.check_create_path')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.remove')
    @mock.patch('os.path.exists')
    def test_build_workspace(self,
                             mock_exists,
                             mock_remove,
                             mock_rmtree,
                             mock_create_path,
                             mock_os_list,
                             mock_path_join,
                             mock_build_models,
                             mock_build_twins,
                             mock_zip,
                             mock_read_config,
                             mock_json_writer):
        mock_read_config.return_value = {}
        mock_exists.return_value = True
        mock_path_join.return_value = "dist_models"
        mock_build_models.return_value = "test models"
        dt_dev.build_workspace(self)
        mock_remove.assert_called_with("dist.zip")
        mock_rmtree.assert_called_with("dist", ignore_errors=True)
        mock_create_path.assert_has_calls([
            mock.call("dist"),
            mock.call("Models"),
            mock.call("dist_models")
        ])
        mock_build_models.assert_called()
        mock_build_twins.assert_called_with("test models")
        mock_zip.assert_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.zip_distribution')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_twins')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_models')
    @mock.patch('os.path.join')
    @mock.patch('os.list')
    @mock.patch('azext_iot.digitaltwins.dev.main.check_create_path')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.remove')
    @mock.patch('os.path.exists')
    def test_build_workspace_without_zip(self,
                             mock_exists,
                             mock_remove,
                             mock_rmtree,
                             mock_create_path,
                             mock_os_list,
                             mock_path_join,
                             mock_build_models,
                             mock_build_twins,
                             mock_zip,
                             mock_read_config,
                             mock_json_writer):
        mock_read_config.return_value = {"noZip": True}
        mock_exists.return_value = True
        mock_path_join.return_value = "dist_models"
        mock_build_models.return_value = "test models"
        dt_dev.build_workspace(self)
        mock_remove.assert_called_with("dist.zip")
        mock_rmtree.assert_called_with("dist", ignore_errors=True)
        mock_create_path.assert_has_calls([
            mock.call("dist"),
            mock.call("Models"),
            mock.call("dist_models")
        ])
        mock_build_models.assert_called()
        mock_build_twins.assert_called_with("test models")
        mock_zip.assert_not_called()

    @mock.patch('six.print_')
    @mock.patch('azext_iot.digitaltwins.dev.main.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.extend_needed_models')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    @mock.patch('os.path.join')
    @mock.patch('os.mkdir')
    @mock.patch('os.walk')
    def test_build_models(self,
                          mock_walk,
                          mock_mkdir,
                          mock_path_join,
                          mock_read_json,
                          mock_extend_models,
                          mock_write_json,
                          mock_print):
        mock_path_join.return_value = "creating"
        mock_walk.return_value = [
            ("Models", ("Sensors", "Switches"), ("Room.json", "NotAModel.txt")),
            ("Models\\Sensors", (), ("motionsensor.json",))
        ]
        mock_read_json.return_value = {"property": "invalid dtdl"}
        with self.assertRaises(CLIError):
            dt_dev.build_models()

        mock_read_json.return_value = {"@id": "model1"}
        with self.assertRaises(CLIError):  # missing contents
            dt_dev.build_models()
        with self.assertRaises(CLIError):  # contents without a @type
            mock_read_json.return_value = {"@id": "model1", "extends": "base_model", "contents": [{"invalid": "missing @type"}]}
            dt_dev.build_models()

        with self.assertRaises(CLIError):
            mock_read_json.return_value = {"@id": "model1", "extends": "base_model", "contents": []}
            mock_extend_models.reset_mock()
            mock_extend_models.return_value = {"some_model": ["room"]}
            mock_mkdir.reset_mock()
            dt_dev.build_models()
        mock_extend_models.assert_has_calls([
            mock.call({}, 'base_model', 'model1', 'Room.json'),
            mock.call({'some_model': ['room']}, 'base_model', 'model1', 'motionsensor.json')
        ])

        mock_extend_models.reset_mock()
        mock_extend_models.return_value = {}
        mock_mkdir.reset_mock()
        mock_write_json.reset_mock()
        mock_read_json.return_value = {
            "@id": "model1",
            "extends": "base_model",
            "contents": [
                {"@type": "Relationship"}
            ]
        }
        with self.assertRaises(CLIError):  # missing target in relationship
            dt_dev.build_models()

        mock_extend_models.reset_mock()
        mock_extend_models.return_value = {}
        mock_mkdir.reset_mock()
        mock_write_json.reset_mock()
        mock_read_json.return_value = {
            "@id": "model1",
            "extends": "base_model",
            "contents": [
                {"@type": "Relationship", "target": "*"},
                {"@type": "Component"}
            ]
        }

        with self.assertRaises(CLIError):  # missing schema on component
            dt_dev.build_models()

        mock_extend_models.reset_mock()
        mock_extend_models.return_value = {}
        mock_mkdir.reset_mock()
        mock_write_json.reset_mock()
        mock_read_json.return_value = {
            "@id": "model1",
            "extends": "base_model",
            "contents": [
                {"@type": "Relationship", "target": "*"},
                {"@type": "Component", "schema": "boolean"}
            ]
        }

        dt_dev.build_models()
        mock_mkdir.assert_has_calls([
            mock.call("creating"),
            mock.call("creating")
        ])

        mock_write_json.assert_has_calls([
            mock.call("creating", {
                '@id': 'model1', 'extends': 'base_model', 'contents': [
                    {"@type": "Relationship", "target": "*"},
                    {"@type": "Component", "schema": "boolean"}
                ]
            }),
            mock.call("creating", {
                '@id': 'model1', 'extends': 'base_model', 'contents': [
                    {"@type": "Relationship", "target": "*"},
                    {"@type": "Component", "schema": "boolean"}
                ]
            })
        ])

    @mock.patch('os.path.exists')
    @mock.patch('os.path.join')
    @mock.patch('azext_iot.digitaltwins.dev.main.write_JSON_file')
    def test_build_config_file(self, mock_write_file, mock_path, mock_exists):
        mock_path.return_value = "mock_file_path"
        mock_exists.return_value = True
        with self.assertRaises(CLIError):
            dt_dev.build_config_file("test_config", "test_group", "test_location", False)
        dt_dev.build_config_file("test_config", "test_group", "test_location", True)
        mock_write_file.assert_called_with("mock_file_path", {
            'name': 'test_config',
            'resourceGroup': 'test_group',
            'location': 'test_location'
        })

    @mock.patch('six.print_')
    def test_extend_needed_models(self, mock_six):
        extended = dt_dev.extend_needed_models("untouched", "*", None, None)
        self.assertEqual(extended, "untouched")
        extended = dt_dev.extend_needed_models({'neededModel': ['oldModel.json']}, "neededModel", "newModel:1", "newModel.json")
        mock_six.assert_called_with("newModel:1 requires model neededModel")
        self.assertEqual(extended, {'neededModel': ['oldModel.json', 'newModel.json']})

    @mock.patch('azext_iot.digitaltwins.dev.main.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    def test_build_twins(self, mock_json, mock_write_json):
        mock_json.return_value = [{
            "incomplete": True
        }]
        with self.assertRaises(CLIError):
            dt_dev.build_twins(None)
        mock_json.return_value = [{
            "@id": "duplicated"
        }, {
            "@id": "duplicated"
        }]
        with self.assertRaises(CLIError):
            dt_dev.build_twins(None)
        mock_json.return_value = [{
            "@id": "unknownModel",
            "@model": "unknown:1"
        }]
        with self.assertRaises(CLIError):
            dt_dev.build_twins(None)

        json_content = [{
            "@id": "knownTwin1",
            "@model": "known:1"
        }, {
            "@id": "knownTwin2",
            "@model": "known:1"
        }]
        mock_json.return_value = json_content
        dt_dev.build_twins(["known:1"])
        mock_write_json.assert_called_with('dist\\twins.json', json_content)

    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_routes')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_endpoints')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_twins')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_models')
    @mock.patch('azext_iot.digitaltwins.dev.main.check_create_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.get_configuration_data')
    @mock.patch('azext_iot.digitaltwins.dev.main.extract_distribution')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_workspace')
    def test_deploy_workspace(self,
                              mock_build,
                              mock_exists,
                              mock_rmtree,
                              mock_extract,
                              mock_config,
                              mock_create_instance,
                              mock_deploy_models,
                              mock_deploy_twins,
                              mock_deploy_endpoints,
                              mock_deploy_routes):
        mock_exists.return_value = True
        mock_config.return_value = {}
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self)
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test")
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test location", resource_group_name="test resource group")
        mock_config.return_value = {
            "location": "test location",
            "resourceGroup": "test resource group",
            "name": "test name"
        }

        dt_dev.deploy_workspace(self)
        mock_build.assert_not_called()
        mock_rmtree.assert_called()
        mock_extract.assert_called()
        mock_config.assert_called()
        mock_create_instance.assert_called()
        mock_deploy_models.assert_called()
        mock_deploy_twins.assert_called()
        mock_deploy_endpoints.assert_called()
        mock_deploy_routes.assert_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_routes')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_endpoints')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_twins')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_models')
    @mock.patch('azext_iot.digitaltwins.dev.main.check_create_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.get_configuration_data')
    @mock.patch('azext_iot.digitaltwins.dev.main.extract_distribution')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_workspace')
    def test_deploy_workspace_builds_project(
        self,
        mock_build,
        mock_exists,
        mock_rmtree,
        mock_extract,
        mock_config,
        mock_create_instance,
        mock_deploy_models,
        mock_deploy_twins,
        mock_deploy_endpoints,
        mock_deploy_routes
    ):
        mock_exists.return_value = False
        mock_config.return_value = {}
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self)
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test")
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test location", resource_group_name="test resource group")
        mock_config.return_value = {
            "location": "test location",
            "resourceGroup": "test resource group",
            "name": "test name"
        }

        dt_dev.deploy_workspace(self)
        mock_build.assert_called()
        mock_rmtree.assert_not_called()
        mock_extract.assert_not_called()
        mock_config.assert_called()
        mock_create_instance.assert_called()
        mock_deploy_models.assert_called()
        mock_deploy_twins.assert_called()
        mock_deploy_endpoints.assert_called()
        mock_deploy_routes.assert_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_routes')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_endpoints')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_twins')
    @mock.patch('azext_iot.digitaltwins.dev.main.deploy_models')
    @mock.patch('azext_iot.digitaltwins.dev.main.check_create_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.get_configuration_data')
    @mock.patch('azext_iot.digitaltwins.dev.main.extract_distribution')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.main.build_workspace')
    def test_deploy_workspace_always_rebuilds(self,
                              mock_build,
                              mock_exists,
                              mock_rmtree,
                              mock_extract,
                              mock_config,
                              mock_create_instance,
                              mock_deploy_models,
                              mock_deploy_twins,
                              mock_deploy_endpoints,
                              mock_deploy_routes):
        mock_exists.return_value = True
        mock_config.return_value = {"rebuild": "always"}
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self)
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test")
        with self.assertRaises(CLIError):
            dt_dev.deploy_workspace(self, location="test location", resource_group_name="test resource group")
        mock_config.return_value = {
            "location": "test location",
            "resourceGroup": "test resource group",
            "name": "test name"
        }

        dt_dev.deploy_workspace(self)
        mock_build.assert_called()
        mock_rmtree.assert_called()
        mock_extract.assert_called()
        mock_config.assert_called()
        mock_create_instance.assert_called()
        mock_deploy_models.assert_called()
        mock_deploy_twins.assert_called()
        mock_deploy_endpoints.assert_called()
        mock_deploy_routes.assert_called()

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    def test_get_models_folder_path(self, mock_exists, mock_mkdir):
        mock_exists.return_value = True
        model_path = dt_dev.get_models_folder_path()
        self.assertEqual(model_path, '.\\Models')
        mock_mkdir.assert_not_called()

        mock_exists.return_value = False
        model_path = dt_dev.get_models_folder_path()
        self.assertEqual(model_path, '.\\Models')
        mock_mkdir.assert_called()

    @mock.patch('os.path.exists')
    @mock.patch('builtins.open', create=True)
    def test_get_configuration_file_path(self, mock_open, mock_exists):
        mock_exists.return_value = True
        config_path = dt_dev.get_configuration_file_path()
        self.assertEqual(config_path, ".\\config.json")

        config_path = dt_dev.get_configuration_file_path(configType="dev")
        self.assertEqual(config_path, ".\\dev.config.json")

        config_path = dt_dev.get_configuration_file_path("dist", "dev")
        self.assertEqual(config_path, "dist\\dev.config.json")

        with self.assertRaises(CLIError):
            mock_exists.return_value = False
            dt_dev.get_configuration_file_path("something_that_doesnt_exists", "something_that_doesnt_exist")

    @mock.patch('azext_iot.digitaltwins.dev.main.apply_additional_config_json')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    def test_get_configuration_data(self, mock_read_json, mock_additional_json):
        mock_read_json.return_value = {}
        mock_additional_json.return_value = {}
        json_content = dt_dev.get_configuration_data(directory="dist", config="test")

        self.assertEqual(json_content["directory"], "dist")
        self.assertEqual(json_content["config"], "test")

    @mock.patch('os.path.exists')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    def test_apply_additional_config_json(self, mock_read_json, mock_exists):
        mock_read_json.return_value = {
            'location': "{some_variable}",
            'resourceGroup': 'overridden',
            'variables': {
                'test': {
                    'some_variable': 'overridden_variable'
                }
            }
        }
        base_json = {
            'location': '{some_variable}',
            'persisted': 'base',
            'resourceGroup': 'base',
            'variables': {
                'test': {
                    'some_variable': 'base_variable'
                }
            }
        }

        mock_exists.return_value = True
        json_content = dt_dev.apply_additional_config_json(base_json, config='test')
        self.assertEqual(json_content["resourceGroup"], 'overridden')
        self.assertEqual(json_content['persisted'], 'base')
        self.assertEqual(json_content['variables']['test']['some_variable'], 'overridden_variable')
        self.assertEqual(json_content['location'], 'overridden_variable')

        json_content = dt_dev.apply_additional_config_json(base_json, config='test2')
        self.assertEqual(json_content['location'], '{some_variable}')

    @mock.patch('os.path.join')
    @mock.patch('os.path.exists')
    @mock.patch('six.print_')
    @mock.patch('os.mkdir')
    def test_check_create_path(self, mock_mkdir, mock_print, mock_exists, mock_join):
        mock_join.return_value = "./path"
        mock_exists.return_value = True
        response = dt_dev.check_create_path("path")
        mock_mkdir.assert_not_called()
        self.assertEqual(response, "./path")

        mock_exists.return_value = False
        dt_dev.check_create_path("path")
        mock_print.assert_called_with("Creating ./path")
        mock_mkdir.assert_called_with("./path")

    @mock.patch('azext_iot.digitaltwins.dev.main.add_models')
    @mock.patch('os.path.join')
    @mock.patch('six.print_')
    def test_deploy_models(self, mock_print, mock_join, mock_add_models):
        mock_join.return_value = "./Models"
        mock_config = {
            'name': 'mock_name',
            'resourceGroup': 'mock_resource_group',
            'directory': './mock'
        }
        dt_dev.deploy_models(self, mock_config)
        mock_add_models.assert_called_with(
            self,
            "mock_name",
            resource_group_name="mock_resource_group",
            from_directory="./Models"
        )

    @mock.patch('azext_iot.digitaltwins.dev.main.create_relationship')
    @mock.patch('azext_iot.digitaltwins.dev.main.create_twin')
    @mock.patch('os.path.join')
    @mock.patch('azext_iot.digitaltwins.dev.main.read_JSON_file')
    def test_deploy_twins(self, mock_json, mock_join, mock_create_twin, mock_create_relationship):
        mock_join.return_value = "./twin.json"
        mock_config = {
            'directory': 'mock_directory',
            'name': 'mock_name',
            'resourceGroup': 'mock_resource_group'

        }
        mock_json.return_value = [{
            '@id': 'mock_twin',
            '@model': 'mock:model;1',
            'properties': {'property1': 'value1'},
            'relationships':
            {
                'relationship1': [
                    {
                        '@id': 'mock_twin2',
                        'properties': {
                            "relationship_property": "related_value"
                        }
                    }
                ]
            }
        }]

        dt_dev.deploy_twins(self, mock_config)
        mock_create_twin.assert_called_with(
            self,
            name="mock_name",
            resource_group_name="mock_resource_group",
            twin_id="mock_twin",
            model_id="mock:model;1",
            properties={"property1": "value1"}
        )
        mock_create_relationship.assert_called_with(
            self,
            name="mock_name",
            resource_group_name="mock_resource_group",
            source_twin_id="mock_twin",
            target_twin_id="mock_twin2",
            relationship_id="mock_twin_relationship1_mock_twin2",
            relationship="relationship1",
            properties={"relationship_property": "related_value"}
        )

    @mock.patch('azext_iot.digitaltwins.dev.main.delete_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.show_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.create_instance')
    def test_create_instance_exists_safe(self, mock_create, mock_show, mock_delete):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group'
        }
        mock_show.return_value = {
            "id": "mock/resource/id/for/mock/twin",
            "hostname": "mock_host.api.wus2.digitaltwins.azure.net",
            "location": "westus2",
            "name": "mock_instance",
            "provisioningState": "Succeeded",
            "resourceGroup": "mock_resource_group",
            "type": "Microsoft.DigitalTwins/digitalTwinsInstances"
        }

        with self.assertRaises(CLIError):
            dt_dev.check_create_instance(self, mock_config)
            mock_create.assert_not_called()
            mock_delete.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.delete_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.show_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.create_instance')
    def test_create_instance_exists_append(self, mock_create, mock_show, mock_delete):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            'deployment_strategy': "Append"
        }
        mock_show.return_value = {
            "id": "mock/resource/id/for/mock/twin",
            "hostname": "mock_host.api.wus2.digitaltwins.azure.net",
            "location": "westus2",
            "name": "mock_instance",
            "provisioningState": "Succeeded",
            "resourceGroup": "mock_resource_group",
            "type": "Microsoft.DigitalTwins/digitalTwinsInstances"
        }

        dt_dev.check_create_instance(self, mock_config)
        mock_create.assert_not_called()
        mock_delete.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.delete_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.show_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.create_instance')
    def test_create_instance_exists_overwrite(self, mock_create, mock_show, mock_delete):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            'deployment_strategy': 'Overwrite',
            'location': 'westus2'
        }
        mock_show.return_value = {
            "id": "mock/resource/id/for/mock/twin",
            "hostname": "mock_host.api.wus2.digitaltwins.azure.net",
            "location": "westus2",
            "name": "mock_instance",
            "provisioningState": "Succeeded",
            "resourceGroup": "mock_resource_group",
            "type": "Microsoft.DigitalTwins/digitalTwinsInstances"
        }

        dt_dev.check_create_instance(self, mock_config)
        mock_delete.assert_called_with(
            self,
            name="mock_instance",
            resource_group_name="mock_resource_group"
        )
        mock_create.assert_called_with(
            self,
            name="mock_instance",
            resource_group_name="mock_resource_group",
            location="westus2"
        )

    @mock.patch('azext_iot.digitaltwins.dev.main.delete_instance')
    @mock.patch('azext_iot.digitaltwins.dev.main.show_instance', side_effect=CLIError("Not found"))
    @mock.patch('azext_iot.digitaltwins.dev.main.create_instance')
    def test_create_instance_not_exists(self, mock_create, mock_show, mock_delete):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            'location': 'westus2'
        }
        dt_dev.check_create_instance(self, mock_config)
        mock_create.assert_called_with(
            self,
            name="mock_instance",
            resource_group_name="mock_resource_group",
            location="westus2"
        )
        mock_delete.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.main.create_route')
    def test_deploy_routes(self, mock_create_route):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "@id": "mock_route",
                    "endpoint_name": "endpoint_name",
                    "filter": "type='Sometype'"
                }
            ]
        }
        dt_dev.deploy_routes(self, mock_config)
        mock_create_route.assert_called_with(
            self,
            resource_group_name="mock_resource_group",
            name="mock_instance",
            route_name="mock_route",
            endpoint_name="endpoint_name",
            filter="type='Sometype'"
        )

        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "@id": "mock_route",
                    "endpoint_name": "endpoint_name"
                }
            ]
        }
        dt_dev.deploy_routes(self, mock_config)
        mock_create_route.assert_called_with(
            self,
            resource_group_name="mock_resource_group",
            name="mock_instance",
            route_name="mock_route",
            endpoint_name="endpoint_name",
            filter="true"
        )

    @mock.patch('azext_iot.digitaltwins.dev.main.create_route')
    def test_deploy_with_no_routes(self, mock_create_route):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": []
        }
        dt_dev.deploy_routes(self, mock_config)
        mock_create_route.assert_not_called()

        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group'
        }
        dt_dev.deploy_routes(self, mock_config)
        mock_create_route.assert_not_called()

    def test_deploy_routes_fails_missing_id(self,):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "filter": "true",
                    "endpoint_name": "endpoint_name"
                }
            ]
        }
        with self.assertRaises(CLIError):
            dt_dev.deploy_routes(self, mock_config)

        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "@id": None,
                    "filter": "true",
                    "endpoint_name": "endpoint_name"
                }
            ]
        }
        with self.assertRaises(CLIError):
            dt_dev.deploy_routes(self, mock_config)

    def test_deploy_routes_fails_missing_endpoint_name(self):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "@id": "route",
                    "filter": "true"
                }
            ]
        }
        with self.assertRaises(CLIError):
            dt_dev.deploy_routes(self, mock_config)

        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "routes": [
                {
                    "@id": "route",
                    "filter": "true",
                    "endpoint_name": None
                }
            ]
        }
        with self.assertRaises(CLIError):
            dt_dev.deploy_routes(self, mock_config)

    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_eventgrid')
    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_servicebus')
    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_eventhub')
    def test_deploy_multiple_endpoint_types(self, mock_create_eventhub, mock_create_servicebus, mock_create_eventgrid):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
            "endpoints": [
                {
                    "@id": "eg_endpoint",
                    "@type": "event_grid",
                    "resource_group": None,
                    "eventgrid_topic": "topic"
                },
                {
                    "@id": "sb_endpoint",
                    "@type": "service_bus",
                    "servicebus_namespace": "sb_namespace",
                    "servicebus_policy": "sb_policy",
                    "resource_group": "sb_resourcegroup",
                    "servicebus_topic": "sb_topic"
                },
                {
                    "@id": "eh_endpoint",
                    "@type": "event_hub",
                    "eventhub": "eh_name",
                    "eventhub_namespace": "eh_namespace",
                    "eventhub_policy": "eh_policy",
                    "resource_group": "eh_resourcegroup"
                }
            ]
        }
        dt_dev.deploy_endpoints(self, mock_config)

        mock_create_eventgrid.assert_called_with(
            self,
            name="mock_instance",
            endpoint_name="eg_endpoint",
            eventgrid_topic_name="topic",
            eventgrid_resource_group="mock_resource_group",
            resource_group_name="mock_resource_group"
        )
        mock_create_eventhub.assert_called_with(
            self,
            name="mock_instance",
            endpoint_name="eh_endpoint",
            resource_group_name="mock_resource_group",
            eventhub_resource_group="eh_resourcegroup",
            eventhub_name="eh_name",
            eventhub_policy="eh_policy",
            eventhub_namespace="eh_namespace"

        )
        mock_create_servicebus.assert_called_with(
            self,
            name="mock_instance",
            endpoint_name="sb_endpoint",
            resource_group_name="mock_resource_group",
            servicebus_topic_name="sb_topic",
            servicebus_resource_group="sb_resourcegroup",
            servicebus_policy="sb_policy",
            servicebus_namespace="sb_namespace"
        )

    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_eventgrid')
    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_servicebus')
    @mock.patch('azext_iot.digitaltwins.dev.main.add_endpoint_eventhub')
    def test_deploy_with_no_endpoint(self, mock_create_eventhub, mock_create_servicebus, mock_create_eventgrid):
        mock_config = {
            'name': 'mock_instance',
            'resourceGroup': 'mock_resource_group',
        }
        dt_dev.deploy_endpoints(self, mock_config)

        mock_create_eventgrid.assert_not_called()
        mock_create_eventhub.assert_not_called()
        mock_create_servicebus.assert_not_called()

    def test_deploy_endpoints_fails_missing_id(self):
        with self.assertRaises(CLIError):
            mock_config = {
                'resourceGroup': 'mock_resource_group',
                'endpoints': [{
                    '@type': 'service_bus'
                }]
            }
            dt_dev.deploy_endpoints(self, mock_config)

    def test_deploy_endpoints_fails_missing_type(self):
        with self.assertRaises(CLIError):
            mock_config = {
                'resourceGroup': 'mock_resource_group',
                'endpoints': [{
                    '@id': 'mock_endpoint'
                }]
            }
            dt_dev.deploy_endpoints(self, mock_config)

    def test_deploy_endpoints_fails_invalid_type(self):
        with self.assertRaises(CLIError):
            mock_config = {
                'resourceGroup': 'mock_resource_group',
                'endpoints': [{
                    '@id': 'mock_endpoint',
                    '@type': 'something invalid'
                }]
            }
            dt_dev.deploy_endpoints(self, mock_config)

# add_endpoint_eventgrid, add_endpoint_eventhub, add_endpoint_servicebus


if __name__ == '__main__':
    unittest.main()
