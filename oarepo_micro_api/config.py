# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration for OARepo Micro API.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""

from __future__ import absolute_import, print_function

# TODO: enable for iiif previews
# from invenio_previewer.config import PREVIEWER_PREFERENCE as BASE_PREFERENCE
from invenio_cesnet_proxyidp.remote import ProxyIDPAuthRemote


def _(x):
    """Identity function used to trigger string extraction."""
    return x


# Rate limiting
# =============
#: Storage for ratelimiter.
RATELIMIT_STORAGE_URL = 'redis://localhost:6379/3'
RATELIMIT_ENABLED = True

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Prague'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    # ('fr', _('French'))
]

APPLICATION_ROOT = '/api/'

# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "du-support@cesnet.cz"
#: Disable email sending by default.
MAIL_SUPPRESS_SEND = True

# Accounts
# ========
#: Email address used as sender of account registration emails.
SECURITY_EMAIL_SENDER = SUPPORT_EMAIL
#: Email subject for account registration emails.
SECURITY_EMAIL_SUBJECT_REGISTER = _(
    "Welcome to OARepo")
#: Redis session storage URL.
ACCOUNTS_SESSION_REDIS_URL = 'redis://localhost:6379/1'
#: Enable session/user id request tracing. This feature will add X-Session-ID
#: and X-User-ID headers to HTTP response. You MUST ensure that NGINX (or other
#: proxies) removes these headers again before sending the response to the
#: client. Set to False, in case of doubt.
ACCOUNTS_USERINFO_HEADERS = True

# Elasticsearch
# =============
import os

ES_USER = os.getenv('OAREPO_ES_USER', None)
ES_PASSWORD = os.getenv('OAREPO_ES_PASSWORD', None)
ES_PARAMS = {}

if ES_USER and ES_PASSWORD:
    ES_PARAMS = dict(http_auth=(ES_USER, ES_PASSWORD))

SEARCH_ELASTIC_HOSTS = [dict(host=h, **ES_PARAMS) for h in
                        os.getenv('OAREPO_SEARCH_ELASTIC_HOSTS', 'localhost').split(',')]

# Celery configuration
# ====================
# TODO: add celery
# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of message broker for Celery (default is RabbitMQ).
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of backend for result storage (default is Redis).
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#: Scheduled tasks configuration (aka cronjobs).
# CELERY_BEAT_SCHEDULE = {
#     'indexer': {
#         'task': 'invenio_indexer.tasks.process_bulk_queue',
#         'schedule': timedelta(minutes=5),
#     },
#     'accounts': {
#         'task': 'invenio_accounts.tasks.clean_session_table',
#         'schedule': timedelta(minutes=60),
#     },
# }

# Database
# ========
#: Database URI including user and password
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://oarepo-micro-api:oarepo-micro-api@localhost/oarepo-micro-api'

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'repozitar.cesnet.cz'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = 'OA_REPO_CHANGE_ME'
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.
APP_ALLOWED_HOSTS = [h for h in os.getenv('OAREPO_APP_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')]

# OAI-PMH
# =======
OAISERVER_ID_PREFIX = 'oai:repozitar.cesnet.cz:'

# Previewers
# ==========
# TODO: enable for previews
#: Include IIIF preview for images.
# PREVIEWER_PREFERENCE = ['iiif_image'] + BASE_PREFERENCE

# Debug
# =====
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available at
# https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration

#: Switches off incept of redirects by Flask-DebugToolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Configures Content Security Policy for PDF Previewer
# Remove it if you are not using PDF Previewer
# TODO: enable for previews
# APP_DEFAULT_SECURE_HEADERS['content_security_policy'] = {
#     'default-src': ["'self'", "'unsafe-inline'"],
#     'object-src': ["'none'"],
#     'style-src': ["'self'", "'unsafe-inline'"],
#     'font-src': ["'self'", "data:", "https://fonts.gstatic.com",
#                  "https://fonts.googleapis.com"],
# }

PROXYIDP_CONFIG = dict(
    base_url='https://login.cesnet.cz/oidc/',
    consumer_key=os.getenv('PROXYIDP_CONSUMER_KEY', 'CHANGE_ME'),
    consumer_secret=os.getenv('PROXYIDP_CONSUMER_SECRET', 'CHANGE_ME'),
    scope=('openid', 'email', 'profile',)
)

OAUTHCLIENT_REMOTE_APPS = dict(
    proxyidp=ProxyIDPAuthRemote().remote_app()
)

INVENIO_OAREPO_UI_LOGIN_URL = '/api/openid/login/proxyidp'

USERPROFILES_EXTEND_SECURITY_FORMS = True
SECURITY_SEND_REGISTER_EMAIL = False
# Disable account confirmation requirement
SECURITY_CONFIRMABLE = False
