# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
from azext_iot.device_certification.command_test import initialize_workspace


class InitClass(unittest.TestCase):
    @mock.patch('os.path.join')
    @mock.patch('builtins.open', create=True)
    @mock.patch('json.dump')
    def test_init_with_no_working_folder(self, mock_dump, mock_open, mock_join):
        initialize_workspace(self, 'My product')
        mock_join.assert_called_with('PnPCert', 'product_configuration.json')
        mock_open.assert_called()
        mock_dump.assert_called()