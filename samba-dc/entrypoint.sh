#!/bin/bash

#
# Copyright (C) 2022 Nethesis S.r.l.
# SPDX-License-Identifier: GPL-3.0-or-later
#

set -e

expand-config

if [ $# -eq 0 ]; then
    extra_args=()
    if [[ -n "${DNS_FORWARDER}" ]]; then
        extra_args+=("--option=dns forwarder=${DNS_FORWARDER}")
    fi
    exec samba -F --debug-stdout "${extra_args[@]}"
else
    exec "${@}"
fi
