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
        self.test_id = 'daa7a1c2-f543-4c00-8046-69d410ed8541'
        self.product_id = 'b70a3805-5800-4272-93f2-1b4d0150f683'
        super(TestTestCreateInt, self).__init__(test_case)

    def test_create_symmetric_key(self):
        # call the GET /deviceTest/{test_id}
        output = self.cmd(
            'iot product test show -t {}'.format(
                self.test_id,
            )
        ).get_output_in_json()

        assert output['productId'] == self.product_id
        assert output['id'] == self.test_id
