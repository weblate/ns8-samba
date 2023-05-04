#!/bin/bash

#
# Copyright (C) 2023 Nethesis S.r.l.
# SPDX-License-Identifier: GPL-3.0-or-later
#

#
# Hint: access the test logs on HTTP port 8000 with this command:
#
#     python -mhttp.server -d tests/outputs/ 8000 &
#

set -e

SSH_KEYFILE=${SSH_KEYFILE:-$HOME/.ssh/id_rsa}

LEADER_NODE="${1:?missing LEADER_NODE argument}"
IMAGE_URL="${2:?missing IMAGE_URL argument}"
shift 2

rfimage="ghcr.io/marketsquare/robotframework-browser/rfbrowser-stable:16.0.5"
site_packages=$(podman run --network=none --rm "${rfimage}" python3 -msite --user-site)
ssh_pwuser_key=/home/pwuser/tests/.ssh_privkey
test_name="$(basename $PWD)"

trap 'set +e ; rm -f tests/.ssh_privkey ; podman cp rfbrowser:/home/pwuser/outputs tests/ ; podman rm rfbrowser || :' EXIT
cp -p "${SSH_KEYFILE}" tests/.ssh_privkey

tar -c tests/ | podman run \
    --init \
    --interactive \
    --name=rfbrowser \
    --network=host \
    --volume=site-packages:${site_packages:?}:z \
    "${rfimage}" \
    bash -c "
        set -e
        cd ~
        mkdir -p outputs
        tar -x -f -
        pip3 install -q -r tests/pythonreq.txt
        exec robot -v NODE_ADDR:${LEADER_NODE} -v IMAGE_URL:${IMAGE_URL} -v SSH_KEYFILE:${ssh_pwuser_key} \
            --name \"${test_name}\" \
            --skiponfailure unstable \
            -d outputs/ \
            \"\${@}\" \
            tests/
        " -- "${@}"
