# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import LiveScenarioTest


class TestTestCreateInt(LiveScenarioTest):
    def __init__(
        self, test_case
    ):
        self.product_id = 'b70a3805-5800-4272-93f2-1b4d0150f683'
        super(TestTestCreateInt, self).__init__(test_case)

    def test_create_symmetric_key(self):
        device_type = 'devkit'
        attestation_type = 'symmetrickey'
        badge_type = 'iotdevice'

        # call the POST /deviceTest
        output = self.cmd(
            'iot product test create -p {} --dt {} --at {} --bt {} --provisioning'.format(
                self.product_id,
                device_type,
                attestation_type,
                badge_type
            )
        ).get_output_in_json()

        assert output['productId'] == self.product_id
        assert output['deviceType'] == device_type
        assert output['provisioningConfiguration']['type'] == attestation_type
        # assert service created symmetric key info
        assert output['provisioningConfiguration']['symmetricKeyEnrollmentInformation']['primaryKey']
