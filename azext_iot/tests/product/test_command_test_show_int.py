# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import LiveScenarioTest


class TestTestShowInt(LiveScenarioTest):
    def __init__(self, test_case):
        self.test_id = "524ac74f-752b-4748-9667-45cd09e8a098"
        self.product_id = "81cf6ae4-1702-4158-8abe-72473c9ae5ab"
        super(TestTestShowInt, self).__init__(test_case)

    def test_show_test(self):
        # call the GET /deviceTest/{test_id}
        output = self.cmd(
            "iot product test show -t {}".format(self.test_id,)
        ).get_output_in_json()

        assert output["productId"] == self.product_id
        assert output["id"] == self.test_id
