# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def show(test_id, run_id=None, latest=False):
    # if run_id GET /deviceTests/{deviceTestId}testRuns/{testRunId}
    # else if latest GET /deviceTests/{deviceTestId}/testRuns/latest
    # else fail
    return True

def create(test_id, run_id):
    # call to POST /deviceTests/{deviceTestId}/testRuns/{testRunId}/submit
    return True
