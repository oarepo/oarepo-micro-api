# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.


def term_facet(field, order='desc', size=100):
    return {
        'terms': {
            'field': field,
            'size': size,
            "order": {"_key": order}
        },
    }


def nested_facet(nested_path, agg_path, order='desc', size=100):
    return {
        'nested': {
            'path': nested_path
        },
        'aggs': {
            agg_path: term_facet(agg_path, order, size)
        }
    }


def title_lang_facet(order='desc', size=100):
    return nested_facet("title", "title.lang", order, size)
