#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# Oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

SETUP_PY='./setup.py'

MAXI=4
SLEEP=20
PKG="oarepo"
OAREPO_VER=$(sed -n "/^OAREPO_VERSION/ { s/^OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '\([0-9\.a-z]\+\)')/\1/; p; }" "${SETUP_PY}")

echo "$(date '+%y%m%d-%H%M%S') check_pypi: $PKG-ver=$OAREPO_VER"

if [[ "$OAREPO_VER" =~ ^([0-9]+\.){2}[0-9]+$ ]]; then
  I=0
  while [[ $((++I)) -le $MAXI ]]; do echo -n '.'
    sleep $SLEEP
    curl -s -f "https://pypi.org/project/${PKG}/${OAREPO_VER}/" >/dev/null && break
    echo "${PKG}-${OAREPO_VER} not available (attempt $I of $MAXI)"
  done
  if [[ $I -gt $MAXI ]]; then
    echo "max retries exceeded ($MAXI)"
    exit 2
  else
    echo "OK: ${PKG}-${OAREPO_VER}"
  fi
  echo "$(date '+%y%m%d-%H%M%S') check_pypi: Done."
else
  echo "ERR: version string format check failed ($OAREPO_VER)"
  exit 1
fi
