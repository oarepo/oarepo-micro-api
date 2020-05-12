# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.
from elasticsearch_dsl import Q


def nested_filter(prefix, field, field_query=None, nested_query='terms'):
    """Create a term filter.
    :param prefix: Field path prefix
    :param field: Field name.
    :param field_query Field query function
    :param nested_query Nested query name
    :returns: Function that returns the Terms query.
    """
    field = prefix + '.' + field

    def inner(values):
        if field_query:
            query = field_query(field)(values)
        else:
            query = Q(nested_query, **{field: values})
        return Q('nested', path=prefix, query=query)

    return inner


def language_aware_match_filter(field):
    return nested_filter(field, 'value', nested_query='match')


def nested_terms_filter(prefix, field, field_query=None):
    """Create a nested terms filter.

    :param field: Field name.
    :returns: Function that returns the Terms query.
    """

    field = prefix + '.' + field

    def inner(values):
        if field_query:
            query = field_query(field)(values)
        else:
            query = Q('terms', **{field: values})
        return Q('nested', path=prefix, query=query)

    return inner
