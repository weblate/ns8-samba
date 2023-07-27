# samba

The Samba module allows to install one or more AD domains in a NS8
cluster. An AD domain (or realm, in Kerberos terms), can have one or more
domain controllers (DCs). Provisioning a new domain and joining an
additional domain controller to an existing domain are both implemented by
the same action: `configure-module`.

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

    api-cli run add-internal-provider --data '{"image":"samba","node":1}'

## Provision

For example, to provision a new domain:

    api-cli run module/samba1/configure-module --data - <<EOF
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

    api-cli run module/samba2/configure-module --data - <<EOF
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

For this reason, if the IP of some domain controller is not in the
routable networks of other nodes, then it is automatically configured to
be routed through the cluster VPN. This typically happens if domain
controllers reside in different networks.

Check the IP addresses of domain controllers are routed through the VPN
with the following commands:

    wg
    ip route

The following command applies the necessary changes to the system routing
table and to the Wireguard runtime configuration. It is automatically
executed at system startup and when the VPN configuration changes, so
manual execution should not be needed:

    apply-vpn-routes

See also the [Core VPN documentation](https://nethserver.github.io/ns8-core/core/vpn/#vpn).

## Create a new user account

Create a new user and assign it to the `developers` group

  api-cli run module/samba1/add-user --data - <<EOF
  {
      "user": "alice",
      "display_name": "Alice Jordan",
      "password": "secret",
      "locked": false,
      "groups": [
          "developers"
      ]
  }
  EOF

## File server

If Samba binds to the **internal VPN interface** (see `ipaddress`
attribute in the Provision section) it is **not reachable** by clients in
other networks.

On the contrary, a Samba instance can be used as a **file server** from
Windows-compatible clients and they can access shared folders and home
directories with domain credentials (guest access does not work at all).

- Whenever a user session is established the user's home directory is
  created in the `homes` volume.

- To create and manage shared folders, use the file server API. Shared
  folders are stored in the `shares` volume. If a shared folder has the
  same name of a domain user, the home directory of that user is no longer
  accessible.
  + `list-shares`
  + `add-share`, `alter-share`, `remove-share`
  + `reset-share-acls`

## Restore from backup

The module backup contains shared folders, home dirs and DC state.

For a single DC domain, run the restore on a system with the original DC
IP address. If this is not the case, the restore procedure configures the
restored DC with the node VPN IP address. Then use `set-ipaddress` action
to change the DC IP address. Network clients must be reconfigured to find
the AD DNS server! For instance:

    api-cli run module/samba1/set-ipaddress --data '{"ipaddress": "10.15.21.100"}'

In a domain with multiple domain controllers, DC state is replicated. In
case of a node failure it is not necessary to restore from backup unless
the failing node is also a file server. In this case the restore procedure
only extracts the contents of home directories and shared folders from the
backup set. When the procedure completes, go to the ``Domain and users``
page and resume the configuration of the DC: it must be joined to the
domain as a new DC.

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
- Home directories are migrated like shared folders. Shared folders have
  higher priority over home dirs: if a shared folder has the same name of
  a domain user, the home directory cannot be accessed.
- Guest access does not work in NS8, because it is [not implemented by the
  Samba DC
  role](https://wiki.samba.org/index.php/FAQ#How_Do_I_Enable_Guest_Access_to_a_Share_on_a_Samba_AD_DC.3F)
- `user.SAMBA_PAI` attribute is not copied to NS8 shares. It contains
  the ACL *protected/don't inherit* flag. See [map acl
  inherit](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html).
