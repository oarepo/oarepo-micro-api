# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test record and files."""

import json

from flask import url_for
from invenio_base import create_cli
from invenio_search import current_search
from webtest import AppError


def _run_command(runner, command, catch_exceptions=False):
    cli = create_cli()
    return runner.invoke(cli, command, catch_exceptions=catch_exceptions)


def setup_environment(runner):
    _run_command(runner, "db destroy --yes-i-know")
    _run_command(runner, "db init")
    _run_command(runner, "index destroy --force --yes-i-know")
    _run_command(runner, "index init --force")


def test_readiness_probes(app, wsgi):
    setup_environment(app.test_cli_runner())
    url = url_for('oarepo-heartbeat.liveliness', _external=True) \
        .replace('http', 'https')

    res = None
    try:
        res = wsgi.get(url)
    except AppError as e:
        assert False, 'liveliness check fails on {}'.format(e)
    res_dict = res.json
    assert res.status_code == 200
    assert res_dict == {}


def test_liveliness_probes(app, wsgi):
    setup_environment(app.test_cli_runner())
    url = url_for('oarepo-heartbeat.readiness', _external=True) \
        .replace('http', 'https')

    res = None
    try:
        res = wsgi.get(url)
    except AppError as e:
        assert False, 'readiness check fails on {}'.format(e)
    res_dict = res.json
    assert res.status_code == 200
    assert res_dict == {}


def test_generic_api(client):
    pass
