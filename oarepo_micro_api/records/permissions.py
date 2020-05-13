# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Permissions for OARepo Micro API."""
from elasticsearch_dsl import Q
from flask_login import current_user
from flask_principal import UserNeed, RoleNeed
from invenio_access import Permission, authenticated_user


def authenticated_permission_factory(record=None):
    return Permission(authenticated_user)


def admin_permission_factory(obj, action=None):
    """Permissions factory for buckets."""
    return Permission(RoleNeed('admin'))


def owner_permission_factory(record=None):
    """Permissions factory for record owners."""
    return Permission(UserNeed(record.get('owner')))


def owner_permission_filter():
    """Search only in owned or system records."""
    ids = [-1]
    cuid = current_user.get_id()
    if cuid:
        ids.append(cuid)
    return Q('terms', owners=ids)
