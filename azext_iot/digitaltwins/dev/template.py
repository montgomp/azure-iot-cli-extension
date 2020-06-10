# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
from knack.util import CLIError
from zipfile import ZipFile


def activate_template(name):
    try:
        url = lookup_template_url(name)
        file_name = download_source(url)

        ZipFile(os.path.join('.', file_name), 'r').extractall('.')
    except Exception:
        os.unlink(file_name)
        raise CLIError('Unable to download template from {}'.format(url))


def download_source(url):
    import requests

    file_name = url.split('/')[-1]

    req = requests.get(url, allow_redirects=True)
    open(file_name, 'wb+').write(req.content)

    return file_name


def lookup_template_url(name):
    templates = {

    }
    if name in templates:
        return templates[name]

    raise CLIError('No known template named "{}".'.format(name))
