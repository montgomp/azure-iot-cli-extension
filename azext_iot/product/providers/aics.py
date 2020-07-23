# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from time import sleep
import os
from azext_iot.product.providers import AICSServiceProvider
from azext_iot.product.shared import (
    TaskType,
    DeviceTestTaskStatus as Status,
    BadgeType,
    AttestationType,
)
from msrestazure.azure_exceptions import CloudError
from knack.util import CLIError

# TODO: Pull argument validation and wait logic from provider into command_{} functions
class AICSProvider(AICSServiceProvider):
    def __init__(self, cmd):
        super(AICSProvider, self).__init__(cmd=cmd)
        self.mgmt_sdk = self.get_mgmt_sdk()

    # Requirements

    def list_requirements(self, badge_type=BadgeType.IotDevice):
        # call to GET /certificationRequirements
        return self.mgmt_sdk.get_device_certification_requirements(
            badge_type=badge_type
        )

    # Test Tasks

    def create_test_task(
        self, test_id, task_type=TaskType.QueueTestRun, wait=False, poll_interval=3
    ):
        final_statuses = [
            Status.failed.value,
            Status.completed.value,
            Status.cancelled.value,
        ]
        status = None
        try:
            response = self.mgmt_sdk.create_device_test_task(
                device_test_id=test_id, task_type=task_type
            )
            if not response:
                raise CLIError(
                    "Failed to create device test task - please ensure a device test exists with Id {}".format(
                        test_id
                    )
                )
            status = response.status
            task_id = response.id
            while all([wait, status, task_id]) and status not in final_statuses:
                sleep(poll_interval)
                response = self.mgmt_sdk.get_device_test_task(
                    task_id=task_id, device_test_id=test_id
                )
                status = response.status
            return response
        except CloudError as e:
            return CLIError(unpack_msrest_error(e))

    def delete_test_task(self, test_id, task_id):
        try:
            return self.mgmt_sdk.cancel_device_test_task(
                task_id=task_id, device_test_id=test_id
            )
        except CloudError as e:
            return CLIError(unpack_msrest_error(e))

    def show_test_task(self, test_id, task_id=None, running=False):
        try:
            if task_id:
                return self.mgmt_sdk.get_device_test_task(
                    task_id=task_id, device_test_id=test_id
                )
            elif running:
                return self.mgmt_sdk.get_running_device_test_tasks(
                    device_test_id=test_id
                )
            else:
                raise CLIError(
                    "Please provide a task-id for individual task details, or use the --running argument to list all running tasks"
                )
        except CloudError as e:
            return CLIError(unpack_msrest_error(e))

    # Tests

    def show_test(self, test_id):
        # call to GET /deviceTests/{deviceTestId}
        return self.mgmt_sdk.get_device_test(device_test_id=test_id)

    def search_test(self, product_id=None, registration_id=None, certificate_name=None):
        # call to POST /deviceTests/search
        if not any([product_id or registration_id or certificate_name]):
            raise CLIError("At least one search criteria must be specified")

        searchOptions = {
            "product_id": product_id,
            "dps_registration_id": registration_id,
            "dps_x509_certificate_common_name": certificate_name,
        }

        return self.mgmt_sdk.search_device_test(body=searchOptions)

    def update_test(
        self,
        test_id,
        configuration_file=None,
        attestation_type=None,
        certificate_path=None,
        connection_string=None,
        endorsement_key=None,
        badge_type=None,
        models=None,
    ):
        # call to PUT /deviceTests
        provisioning = False

        # verify required parameters for vairous options
        if attestation_type == AttestationType.x509.value and not certificate_path:
            raise CLIError("If attestation type is x509, certificate path is required")
        if attestation_type == AttestationType.tpm.value and not endorsement_key:
            raise CLIError("If attestation type is tpm, endorsement key is required")
        if badge_type == BadgeType.Pnp.value and not models:
            raise CLIError("If badge type is Pnp, models is required")
        if badge_type == BadgeType.IotEdgeCompatible.value and not all(
            [
                connection_string,
                attestation_type == AttestationType.connectionString.value,
            ]
        ):
            raise CLIError(
                "Connection string is required for Edge Compatible modules testing"
            )
        if badge_type != BadgeType.IotEdgeCompatible.value and (
            connection_string
            or attestation_type == AttestationType.connectionString.value
        ):
            raise CLIError(
                "Connection string is only available for Edge Compatible modules testing"
            )

        if configuration_file:
            test_configuration = _create_from_file(configuration_file)
            return self.mgmt_sdk.update_device_test(
                device_test_id=test_id,
                generate_provisioning_configuration=provisioning,
                body=test_configuration,
            )

        if not any([attestation_type, badge_type, models]):
            raise CLIError(
                "Configuration file, attestation information, or device configuration must be specified"
            )

        test_configuration = self.mgmt_sdk.get_device_test(
            device_test_id=test_id, raw=True
        ).response.json()

        provisioning_configuration = test_configuration["provisioningConfiguration"]
        registration_id = provisioning_configuration["dpsRegistrationId"]

        # change attestation
        if attestation_type:
            # reset the provisioningConfiguration
            test_configuration["provisioningConfiguration"] = {
                "type": attestation_type,
                "dpsRegistrationId": registration_id,
            }
            provisioning = True
            if attestation_type == AttestationType.symmetricKey.value:
                test_configuration["provisioningConfiguration"][
                    "symmetricKeyEnrollmentInformation"
                ] = {}
            elif attestation_type == AttestationType.tpm.value:
                test_configuration["provisioningConfiguration"][
                    "tpmEnrollmentInformation"
                ] = {"endorsementKey": endorsement_key}
            elif attestation_type == AttestationType.x509.value:
                test_configuration["provisioningConfiguration"][
                    "x509EnrollmentInformation"
                ] = {
                    "base64EncodedX509Certificate": _read_certificate_from_file(
                        certificate_path
                    )
                }
            elif attestation_type == AttestationType.connectionString.value:
                test_configuration["provisioningConfiguration"][
                    "deviceConnectionString"
                ] = connection_string

        # reset PnP models
        badge_config = test_configuration["certificationBadgeConfigurations"]

        if (
            badge_type == BadgeType.Pnp.value
            or badge_config[0]["type"].lower() == BadgeType.Pnp.value.lower()
        ) and models:
            models_array = _process_models_directory(models)
            test_configuration["certificationBadgeConfigurations"] = [
                {
                    "type": BadgeType.Pnp.value,
                    "digitalTwinModelDefinitions": models_array,
                }
            ]
        elif badge_type:
            test_configuration["certificationBadgeConfigurations"] = [
                {"type": badge_type}
            ]

        return self.mgmt_sdk.update_device_test(
            device_test_id=test_id,
            generate_provisioning_configuration=provisioning,
            body=test_configuration,
            raw=True,
        ).response.json()

    def create_test(
        self,
        configuration_file=None,
        product_id=None,
        device_type=None,
        attestation_type=None,
        certificate_path=None,
        connection_string=None,
        endorsement_key=None,
        badge_type=BadgeType.IotDevice.value,
        models=None,
        provisioning=True,
    ):
        # call to POST /deviceTests
        if attestation_type == AttestationType.x509.value and not certificate_path:
            raise CLIError("If attestation type is x509, certificate path is required")
        if attestation_type == AttestationType.tpm.value and not endorsement_key:
            raise CLIError("If attestation type is tpm, endorsement key is required")
        if badge_type == BadgeType.Pnp.value and not models:
            raise CLIError("If badge type is Pnp, models is required")
        if badge_type == BadgeType.IotEdgeCompatible.value and not all(
            [
                connection_string,
                attestation_type == AttestationType.connectionString.value,
            ]
        ):
            raise CLIError(
                "Connection string is required for Edge Compatible modules testing"
            )
        if badge_type != BadgeType.IotEdgeCompatible.value and (
            connection_string
            or attestation_type == AttestationType.connectionString.value
        ):
            raise CLIError(
                "Connection string is only available for Edge Compatible modules testing"
            )
        if not any(
            [
                configuration_file,
                all([device_type, product_id, attestation_type, badge_type]),
            ]
        ):
            raise CLIError(
                "If configuration file is not specified, attestation and device definition parameters must be specified"
            )
        test_configuration = (
            _create_from_file(configuration_file)
            if configuration_file
            else _build_test_configuration(
                product_id=product_id,
                device_type=device_type,
                attestation_type=attestation_type,
                certificate_path=certificate_path,
                endorsement_key=endorsement_key,
                badge_type=badge_type,
                connection_string=connection_string,
                models=models,
            )
        )
        return self.mgmt_sdk.create_device_test(provisioning, body=test_configuration)

    # Test runs

    def show_test_run(self, test_id, run_id):
        return self.mgmt_sdk.get_test_run(test_run_id=run_id, device_test_id=test_id)

    def show_test_run_latest(self, test_id):
        return self.mgmt_sdk.get_latest_test_run(device_test_id=test_id)

    def submit_test_run(self, test_id, run_id):
        return self.mgmt_sdk.submit_test_run(test_run_id=run_id, device_test_id=test_id)

    # Test cases

    def show_test_cases(self, test_id):
        return self.mgmt_sdk.get_test_cases(device_test_id=test_id)

    def update_test_cases(self, test_id, patch):
        return self.mgmt_sdk.update_test_cases(
            device_test_id=test_id, certification_badge_test_cases=patch
        )


