#!/bin/bash

set -e
images=()

repobase="${REPOBASE:-ghcr.io/nethserver}"
reponame="ubuntu-samba"
ubuntu_tag="devel"

container="ubuntu-working-container"
# Prepare a local Ubuntu-based samba image
if ! buildah inspect --type container "${container}" &>/dev/null; then
    container=$(buildah from --name "${container}" docker.io/library/ubuntu:${ubuntu_tag})
    buildah run "${container}" -- bash <<EOF
set -e
apt-get update
apt-get -y install samba winbind krb5-user iputils-ping bzip2 ldb-tools chrony dnsutils
apt-get clean
find /var/lib/apt/lists/ -type f -delete
EOF
    buildah commit "${container}" "${repobase}/${reponame}"
fi

#
# Add our entrypoint script to build samba-dc
#
container=$(buildah from "${repobase}/${reponame}")
reponame="samba-dc"
buildah run "${container}" -- mv -v /etc/samba/smb.conf /etc/samba/smb.conf.${ubuntu_tag}
buildah add "${container}" samba-dc/ /
buildah config --cmd='' \
    --entrypoint='["/entrypoint.sh"]' \
    --env=SAMBA_LOGLEVEL="1 auth_audit:3" \
    --volume=/var/lib/samba \
    --volume=/etc/samba \
    "${container}"
buildah commit "${container}" "${repobase}/${reponame}"
images+=("${repobase}/${reponame}")

#
# Imageroot samba
#
container=$(buildah from scratch)
reponame="samba"
buildah add "${container}" imageroot /imageroot
buildah add "${container}" ui /ui
buildah config \
    --label "org.nethserver.images=ghcr.io/nethserver/samba-dc:${IMAGETAG:-latest}" \
    --label 'org.nethserver.authorizations=ldapproxy@node:accountprovider cluster:accountprovider' \
    --label 'org.nethserver.flags=core_module account_provider' \
    --entrypoint=/ "${container}"
buildah commit "${container}" "${repobase}/${reponame}"
images+=("${repobase}/${reponame}")

#
#
#

if [[ -n "${CI}" ]]; then
    # Set output value for Github Actions
    printf "::set-output name=images::%s\n" "${images[*]}"
else
    printf "Publish the images with:\n\n"
    for image in "${images[@]}"; do printf "  buildah push %s docker://%s:latest\n" "${image}" "${image}" ; done
    printf "\n"
fi
