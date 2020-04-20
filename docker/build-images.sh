#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Build dependencies image
docker build -f Dockerfile.base -t oarepo-api-base:latest .
docker build -f Dockerfile.base -t oarepo-api-base:3.2.1 .

# Build application image
docker build --build-arg DEPENDENCIES_VERSION=3.2.1 . -t oarepo-api
