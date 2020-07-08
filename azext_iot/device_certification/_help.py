# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Help definitions for Device Certification commands.
"""

from knack.help_files import helps

def load_help():
    helps["iot device-certification"] = """
        type: group
        short-summary: Manage device testing for product certification
    """
# certification requirements
    helps["iot device-certification requirement"] = """
        type: group
        short-summary: Manage device certification requirements
    """
    helps["iot device-certification requirement list"] = """
        type: command
        short-summary: Get certification requirements
        examples:
        - name: Basic usage
          text: >
            az iot device-certification requirement list
    """
# Device Tests
    helps["iot device-certification test"] = """
        type: group
        short-summary: Manage device tests for certification
    """
    helps["iot device-certification test create"] = """
        type: command
        short-summary: Create a new device test for product certification
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test create --configuration-file {configuration_file}
        - name: Generate provisioning configuration info from the server
          text: >
            az iot device-certification test create --configuration-file {configuration_file} --provisioning
    """
    helps["iot device-certification test init"] = """
        type: command
        short-summary: Used to initialize local workspace for a new product certification
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test init --product-name {product_name}
    """
    helps["iot device-certification test search"] = """
        type: command
        short-summary: Search product repository for testing data
        examples:
        - name: Search by product id
          text: >
            az iot device-certification test search --product-id {product_id}
        - name: Search by DPS registration
          text: >
            az iot device-certification test search --registration-id {registration_id}
        - name: Search by x509 certifcate common name (CN)
          text: >
            az iot device-certification test search --certificate-name {certificate_name}
        - name: Search by multiple values
          text: >
            az iot device-certification test search --product-id {product_id} --certificate-name {certificate_name}
    """
    helps["iot device-certification test show"] = """
        type: command
        short-summary: View device test data
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test show --test-id {test_id}
    """
    helps["iot device-certification test update"] = """
        type: command
        short-summary: Update the device certification test data
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test update --test-id {test_id} --configuration-file {configuration_file}
    """
# Device Test Tasks
    helps["iot device-certification test-task"] = """
        type: group
        short-summary: Manage device testing certification tasks
    """
    helps["iot device-certification test-task create"] = """
        type: command
        short-summary: Queue a new testing task. Only one testing task can be running at a time
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test-task create --test-id {test_id}
    """
    helps["iot device-certification test-task delete"] = """
        type: command
        short-summary: Cancel a running task matching the specified --task-id
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test-task delete --test-id {test_id} --task-d {task_id}
    """
    helps["iot device-certification test-task show"] = """
        type: command
        short-summary: Show the status of a testing task. Use --running for current running task or --task-id
        examples:
        - name: Task status by --task-id
          text: >
            az iot device-certification test-task show --test-id {test_id} --task-id {task_id}
        - name: Currently running task of device test
          text: >
            az iot device-certification test-task show --test-id {test_id} --running
    """
# Test Cases
    helps["iot device-certification test-case"] = """
        type: group
        short-summary: Manage device testing certification test cases
    """
    helps["iot device-certification test-case update"] = """
        type: command
        short-summary: Update the device certification test case data
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test-case update --test-id {test_id} --configuration-file {configuration_file}
    """
    helps["iot device-certification test-case list"] = """
        type: command
        short-summary: List the test cases of a device certification test
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test-case list --test-id {test_id}
    """
# Test Runs
    helps["iot device-certification test-run"] = """
        type: group
        short-summary: Manage device testing certification test runs
    """
    helps["iot device-certification test-run create"] = """
        type: command
        short-summary: Submit a completed test run to the partner/product service
        examples:
        - name: Basic usage
          text: >
            az iot device-certification test-run create --test-id {test_id}
    """
    helps["iot device-certification test-run show"] = """
        type: command
        short-summary: Show the status of a testing run. Use --latest for most recently queued test run
        examples:
        - name: Testing status by --run-id
          text: >
            az iot device-certification test-task show --test-id {test_id} --run-id {run_id}
        - name: Latest device test run
          text: >
            az iot device-certification test-run show --test-id {test_id} --latest
    """
