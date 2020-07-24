# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import LiveScenarioTest


class TestTestShowInt(LiveScenarioTest):
    def __init__(
        self, test_case
    ):
        self.test_id = '9825514b-27e6-4563-8cd9-2b384f3ac10d'
        self.product_id = 'test-product'
        super(TestTestShowInt, self).__init__(test_case)

    def test_show_test(self):
        # call the GET /deviceTest/{test_id}
        output = self.cmd(
            'iot product test show -t {}'.format(
                self.test_id,
            )
        ).get_output_in_json()

        assert output['productId'] == self.product_id
        assert output['id'] == self.test_id
