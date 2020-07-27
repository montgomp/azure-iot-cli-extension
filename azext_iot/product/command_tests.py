# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from uuid import uuid4
from azext_iot.product.providers.aics import AICSProvider
from azext_iot.sdk.product.models import DeviceTestSearchOptions
from azext_iot.product.shared import BadgeType, AttestationType
from knack.log import get_logger
from knack.util import CLIError
import os

logger = get_logger(__name__)


def initialize_workspace(cmd, product_name, working_folder="PnPCert"):
    id = uuid4()
    if not os.path.exists(working_folder):
        os.mkdir(working_folder)

    product_config = {
        "id": str(id),
        "name": product_name,
        "industryTemplates": [
            "InstoreAnalytics |"
            + " DigitalDistributionCenter |"
            + " ConnectedLogistics |"
            + " SmartInventoryManagement |"
            + " ContinuousPatientMonitoring |"
            + " SmartMeterAnalytics |"
            + " SolarPowerMonitoring |"
            + " WaterQualityMonitoring |"
            + " WaterConsumptionMonitoring |"
            + " ConnectedWasteManagement |"
            + " ShelfAvailability"
        ],
        "shortDescription": "string - max length 100",
        "longDescription": "string - max length 1200",
        "dimensions": {
            "length": {"value": 0, "displayUnit": "cm | @in"},
            "width": {"value": 0, "displayUnit": "cm | @in"},
            "height": {"value": 0, "displayUnit": "cm | @in"},
        },
        "weight": {"value": 0, "displayUnit": "g | lb"},
        "deviceType": "FinishedProduct | DevKit",
        "geoAvailability": ["Worldwide | EMEA | APAC_Except_Japan | Americas | Japan"],
        "marketingPage": "url",
        "purchaseURL": "url",
        "salesContact": "url",
        "caseStudyURL": "url",
        "languages": ["C | CSharp | Java | JavaScript | Python"],
        "os": [""],
        "cloudProtocols": ["AMQPS | AMQPS_Websockets | MQTT | MQTT_Websockets | HTTPS"],
        "industrialProtocols": [
            "CAN_Bus | EtherCAT | Modbus | OPC_Classic | OPC_UA | PROFINET | ZigBee | PPMP | Others"
        ],
        "connectivity": ["Bluetooth | LAN | WIFI | LTE | ThreeG | Others"],
        "hardwareInterfaces": ["GPIO | I2C_SPI | COM | USB | Others"],
        "integratedSensors": [
            "GPS |"
            + " Touch |"
            + " LED |"
            + " Light |"
            + " Gas |"
            + " Noise |"
            + " Proximity |"
            + " Temperature |"
            + " Humidity |"
            + " Pressure |"
            + " Accelerometers |"
            + " Weight |"
            + " Soil_Alkalinity |"
            + " Vibrations |"
            + " Image_capture |"
            + " Motion_Detection |"
            + " Chemical_compound_presence |"
            + " No_Sensors"
        ],
        "secureHardware": ["TPM | DICE | SIM_eSIM | Smartcard | Others"],
        "numOfHardwareComponents": 1,
        "componentType": "SoM_SoC | Carrier_Board",
        "componentName": "Video_SoM | Audio_SoM | Video_Carrier_Board | Others",
        "processorArchitecture": "arm | arm64 | x86 | amd64",
        "processorManufacturer": "string",
        "totalStorage": {"value": 0, "displayUnit": "b | kb | mb | gb"},
        "totalMemory": {"value": 0, "displayUnit": "b | kb | mb | gb"},
        "battery": {"value": 0, "displayUnit": "mwH"},
        "hardwareAcceleratorManufacturer": "string",
        "hardwareAcceleratorName": "string",
        "hardwareAcceleratorVersion": "string",
        "industryCertifications": ["FCC | ISCC | Others"],
        "industryCertificationExternalLink": "url",
        "distributors": [{"name": "string", "purchaseUrl": "url"}],
        "techSpecURL": "url",
        "firmwareImageURL": "url",
    }

    from json import dump
    from os import path

    with open(
        file=path.join(working_folder, "product_configuration.json"),
        mode="w+",
        encoding="utf-8",
    ) as f:
        dump(obj=product_config, fp=f, indent=4, sort_keys=False)


