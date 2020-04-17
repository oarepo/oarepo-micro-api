#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE oarepo-micro-api WITH LOGIN PASSWORD 'oarepo-micro-api';
    ALTER ROLE oarepo-micro-api CREATEDB;
    \du;
EOSQL
