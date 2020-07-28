# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
from azext_iot.product.command_product import initialize_workspace


class InitClass(unittest.TestCase):
    @mock.patch("os.path.exists")
    @mock.patch("os.path.join")
    @mock.patch("os.mkdir")
    @mock.patch("builtins.open", create=True)
    @mock.patch("json.dump")
    def test_init_with_no_working_folder(
        self, mock_dump, mock_open, mock_mkdir, mock_join, mock_exists
    ):
        mock_exists.return_value = False
        mock_join.return_value = "filepath"
        initialize_workspace(self, "My product")
        mock_mkdir.assert_called_with("PnPCert")
        mock_join.assert_called_with("PnPCert", "product_configuration.json")
        mock_open.assert_called_with(file="filepath", mode="w+", encoding="utf-8")
        mock_dump.assert_called()
        call = mock_dump.call_args
        call_kwargs = call[1]
        self.assertTrue(call_kwargs["obj"]["name"] == "My product")

    @mock.patch("os.path.exists")
    @mock.patch("os.path.join")
    @mock.patch("os.mkdir")
    @mock.patch("builtins.open", create=True)
    @mock.patch("json.dump")
    def test_init_with_working_folder(
        self, mock_dump, mock_open, mock_mkdir, mock_join, mock_exists
    ):
        mock_exists.return_value = False
        mock_join.return_value = "filepath"
        initialize_workspace(self, "My product", "my folder")
        mock_mkdir.assert_called_with("my folder")
        mock_join.assert_called_with("my folder", "product_configuration.json")
        mock_open.assert_called_with(file="filepath", mode="w+", encoding="utf-8")
        mock_dump.assert_called()
        call = mock_dump.call_args
        call_kwargs = call[1]
        self.assertTrue(call_kwargs["obj"]["name"] == "My product")
