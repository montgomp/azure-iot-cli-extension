# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mock
from knack.util import CLIError
from azext_iot.product.command_tests import create


class TestTestCreateUnit(unittest.TestCase):
    def __init__(
        self, test_case
    ):
        self.product_id = 'b70a3805-5800-4272-93f2-1b4d0150f683'
        super(TestTestCreateUnit, self).__init__(test_case)

    def test_create_with_no_parameters_fails(self):
        with self.assertRaises(CLIError):
            create(self)

    def test_create_with_x509_and_no_certificate_fails(self):
        with self.assertRaises(CLIError) as context:
            create(self, attestation_type='x509')

            self.assertTrue('If attestation type is x509, certificate path is required', context.exception)

    def test_create_with_tpm_and_no_endorsement_key_fails(self):
        with self.assertRaises(CLIError) as context:
            create(self, attestation_type='tpm')

            self.assertTrue('If attestation type is tpm, endorsement key is required', context.exception)

    def test_create_with_pnp_and_no_models_fails(self):
        with self.assertRaises(CLIError) as context:
            create(self, badge_type='pnp')

            self.assertTrue('If badge type is Pnp, models is required', context.exception)

    def test_create_with_missing_device_type_fails(self):
        with self.assertRaises(CLIError) as context:
            create(
                self,
                attestation_type='symmetricKey',
                product_id=self.product_id,
                badge_type='pnp',
                models='models_folder'
            )

            self.assertTrue(
                'If configuration file is not specified, attestation and device definition parameters must be specified',
                context.exception
            )

    def test_create_with_missing_product_id_fails(self):
        with self.assertRaises(CLIError) as context:
            create(
                self,
                attestation_type='symmetricKey',
                device_type='devkit',
                badge_type='pnp',
                models='models_folder'
            )

            self.assertTrue(
                'If configuration file is not specified, attestation and device definition parameters must be specified',
                context.exception
            )

    @mock.patch('azext_iot.product.command_tests._process_models_directory')
    @mock.patch('azext_iot.sdk.product.aicsapi.AICSAPI.create_device_test')
    def test_create_with_default_badge_type_doesnt_check_models(self, mock_service, mock_process_models):
        create(
            self,
            attestation_type='symmetricKey',
            product_id=self.product_id,
            device_type='devkit',
            models='models_folder'
        )

        mock_process_models.assert_not_called()
        mock_service.assert_called_with(
            False,
            body={
                'validationType': 'Certification',
                'productId': self.product_id,
                'deviceType': 'devkit',
                'provisioningConfiguration': {
                    'type': 'symmetricKey',
                    'symmetricKeyEnrollmentInformation': {}
                },
                'certificationBadgeConfigurations': [
                    {'type': 'IotDevice'}
                ]
            }
        )

    @mock.patch('azext_iot.product.command_tests._process_models_directory')
    @mock.patch('azext_iot.sdk.product.aicsapi.AICSAPI.create_device_test')
    def test_create_with_pnp_badge_type_checks_models(self, mock_service, mock_process_models):
        mock_process_models.return_value = [
            "{\"@id\":\"model1\"}",
            "{\"@id\":\"model2\"}",
            "{\"@id\":\"model3\"}"
        ]
        create(
            self,
            attestation_type='symmetricKey',
            product_id=self.product_id,
            device_type='devkit',
            models='models_folder',
            badge_type='Pnp'
        )

        mock_process_models.assert_called_with('models_folder')
        mock_service.assert_called_with(
            False,
            body={
                'validationType': 'Certification',
                'productId': self.product_id,
                'deviceType': 'devkit',
                'provisioningConfiguration': {
                    'type': 'symmetricKey',
                    'symmetricKeyEnrollmentInformation': {}
                },
                'certificationBadgeConfigurations': [
                    {
                        'type': 'Pnp',
                        'digitalTwinModelDefinitions': [
                            '{"@id":"model1"}',
                            '{"@id":"model2"}',
                            '{"@id":"model3"}'
                        ]
                    }
                ]
            }
        )

    @mock.patch('azext_iot.product.command_tests._read_certificate_from_file')
    @mock.patch('azext_iot.product.command_tests._process_models_directory')
    @mock.patch('azext_iot.sdk.product.aicsapi.AICSAPI.create_device_test')
    def test_create_with_cert_auth_reads_cert_file(self, mock_service, mock_process_models, mock_read_certificate):
        mock_read_certificate.return_value = "MockBase64String"
        mock_process_models.return_value = [
            "{\"@id\":\"model1\"}",
            "{\"@id\":\"model2\"}",
            "{\"@id\":\"model3\"}"
        ]
        create(
            self,
            attestation_type='x509',
            product_id=self.product_id,
            device_type='devkit',
            models='models_folder',
            badge_type='Pnp',
            certificate_path='mycertificate.cer'
        )

        mock_read_certificate.assert_called_with('mycertificate.cer')
        mock_process_models.assert_called_with('models_folder')
        mock_service.assert_called_with(
            False,
            body={
                'validationType': 'Certification',
                'productId': self.product_id,
                'deviceType': 'devkit',
                'provisioningConfiguration': {
                    'type': 'x509',
                    'x509EnrollmentInformation': {
                        'base64EncodedX509Certificate': 'MockBase64String'
                    }
                },
                'certificationBadgeConfigurations': [
                    {
                        'type': 'Pnp',
                        'digitalTwinModelDefinitions': [
                            '{"@id":"model1"}',
                            '{"@id":"model2"}',
                            '{"@id":"model3"}'
                        ]
                    }
                ]
            }
        )

    @mock.patch('azext_iot.product.command_tests._read_certificate_from_file')
    @mock.patch('azext_iot.product.command_tests._process_models_directory')
    @mock.patch('azext_iot.sdk.product.aicsapi.AICSAPI.create_device_test')
    def test_create_with_tpm(self, mock_service, mock_process_models, mock_read_certificate):
        mock_process_models.return_value = [
            "{\"@id\":\"model1\"}",
            "{\"@id\":\"model2\"}",
            "{\"@id\":\"model3\"}"
        ]
        create(
            self,
            attestation_type='tpm',
            endorsement_key='12345',
            product_id=self.product_id,
            device_type='devkit',
            models='models_folder',
            badge_type='Pnp',
            certificate_path='mycertificate.cer'
        )

        mock_read_certificate.assert_not_called()
        mock_process_models.assert_called_with('models_folder')
        mock_service.assert_called_with(
            False,
            body={
                'validationType': 'Certification',
                'productId': self.product_id,
                'deviceType': 'devkit',
                'provisioningConfiguration': {
                    'type': 'tpm',
                    'tpmEnrollmentInformation': {
                        'endorsementKey': '12345'
                    }
                },
                'certificationBadgeConfigurations': [
                    {
                        'type': 'Pnp',
                        'digitalTwinModelDefinitions': [
                            '{"@id":"model1"}',
                            '{"@id":"model2"}',
                            '{"@id":"model3"}'
                        ]
                    }
                ]
            }
        )

    @mock.patch('azext_iot.sdk.product.aicsapi.AICSAPI.create_device_test')
    @mock.patch('azext_iot.product.command_tests._create_from_file')
    def test_create_with_configuration_file(self, mock_from_file, mock_sdk_create):
        mock_file_data = {
            'mock': 'data'
        }
        mock_from_file.return_value = mock_file_data
        create(self, configuration_file='somefile')
        mock_from_file.assert_called_with('somefile')
        mock_sdk_create.assert_called_with(
            False,
            body=mock_file_data
        )
