# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Record serializers."""

from __future__ import absolute_import, print_function

from invenio_records_rest.serializers.citeproc import CiteprocSerializer
from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify

from ..marshmallow import RecordSchemaV1

# Serializers
# ===========
#: JSON serializer definition.
from ..marshmallow.json import CitationSchemaV1

json_v1 = JSONSerializer(RecordSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================
#: JSON record serializer for individual records.
json_v1_response = record_responsify(json_v1, 'application/json')
#: JSON record serializer for search results.
json_v1_search = search_responsify(json_v1, 'application/json')

# Citation serializers
csl_v1 = JSONSerializer(CitationSchemaV1, replace_refs=True)
citeproc_v1 = CiteprocSerializer(csl_v1)
citeproc_v1_response = record_responsify(citeproc_v1, 'text/x-bibliography')

__all__ = (
    'json_v1',
    'json_v1_response',
    'json_v1_search',
    'csl_v1',
    'citeproc_v1',
    'citeproc_v1_response'
)
