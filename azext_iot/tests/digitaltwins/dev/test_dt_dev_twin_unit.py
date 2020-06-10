# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
import azext_iot.digitaltwins.dev.twins as dt_dev
from knack.util import CLIError
from json import dumps


class TwinsClass(unittest.TestCase):
    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_fails_when_existing(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}]
        with self.assertRaises(CLIError):
            dt_dev.create("model_name", "model1")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_with_force(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}]
        dt_dev.create("model_name", "model1", force=True)
        mock_writer.assert_called_with("twins.json", [{'@model': 'model_name', '@id': 'model1'}])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_empty_collection(self, mock_reader, mock_writer):
        mock_reader.return_value = []
        dt_dev.create("model_name", "model1", "{\"property1\": \"value\"}")
        mock_writer.assert_called_with(
            "twins.json",
            [{'@model': 'model_name', '@id': 'model1', "properties": {"property1": "value"}}]
        )

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_adds_to_collection(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}]
        dt_dev.create("model_name", "model2")
        mock_writer.assert_called_with(
            "twins.json",
            [
                {
                    '@model': 'model_name',
                    '@id': 'model1'
                },
                {
                    '@model': 'model_name',
                    '@id': 'model2'
                }
            ]
        )

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_with_properties(self, mock_reader, mock_writer):
        mock_reader.return_value = []
        dt_dev.create("model_name", "model1", properties=dumps({"property1": "value1"}))
        mock_writer.assert_called_with(
            "twins.json",
            [
                {
                    '@model': 'model_name',
                    '@id': 'model1',
                    "properties": {"property1": "value1"}}
            ]
        )

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}]

        dt_dev.delete("model1")
        mock_writer.assert_called_with("twins.json", [])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_empty_collection(self, mock_reader, mock_writer):
        mock_reader.return_value = []
        dt_dev.delete("model_name")
        mock_writer.assert_called_with("twins.json", [])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_twin_not_in_collection(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}]

        dt_dev.delete("model2")
        mock_writer.assert_called_with("twins.json", [{'@model': 'model_name', '@id': 'model1'}])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_without_damaging_other_items(self, mock_reader, mock_writer):
        mock_reader.return_value = [{'@model': 'model_name', '@id': 'model1'}, {'@model': 'model_name', '@id': 'model2'}]

        dt_dev.delete("model2")
        mock_writer.assert_called_with("twins.json", [{'@model': 'model_name', '@id': 'model1'}])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_missing_origin(self, mock_reader, mock_writer):
        # model1 and model2 defined without relationships
        mock_reader.return_value = []
        with self.assertRaises(CLIError):
            # origin of relationship is missing
            dt_dev.createRelationship("model_missing", "has", "model2")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_missing_target(self, mock_reader, mock_writer):
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1'},
        ]
        with self.assertRaises(CLIError):
            # target of relationship is missing
            dt_dev.createRelationship("model1", "has", "model_missing")
            mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_without_existing_relationships(self, mock_reader, mock_writer):
        # model1 and model2 defined without relationships
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1'},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        # model1 and model2 defined without relationships
        dt_dev.createRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_with_existing_other_relationship(self, mock_reader, mock_writer):
        # model1 with other relationship to model2
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships' : {'with_other': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.createRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {
                '@model': 'model_name',
                '@id': 'model1',
                'relationships': {
                    'with_other': [{"@id": "model2"}], 'has': [{"@id": "model2"}]
                }
            },
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_with_existing_relationship_to_other_twin(self, mock_reader, mock_writer):
        # relationship model1 has othermodel exists
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.createRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {
                '@model': 'model_name',
                '@id': 'model1',
                'relationships': {
                    'has': [{"@id": "other_model"}, {"@id": "model2"}]
                }
            },
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_with_properties(self, mock_reader, mock_writer):
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.createRelationship("model1", "has", "model2", dumps({"property1": True}))
        mock_writer.assert_called_with("twins.json", [
            {
                '@model': 'model_name',
                '@id': 'model1',
                'relationships': {
                    'has': [
                        {"@id": "other_model"},
                        {
                            "@id": "model2",
                            "properties": {
                                "property1": True
                            }
                        }
                    ]
                }
            },
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_create_relationship_that_already_exists(self, mock_reader, mock_writer):
        # relationship model1 has model2 already exists
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.createRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_missing_origin(self, mock_reader, mock_writer):
        # model1 and model2 defined without relationships
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1'},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        # origin of relationship is missing
        dt_dev.deleteRelationship("model_missing", "has", "model2")  # does not raise error
        mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_with_none_existing(self, mock_reader, mock_writer):
        # model1 and model2 defined without relationships
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1'},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        # model1 and model2 defined without relationships
        dt_dev.deleteRelationship("model1", "has", "model2")
        mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_with_other_existing_relationsips(self, mock_reader, mock_writer):
        # model1 with other relationship to model2
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships' : {'with_other': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model2")
        mock_writer.assert_not_called()

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_with_same_relationship_only_to_other_twins(self, mock_reader, mock_writer):
        # relationship model1 has othermodel and model2 exists
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_with_same_relationship_to_multiple_items(self, mock_reader, mock_writer):
        # relationship model1 has othermodel and model2 exists
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}, {"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "other_model"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_exists_with_only_targeted_removal(self, mock_reader, mock_writer):
        # relationship model1 has model2 already exists
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model2")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1'},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_with_target_missing(self, mock_reader, mock_writer):
        # target of relationship is missing
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model_missing")
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

    @mock.patch('azext_iot.digitaltwins.dev.twins.write_JSON_file')
    @mock.patch('azext_iot.digitaltwins.dev.twins.read_JSON_file')
    def test_delete_relationship_and_keeps_empty_relationship_array(self, mock_reader, mock_writer):
        # retains empty relationship
        mock_reader.return_value = [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': [{"@id": "model2"}]}},
            {'@model': 'model_name', '@id': 'model2'}
        ]
        dt_dev.deleteRelationship("model1", "has", "model2", remove_empty=False)
        mock_writer.assert_called_with("twins.json", [
            {'@model': 'model_name', '@id': 'model1', 'relationships': {'has': []}},
            {'@model': 'model_name', '@id': 'model2'}
        ])

# end of class


if __name__ == '__main__':
    unittest.main()
