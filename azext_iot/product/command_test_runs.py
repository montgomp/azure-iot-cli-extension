# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azext_iot.product.providers.aics import AICSProvider

def show(cmd, test_id, run_id=None, wait=False, poll_interval=3):
    ap = AICSProvider(cmd)
    if run_id:
        return ap.show_test_run(test_id=test_id,run_id=run_id)
    return ap.show_test_run_latest(test_id=test_id)


def submit(cmd, test_id, run_id):
    ap = AICSProvider(cmd)
    return ap.submit_test_run(test_id=test_id, run_id=run_id)
