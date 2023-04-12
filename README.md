# samba

The Samba module allows to install one or more AD domains in a NS8
cluster. An AD domain (or realm, in Kerberos terms), can have one or more
domain controllers (DCs). Provisioning a new domain and joining an
additional domain controller to an existing domain are both implemented by
the same action: `provision-domain`.

A Samba DC requires a dedicated IP address. Two DCs cannot share the same
IP.

Do not assign the IP address of a untrusted network! The IP address
assigned to Samba DC exposes internal services that are not designed to be
exposed publicly. The IP address can be added to the cluster VPN routes,
so DCs can see each other and perform replication.

The LDAP service of Samba DCs does not allow clear-text LDAP binds: enable
TLS or use Kerberos/GSSAPI authentication in external applications.
Applications that run as cluster modules must connect to the LDAP service
of Samba DCs through the Ldapproxy instance running on the local node; read
the core documentation for more information about Ldapproxy.

## Installation

A Samba module instance is also an account provider. It must be installed
with the specific `add-internal-provider` action:

    api-cli run add-internal-provider --data '{"image":"ghcr.io/nethserver/samba:latest","node":1}'

## Provision

Provision a new domain:

    api-cli run configure-module --agent module/samba1 --data - <<EOF
    {
        "provision":"new-domain",
        "adminuser":"administrator",
        "adminpass":"Nethesis,1234",
        "realm":"ad.$(hostname -d)",
        "nbdomain":"DP",
        "hostname":"dc1",
        "ipaddress":"10.133.0.2"
    }
    EOF

Further Samba instances for the same `realm` can be **joined** to the existing domain.
The command is similar.

    api-cli run configure-module --agent module/samba2 --data - <<EOF
    {
        "provision":"join-domain",
        "adminuser":"administrator",
        "adminpass":"Nethesis,1234",
        "realm":"ad.$(hostname -d)",
        "hostname":"dc2",
        "ipaddress":"10.124.0.2"
    }
    EOF

## IP routing for the AD domain

In multiple DCs domains, DCs must connect each other to join the domain
and for data replication. If a DC cannot contact other DCs the provision
procedure fails.

For this reason the DC IP is reachable from other nodes of the cluster
through the cluster VPN.

## Create user

To create a new user, just execute:
```
podman exec -ti samba1 samba-tool user create goofy Nethesis,1234 --given-name=Goofy --surname=Goof --mail=goofy@mail.org
```

## Migration notes

Migration is implemented in the `import-module` action.

- The NS7 DC role is transferred to NS8 by copying `/var/lib/samba` dir
  contents. The NS7 file-server role can be transferred to NS8 too.
- If file-server role is migrated, the host name is retained as a NetBIOS
  alias and a DNS CNAME record, pointing to the DC host name.
- The migration procedure synchronizes the existing Posix ACLs of shared
  folders. A special backward-compatible configuration is applied to
  shares created by the migration procedure. The `samba-reset-acls`
  command clears that special configuration, too.
- Home directories are migrated like shared folders. If a shareed folder
  has the same name of a user, the home directory is not migrated.
- Guest access does not work in NS8, because it is [not implemented by the
  Samba DC
  role](https://wiki.samba.org/index.php/FAQ#How_Do_I_Enable_Guest_Access_to_a_Share_on_a_Samba_AD_DC.3F)
- `user.SAMBA_PAI` attribute is not copied to NS8 shares. It contains
  the ACL *protected/don't inherit* flag. See [map acl
  inherit](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html).
