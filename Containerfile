# Stage 1: Base Ubuntu + Samba image
FROM docker.io/library/ubuntu:noble AS ubuntu-samba-base

ENV DEBIAN_FRONTEND=noninteractive

# renovate-ubuntu: suite=noble
RUN set -e \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        samba=2:4.19.5+dfsg-4ubuntu9.7 \
        samba-ad-dc=2:4.19.5+dfsg-4ubuntu9.7 \
        samba-ad-provision=2:4.19.5+dfsg-4ubuntu9.7 \
        winbind=2:4.19.5+dfsg-4ubuntu9.7 \
        krb5-user=1.20.1-6ubuntu2.10 \
        iputils-ping=3:20240117-1ubuntu0.1 \
        bzip2=1.0.8-5.1ubuntu0.1 \
        ldb-tools=2:2.8.0+samba4.19.5+dfsg-4ubuntu9.7 \
        chrony=4.5-1ubuntu4.2 \
        bind9-dnsutils=1:9.18.39-0ubuntu0.24.04.7 \
        acl=2.3.2-1build1.1 \
        attr=1:2.5.2-1ubuntu0.1 \
        smbclient=2:4.19.5+dfsg-4ubuntu9.7 \
        libnss-winbind=2:4.19.5+dfsg-4ubuntu9.7 \
        rsync=3.2.7-1ubuntu1.5 \
        plocate=1.1.19-2ubuntu2 \
        wsdd=2:0.7.1-5 \
        syslog-ng-core=4.3.1-2build5 \
        syslog-ng-mod-sql=4.3.1-2build5 \
        libdbd-pgsql=0.9.0-12 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*.deb \
    && rm -rf /tmp/* /var/tmp/* \
    && find /usr/share/doc -depth -type f ! -name copyright -delete \
    && find /usr/share/man -type f -delete

# Stage 2: Samba DC image
FROM ubuntu-samba-base

# Copy entrypoint and other required files
COPY samba-dc/ /

# Move default smb.conf to backup
RUN mv -v /etc/samba/smb.conf /etc/samba/smb.conf.distro

# Set environment variables
ENV SAMBA_LOGLEVEL="1 auth_audit:0 auth_json_audit:0" \
    SAMBA_SHARES_DIR=/srv/shares \
    SAMBA_HOMES_DIR=/srv/homes \
    SERVER_ROLE=dc \
    DNS1ADDRESS=127.0.0.1

# Create required directories and perform system setup
RUN set -e \
    && mkdir -m 0755 -p "${SAMBA_SHARES_DIR}" "${SAMBA_HOMES_DIR}" \
    && chown -c root:root "${SAMBA_SHARES_DIR}" "${SAMBA_HOMES_DIR}" \
    && [ "$(id -u nobody)" = "65534" ] || (echo "Unexpected nobody uid value" && exit 1) \
    && [ "$(id -g nobody)" = "65534" ] || (echo "Unexpected nobody gid value" && exit 1) \
    && [ "$(getent group users | cut -d: -f3)" = "100" ] || (echo "Unexpected users gid value" && exit 1) \
    && echo "OS $(grep -E '^(NAME|VERSION)=' /etc/os-release)" \
    && echo "Samba $(samba -V)" \
    && mkdir -vp /var/lib/samba/skel.d \
    && sed -r -i '/^HOME_MODE/ s/\b0750\b/0700/' /etc/login.defs

# Define volumes
VOLUME ["/srv/shares", "/srv/homes", "/var/lib/samba", "/etc/samba"]

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD []
