# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Utility functions."""
import sqlalchemy
from invenio_db import db
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets


def record_from_bucket(bucket_id):
    record_bucket = \
        RecordsBuckets.query.filter_by(bucket_id=bucket_id).first()
    if record_bucket:
        record = Record.get_record(record_bucket.record_id)
        return record
    return None
