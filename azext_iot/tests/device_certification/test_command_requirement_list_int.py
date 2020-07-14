# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import LiveScenarioTest


class TestRequirementList(LiveScenarioTest):

    def test_list_default(self):
        create_output = self.cmd(
            'iot device-certification requirement list'
        ).get_output_in_json()
        expected = [
            {
                "badgeType": "IotDevice",
                "provisioningRequirement": {
                    "provisioningTypes": [
                        "SymmetricKey",
                        "TPM",
                        "X509"
                    ]
                }
            }
        ]
        assert create_output == expected

    def test_list_device(self):
        create_output = self.cmd(
            'iot device-certification requirement list --badge-type IotDevice'
        ).get_output_in_json()
        expected = [
            {
                "badgeType": "IotDevice",
                "provisioningRequirement": {
                    "provisioningTypes": [
                        "SymmetricKey",
                        "TPM",
                        "X509"
                    ]
                }
            }
        ]
        assert create_output == expected

    def test_list_edge(self):
        create_output = self.cmd(
            'iot device-certification requirement list --badge-type IotEdgeCompatible'
        ).get_output_in_json()
        expected = [
            {
                "badgeType": "IotEdgeCompatible",
                "provisioningRequirement": {
                    "provisioningTypes": [
                        "ConnectionString"
                    ]
                }
            }
        ]
        assert create_output == expected

    def test_list_pnp(self):
        create_output = self.cmd(
            'iot device-certification requirement list --badge-type Pnp'
        ).get_output_in_json()
        expected = [
            {
                "badgeType": "Pnp",
                "provisioningRequirement": {
                    "provisioningTypes": [
                        "SymmetricKey",
                        "TPM",
                        "X509"
                    ]
                }
            }
        ]
        assert create_output == expected
