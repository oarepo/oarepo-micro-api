# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OARepo REST API microservice"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_micro_api', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo-micro-api',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='oarepo-micro-api Invenio',
    license='MIT',
    author='Miroslav Bauer @ CESNET',
    author_email='bauer@cesnet.cz',
    url='https://github.com/oarepo/oarepo-micro-api',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'oarepo = invenio_app.cli:cli',
        ],
        "invenio_base.api_apps": [
            "oarepo_micro_api = oarepo_micro_api.records.ext:OARepoMicroAPI",
        ],
        "flask.commands": [
            "demo = oarepo_micro_api.cli:demo",
            "setup = oarepo_micro_api.cli:setup",
        ],
        'invenio_config.module': [
            'oarepo_micro_api = oarepo_micro_api.config',
        ],
        'invenio_i18n.translations': [
            'messages = oarepo_micro_api',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
