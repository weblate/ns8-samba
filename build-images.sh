#!/bin/bash

set -e
images=()

repobase="${REPOBASE:-ghcr.io/nethserver}"
reponame="ubuntu-samba"
ubuntu_tag=23.04

container="ubuntu-working-container"
# Prepare a local Ubuntu-based samba image
if ! buildah inspect --type container "${container}" &>/dev/null; then
    container=$(buildah from --name "${container}" docker.io/library/ubuntu:${ubuntu_tag})
    buildah run "${container}" -- bash <<'EOF'
set -e
apt-get update
apt-get -y install samba winbind krb5-user iputils-ping bzip2 ldb-tools chrony dnsutils acl smbclient libnss-winbind rsync
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
    --env=SAMBA_SHARES_DIR=/srv/shares \
    --volume=/srv/shares \
    --volume=/var/lib/samba \
    --volume=/etc/samba \
    "${container}"
buildah run "${container}" -- bash <<'EOF'
groupadd --gid=1001 administrators # alias of Administrators group
mkdir -p "${SAMBA_SHARES_DIR:?}"
chown -c root:administrators "${SAMBA_SHARES_DIR}"
chmod -c 0770 "${SAMBA_SHARES_DIR}"
# Verify our assumptions on the uid/gid numeric value of some well-known entries
[[ "$(id -u nobody)" == 65534 ]] || : ${nobody_uid_error:?Unexpected nobody uid value}
[[ "$(id -g nobody)" == 65534 ]] || : ${nobody_gid_error:?Unexpected nobody gid value}
[[ "$(getent group users | cut -d: -f3)" == 100 ]] || : ${users_gid_error:?Unexpected users gid value}
echo "OS" $(grep -E '^(NAME|VERSION)=' /etc/os-release)
echo "Samba" $(samba -V)
EOF
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
    --label 'org.nethserver.authorizations=node:fwadm ldapproxy@node:accountprovider cluster:accountprovider' \
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
