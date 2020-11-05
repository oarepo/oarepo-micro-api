# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OARepo Micro API extension."""
from flask import jsonify
from invenio_base.signals import app_loaded


class OARepoMicroAPI:
    def __init__(self, app, **kwargs):
        app.extensions['oarepo-micro-api'] = self


@app_loaded.connect
def loaded(target, app, **kwargs):
    def handler(exc, *args, **kwargs):
        code = getattr(exc, 'code', 400)
        ret = jsonify({'status': 'error', 'message': str(exc)})
        ret.status_code = code
        return ret

    # Register error handlers.
    app.register_error_handler(400, handler)
    app.register_error_handler(401, handler)
    app.register_error_handler(403, handler)
    app.register_error_handler(404, handler)
    app.register_error_handler(405, handler)
    app.register_error_handler(429, handler)
    app.register_error_handler(500, handler)