def create(
    cmd,
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
    if attestation_type == AttestationType.x509.value and not certificate_path:
        raise CLIError("If attestation type is x509, certificate path is required")
    if attestation_type == AttestationType.tpm.value and not endorsement_key:
        raise CLIError("If attestation type is TPM, endorsement key is required")
    if badge_type == BadgeType.Pnp.value and not models:
        raise CLIError("If badge type is Pnp, models is required")
    if badge_type == BadgeType.IotEdgeCompatible.value and not all(
        [connection_string, attestation_type == AttestationType.connectionString.value, ]
    ):
        raise CLIError(
            "Connection string is required for Edge Compatible modules testing"
        )
    if badge_type != BadgeType.IotEdgeCompatible.value and (
        connection_string or attestation_type == AttestationType.connectionString.value
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

    ap = AICSProvider(cmd)
    return ap.create_test(
        test_configuration=test_configuration, provisioning=provisioning
    )


def show(cmd, test_id):
    ap = AICSProvider(cmd)
    return ap.show_test(test_id)


def update(
    cmd,
    test_id,
    configuration_file=None,
    attestation_type=None,
    certificate_path=None,
    connection_string=None,
    endorsement_key=None,
    badge_type=None,
    models=None,
):
    provisioning = False
    # verify required parameters for various options
    if attestation_type == AttestationType.x509.value and not certificate_path:
        raise CLIError("If attestation type is x509, certificate path is required")
    if attestation_type == AttestationType.tpm.value and not endorsement_key:
        raise CLIError("If attestation type is tpm, endorsement key is required")
    if badge_type == BadgeType.Pnp.value and not models:
        raise CLIError("If badge type is Pnp, models is required")
    if badge_type == BadgeType.IotEdgeCompatible.value and not all(
        [connection_string, attestation_type == AttestationType.connectionString.value, ]
    ):
        raise CLIError(
            "Connection string is required for Edge Compatible modules testing"
        )
    if badge_type != BadgeType.IotEdgeCompatible.value and (
        connection_string or attestation_type == AttestationType.connectionString.value
    ):
        raise CLIError(
            "Connection string is only available for Edge Compatible modules testing"
        )
    ap = AICSProvider(cmd)
    if configuration_file:
        test_configuration = _create_from_file(configuration_file)
        return ap.update_test(test_id=test_id, test_configuration=test_configuration, provisioning=provisioning)

    if not any([attestation_type, badge_type, models]):
        raise CLIError(
            "Configuration file, attestation information, or device configuration must be specified"
        )

    test_configuration = ap.show_test(test_id=test_id)

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
            {"type": BadgeType.Pnp.value, "digitalTwinModelDefinitions": models_array, }
        ]
    elif badge_type:
        test_configuration["certificationBadgeConfigurations"] = [{"type": badge_type}]

    return ap.update_test(test_id=test_id, test_configuration=test_configuration, provisioning=provisioning)


def search(cmd, product_id=None, registration_id=None, certificate_name=None):
    if not any([product_id or registration_id or certificate_name]):
        raise CLIError("At least one search criteria must be specified")

    ap = AICSProvider(cmd)
    searchOptions = DeviceTestSearchOptions(
        product_id=product_id,
        dps_registration_id=registration_id,
        dps_x509_certificate_common_name=certificate_name,
    )
    return ap.search_test(searchOptions)


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


def _read_certificate_from_file(certificate_path):
    with open(file=certificate_path, mode="rb") as f:
        data = f.read()

        from base64 import encodestring

        return encodestring(data)


def _create_from_file(configuration_file):
    if not (os.path.exists(configuration_file)):
        raise CLIError("Specified configuration file does not exist")

    # read the json file and POST /deviceTests
    with open(file=configuration_file, encoding="utf-8") as f:
        file_contents = f.read()

        from json import loads

        return loads(file_contents)
