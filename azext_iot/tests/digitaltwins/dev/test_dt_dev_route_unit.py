# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
import azext_iot.digitaltwins.dev.routes as dt_dev
from knack.util import CLIError


class RoutesClass(unittest.TestCase):
    @mock.patch('azext_iot.digitaltwins.dev.routes.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.routes.read_JSON_file')
    def test_create_route(self, mock_reader, mock_writer):
        mock_reader.return_value = {}

        dt_dev.create_route("route", "endpoint")

        mock_writer.assert_called_with(
            "config.json",
            {
                "routes": [
                    {
                        "endpoint_name": "endpoint",
                        "filter": "true",
                        "@id": "route"
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.routes.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.routes.read_JSON_file')
    def test_create_route_fails_existing(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "routes": [
                {
                    "endpoint_name": "endpoint",
                    "filter": "true",
                    "@id": "route"
                }
            ]
        }

        with self.assertRaises(CLIError):
            dt_dev.create_route("route", "endpoint")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.routes.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.routes.read_JSON_file')
    def test_create_route_with_filter(self, mock_reader, mock_writer):
        mock_reader.return_value = {}

        dt_dev.create_route("route", "endpoint", route_filter="type='SomeValue'")

        mock_writer.assert_called_with(
            "config.json",
            {
                "routes": [
                    {
                        "endpoint_name": "endpoint",
                        "filter": "type='SomeValue'",
                        "@id": "route"
                    }
                ]
            }
        )

    @mock.patch('azext_iot.digitaltwins.dev.routes.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.routes.read_JSON_file')
    def test_create_route_with_force(self, mock_reader, mock_writer):
        mock_reader.return_value = {
            "routes": [
                {
                    "endpoint_name": "existing endpoint",
                    "filter": "existing filter",
                    "@id": "route"
                }
            ]
        }

        dt_dev.create_route("route", "endpoint", force=True)

        mock_writer.assert_called_with(
            "config.json",
            {
                "routes": [
                    {
                        "endpoint_name": "endpoint",
                        "filter": "true",
                        "@id": "route"
                    }
                ]
            }
        )


if __name__ == '__main__':
    unittest.main()