def _build_test_configuration(
    product_id,
    device_type,
    attestation_type,
    certificate_path,
    endorsement_key,
    connection_string,
    badge_type,
    models,
):
    config = {
        "validationType": "Certification",
        "productId": product_id,
        "deviceType": device_type,
        "provisioningConfiguration": {"type": attestation_type},
        "certificationBadgeConfigurations": [{"type": badge_type}],
    }
    if attestation_type == AttestationType.symmetricKey.value:
        config["provisioningConfiguration"]["symmetricKeyEnrollmentInformation"] = {}
    elif attestation_type == AttestationType.tpm.value:
        config["provisioningConfiguration"]["tpmEnrollmentInformation"] = {
            "endorsementKey": endorsement_key
        }
    elif attestation_type == AttestationType.x509.value:
        config["provisioningConfiguration"]["x509EnrollmentInformation"] = {
            "base64EncodedX509Certificate": _read_certificate_from_file(
                certificate_path
            )
        }
    elif attestation_type == AttestationType.connectionString.value:
        config["provisioningConfiguration"][
            "deviceConnectionString"
        ] = connection_string

    if badge_type == BadgeType.Pnp.value and models:
        models_array = _process_models_directory(models)
        config["certificationBadgeConfigurations"][0][
            "digitalTwinModelDefinitions"
        ] = models_array

    return config


def _read_certificate_from_file(certificate_path):
    with open(file=certificate_path, mode="rb") as f:
        data = f.read()

        from base64 import encodestring

        return encodestring(data)


def _process_models_directory(from_directory):
    from azext_iot.common.utility import scantree, process_json_arg

    models = []
    for entry in scantree(from_directory):
        if not any([entry.name.endswith(".json"), entry.name.endswith(".dtdl")]):
            logger.debug(
                "Skipping {} - model file must end with .json or .dtdl".format(
                    entry.path
                )
            )
            continue
        entry_json = process_json_arg(content=entry.path, argument_name=entry.name)
        # we need to double-encode the JSON string
        from json import dumps

        models.append(dumps(entry_json))
    return models


def _create_from_file(configuration_file):
    if not (os.path.exists(configuration_file)):
        raise CLIError("Specified configuration file does not exist")

    # read the json file and POST /deviceTests
    with open(file=configuration_file, encoding="utf-8") as f:
        file_contents = f.read()

        from json import loads

        return loads(file_contents)
