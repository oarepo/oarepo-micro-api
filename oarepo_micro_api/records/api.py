# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Records API."""

from __future__ import absolute_import, print_function

from invenio_records_files.api import Record as FilesRecord

from oarepo_micro_api.records.constants import ACL_ALLOWED_SCHEMAS, ACL_PREFERRED_SCHEMA


class Record(FilesRecord):
    """ACL enabled Demo Record."""
    _schema = "records/record-v1.0.0.json"
    ALLOWED_SCHEMAS = ACL_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = ACL_PREFERRED_SCHEMA
