# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
# Dockerfile that builds a fully functional image of your app.
#
# Note: It is important to keep the commands in this file in sync with your
# boostrap script located in ./scripts/bootstrap.
#
# In order to increase the build speed, we are extending this image from a base
# image (built with Dockerfile.base) which only includes your Python
# dependencies.

ARG DEPENDENCIES_VERSION=latest
FROM oarepo-api-base:${DEPENDENCIES_VERSION}

ENTRYPOINT [ "bash", "-c"]
