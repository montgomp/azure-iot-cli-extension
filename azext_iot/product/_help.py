# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Help definitions for Product Certification commands.
"""

from knack.help_files import helps


def load_help():
    helps[
        "iot product"
    ] = """
        type: group
        short-summary: Manage device testing for product certification
    """
    # certification requirements
    helps[
        "iot product requirement"
    ] = """
        type: group
        short-summary: Manage product certification requirements
    """
    helps[
        "iot product requirement list"
    ] = """
        type: command
        short-summary: Get certification requirements
        long-summary: |
                      Discover information about provisioning attestation methods that are supported for each badge type
        examples:
        - name: Basic usage
          text: >
            az iot product requirement list
    """
    helps[
        "iot product init"
    ] = """
        type: command
        short-summary: Used to initialize local workspace for a new product certification
        examples:
        - name: Basic usage
          text: >
            az iot product init --product-name {product_name}
        - name: Specify working folder
          text: >
            az iot product init --product-name {product_name} --working-folder {working_folder}
    """
