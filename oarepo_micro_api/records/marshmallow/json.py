# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_jsonschemas import current_jsonschemas
from invenio_oarepo_dc.marshmallow import DCObjectSchemaV1Mixin
from invenio_oarepo_invenio_model.marshmallow import InvenioRecordMetadataSchemaV1Mixin
from invenio_oarepo_multilingual.marshmallow import MultilingualStringSchemaV1
from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import GenFunction, \
    PersistentIdentifier
from marshmallow import fields, missing, INCLUDE


from oarepo_micro_api.records.api import Record


def bucket_from_context(_, context):
    """Get the record's bucket from context."""
    record = (context or {}).get('record', {})
    return record.get('_bucket', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def schema_from_context(_, context):
    """Get the record's schema from context."""
    record = (context or {}).get('record', {})
    return record.get(
        "_schema",
        current_jsonschemas.path_to_url(Record._schema)
    )


class MetadataSchemaV1(InvenioRecordMetadataSchemaV1Mixin,
                       DCObjectSchemaV1Mixin):
    """Schema for the record metadata."""
    abstract = MultilingualStringSchemaV1(required=True)
    description = MultilingualStringSchemaV1(required=True)

    class Meta:
        unknown = INCLUDE


class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""
    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)
