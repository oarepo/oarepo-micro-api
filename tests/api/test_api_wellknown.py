# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test record and files."""

from flask import url_for
from webtest import AppError


def test_readiness_probes(app, wsgi):
    url = url_for('oarepo-heartbeat.liveliness', _external=True)
    assert url.startswith('http://localhost/api/')

    res = wsgi.get(url)
    assert res.status_code != 404


def test_liveliness_probes(app, wsgi):
    url = url_for('oarepo-heartbeat.readiness', _external=True)
    assert url.startswith('http://localhost/api/')

    res = wsgi.get(url)
    assert res.status_code != 404


def test_generic_api(wsgi):
    url = url_for('invenio_records_rest.recid_list', _external=True)
    assert url.startswith('http://localhost/api/')

    res = wsgi.get(url)
    assert res.status_code != 404
