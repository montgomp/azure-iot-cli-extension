# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import azext_iot.digitaltwins.dev.main as dt_dev


class MainTest(unittest.TestCase):
    def test_init(self):
        name = "testing"
        # if os.path.exists(os.path.join('.', 'config.json')):
        #     os.remove(os.path.join('.', 'config.json'))
        dt_dev.init_workspace(self, name, force=True)
        config = dt_dev.get_configuration_data()
        self.assertEqual(name, config["name"])
        twins = dt_dev.read_JSON_file("twins.json")
        self.assertEqual([], twins)


if __name__ == '__main__':
    unittest.main()
