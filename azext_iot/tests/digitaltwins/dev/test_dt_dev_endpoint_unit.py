# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
import azext_iot.digitaltwins.dev.endpoints as dt_dev
from knack.util import CLIError


class EndpointsClass(unittest.TestCase):

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_delete(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint",
                    "@type": "event_grid",
                    "resource_group": None,
                    "eventgrid_topic": "topic"
                }
            ]
        }

        dt_dev.delete_endpoint("endpoint")
        mock_writer.assert_called_with(
            "config.json",
            {
                "endpoints": []
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventgrid(self, mock_reader, mock_writer):
        mock_reader.return_value = {}

        dt_dev.create_eventgrid("endpoint", "topic")
        mock_writer.assert_called_with(
            "config.json",
            {
                "endpoints": [
                    {
                        "@id": "endpoint",
                        "@type": "event_grid",
                        "resource_group": None,
                        "eventgrid_topic": "topic"
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventgrid_fails_existing(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        with self.assertRaises(CLIError):
            dt_dev.create_eventgrid("endpoint", "topic")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventgrid_with_force(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        dt_dev.create_eventgrid(
            "endpoint",
            "topic",
            force=True
        )
        mock_writer.assert_called_with(
            "config.json",
            {
                "endpoints": [
                    {
                        "@id": "endpoint",
                        "@type": "event_grid",
                        "resource_group": None,
                        "eventgrid_topic": "topic"
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventhub(self, mock_reader, mock_writer):
        mock_reader.return_value = {}

        dt_dev.create_eventhub("endpoint", "namespace", "eventhub", "policy")
        mock_writer.assert_called_with(
            "config.json",
            {
                'endpoints': [
                    {
                        '@id': 'endpoint',
                        'resource_group': None,
                        'eventhub_namespace': 'namespace',
                        'eventhub': 'eventhub',
                        'eventhub_policy': 'policy',
                        '@type': 'event_hub'
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventhub_fails_existing(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        with self.assertRaises(CLIError):
            dt_dev.create_eventhub("endpoint", "namespace", "eventhub", "policy")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_eventhub_with_force(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        dt_dev.create_eventhub("endpoint", "namespace", "eventhub", "policy", eventhub_resource_group="group", force=True)
        mock_writer.assert_called_with(
            "config.json",
            {
                'endpoints': [
                    {
                        '@id': 'endpoint',
                        'resource_group': 'group',
                        'eventhub_namespace': 'namespace',
                        'eventhub': 'eventhub',
                        'eventhub_policy': 'policy',
                        '@type': 'event_hub'
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_servicebus(self, mock_reader, mock_writer):
        mock_reader.return_value = {}

        dt_dev.create_servicebus("endpoint", "namespace", "topic", "policy")
        mock_writer.assert_called_with(
            "config.json",
            {
                'endpoints': [
                    {
                        '@id': 'endpoint',
                        'resource_group': None,
                        'servicebus_namespace': 'namespace',
                        'servicebus_topic': 'topic',
                        'servicebus_policy': 'policy',
                        '@type': 'service_bus'
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_servicebus_fails_existing(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        with self.assertRaises(CLIError):
            dt_dev.create_servicebus("endpoint", "namespace", "topic", "policy", "group")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.endpoints.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.endpoints.read_JSON_file')
    def test_create_servicebus_with_force(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "endpoints": [
                {
                    "@id": "endpoint"
                }
            ]
        }

        dt_dev.create_servicebus(
            "endpoint",
            "namespace",
            "topic",
            "policy",
            "group",
            force=True
        )
        mock_writer.assert_called_with(
            "config.json",
            {
                'endpoints': [
                    {
                        '@id': 'endpoint',
                        'resource_group': 'group',
                        'servicebus_namespace': 'namespace',
                        'servicebus_topic': 'topic',
                        'servicebus_policy': 'policy',
                        '@type': 'service_bus'
                    }
                ]
            }
        )
# end of class


if __name__ == '__main__':
    unittest.main()
