#
# Copyright (C) 2022 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

import ipaddress as ipm
import datetime
import re
import subprocess
import socket
import json
import dns.resolver
import sys
import agent
import os
import cluster.userdomains
import base64

# Map of array indexes returned by _make_record():
ACDN = 0
ACMEMBERS = 1
ACUAC = 2
ACID = 3
ACGROUPS = 4
ACTYPE = 5
ACDISPLAY = 6
ACMAIL = 7
ACPWDLASTSET = 8
ACPHONE = 9

class SambaException(Exception):
    pass

class IpNotPrivate(SambaException):
    pass

class IpNotAvailable(SambaException):
    pass

class IpBindError(SambaException):
    def __init__(self, ipaddr, message):
        self.ipaddr = ipaddr
        self.message = message
        super().__init__(self.message)

def ipaddress_check(ipaddress):
    """Run all checks together"""
    ipaddress_check_isprivate(ipaddress)
    ipaddress_check_isavailable(ipaddress)
    ipaddress_check_hasfreeports(ipaddress)
    return True

def ipaddress_check_isprivate(ipaddress):
    """The IP address must be in a private network class"""
    addr = ipm.ip_address(ipaddress)
    # See Python docs: https://docs.python.org/3.9/library/ipaddress.html#ip-addresses
    if not addr.is_private or addr.is_unspecified or addr.is_reserved or addr.is_loopback or addr.is_link_local:
        raise IpNotPrivate()

    return True

def ipaddress_check_isavailable(ipaddress):
    """The IP address is available and it is possible to bind a random port on it"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
                sk.bind((ipaddress, 0))
    except Exception as ex:
        raise IpNotAvailable(f"Address {ipaddress} bind failed: {ex}") from ex

    return True

def ipaddress_check_hasfreeports(ipaddress):
    """TCP ports for DC services are free on the given IP address"""
    for tcp_port in [53, 88, 636, 464, 445, 3268, 3269, 389, 135, 139]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
                sk.bind((ipaddress, tcp_port))
        except Exception as ex:
            raise IpBindError(ipaddress, f"Address {ipaddress}:{tcp_port} bind failed: {ex}") from ex

    return True

def ipaddress_list(skip_wg0=False, only_wg0=False):
    proc = subprocess.run(["ip", "-j", "-4", "address", "show"], text=True, capture_output=True)
    try:
        joutput = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []

    ipaddresses = []
    for iface in joutput:
        try:
            # skip wg0, as required by arguments
            if iface["ifname"] == "wg0" and skip_wg0:
                continue
            # skip non-wg0 interfaces, as required by arguments
            if iface["ifname"] != "wg0" and only_wg0:
                continue
            # skip interface without bcast address; wg0 is handled specially
            if iface["ifname"] != "wg0" and not 'BROADCAST' in iface["flags"]:
                continue
            # skip CNI interfaces
            if iface["ifname"].startswith('cni-'):
                continue
        except KeyError:
            pass

        ifip_list = [] # this list collects private ip addresses for iface
        for ainfo in iface['addr_info']:
            addr = ipm.ip_address(ainfo['local'])
            if addr.is_private and not (addr.is_unspecified or addr.is_reserved or addr.is_loopback or addr.is_link_local):
                altnames = ""
                if 'altnames' in iface:
                    altnames = f" ({', '.join(iface['altnames'])})"
                ifip_list.append({
                    "ipaddress": ainfo['local'],
                    "label": iface['ifname'] + altnames
                })
            else:
                # If the interface has at least a non-private
                # address, ignore it completely
                break
        else:
            # If the loop completes without breaking, add collected
            # ip addresses to the response list
            ipaddresses += ifip_list
    return ipaddresses

def validate_hostname(hostname, realm, nameservers=[]):
    rsv = dns.resolver.Resolver(configure=False)
    rsv.nameservers.extend(nameservers)
    try:
        resolve_ret = rsv.resolve(realm)
        print("DNS nameserver", resolve_ret.nameserver, file=sys.stderr)
        print("DNS authority", resolve_ret.response.authority, file=sys.stderr)
        print("Domain", resolve_ret.rrset.to_text(), file=sys.stderr)
    except dns.resolver.NoAnswer as ex:
        print("DNS error:", ex, file=sys.stderr)
        json.dump([{"field": "realm", "parameter": "realm", "value": realm, "error": "realm_dc_avail_check_failed"}], fp=sys.stdout)
        agent.set_status('validation-failed')
        sys.exit(6)
    except dns.exception.Timeout as ex:
        print("DNS error:", ex, file=sys.stderr)
        json.dump([{"field": "realm", "parameter": "realm", "value": realm, "error": "realm_dc_reachable_check_failed"}], fp=sys.stdout)
        agent.set_status('validation-failed')
        sys.exit(7)

    #
    # Check if the hostname is already registered in the DNS
    #
    try:
        hostname_resolve_ret = rsv.resolve(hostname + '.' + realm)
        print(agent.SD_ERR + f"DC hostname {hostname} is already in DNS!", hostname_resolve_ret.rrset.to_text(), file=sys.stderr)
        json.dump([{"field": "hostname", "parameter": "hostname", "value": hostname, "error": "hostname_check_failed"}], fp=sys.stdout)
        agent.set_status('validation-failed')
        sys.exit(11)
    except dns.resolver.NXDOMAIN:
        pass

def validate_ipaddress(ipaddress):
    try:
        ipaddress_check(ipaddress)
    except IpNotPrivate:
        agent.set_status('validation-failed')
        json.dump([{"field":"ipaddress","parameter":"ipaddress","value": ipaddress,"error":"ipaddress_private_check_failed"}], fp=sys.stdout)
        sys.exit(2)
    except IpNotAvailable:
        agent.set_status('validation-failed')
        json.dump([{"field":"ipaddress","parameter":"ipaddress","value": ipaddress,"error":"ipaddress_avail_check_failed"}], fp=sys.stdout)
        sys.exit(3)
    except IpBindError as ex:
        print(ex, file=sys.stderr)
        agent.set_status('validation-failed')
        json.dump([{"field":"ipaddress","parameter":"ipaddress","value": ex.ipaddr,"error":"ipaddress_bind_check_failed"}], fp=sys.stdout)
        sys.exit(4)

def push_vpn_routes():
    node_id = int(os.environ['NODE_ID'])
    rdb = agent.redis_connect()
    oip_address = ipm.ip_address(os.environ['IPADDRESS'])
    ocluster_network = ipm.ip_network(rdb.get('cluster/network'), strict=False)
    if not oip_address in ocluster_network:
        agent.tasks.run(
            agent_id='cluster',
            action='update-routes',
            data={
                'add': [{
                    "ip_address": os.environ['IPADDRESS'],
                    "node_id": node_id,
                }],
            },
            extra={"isNotificationHidden": True},
        )

def get_joinaddress():
    kdomain = os.getenv('DOMAIN', os.environ['REALM'].lower())

    rdb = agent.redis_connect()
    domains = cluster.userdomains.get_internal_domains(rdb)

    if not kdomain in domains:
        raise SambaException(f'Realm "{kdomain}" not found')

    for provider in domains[kdomain]['providers']:
        if provider['id'] != os.environ["MODULE_ID"]:
            break # DC found. Stop searching.
    else:
        # DC not found: error!
        raise SambaException(f'DC for "{kdomain}" not found')

    return provider['host']

def configure_samba_audit(sharename, enable_audit=True, log_failed_events=False):
    podman_exec = ["podman", "exec", "samba-dc"]
    setparm_cmd = podman_exec + ["net", "conf", "setparm", sharename]
    delparm_cmd = podman_exec + ["net", "conf", "delparm", sharename]
    enabled_success_operations = os.getenv("SAMBA_AUDIT_SUCCESS", "create_file unlinkat renameat mkdirat fsetxattr")
    enabled_failure_operations = os.getenv("SAMBA_AUDIT_FAILURE", "create_file unlinkat renameat mkdirat fsetxattr")
    set_audit_cmd = delparm_cmd + ["full_audit:success"]
    set_logfailed_cmd = delparm_cmd + ["full_audit:failure"]
    if enable_audit:
        set_audit_cmd = setparm_cmd + ["full_audit:success", enabled_success_operations]
        if log_failed_events:
            set_logfailed_cmd = setparm_cmd + ["full_audit:failure", enabled_failure_operations]
    agent.run_helper(*set_audit_cmd, stderr=subprocess.DEVNULL)
    agent.run_helper(*set_logfailed_cmd, stderr=subprocess.DEVNULL)

def configure_recycle(sharename, enable_recycle=True, recycle_retention=0, recycle_versions=False):
    if enable_recycle:
        agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "setparm", sharename, "recycle:repository", os.getenv("RECYCLE_REPOSITORY", ".recycle") + "/%U")
        if recycle_versions:
            agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "delparm", sharename, "recycle:versions")
        else:
            agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "setparm", sharename, "recycle:versions", "no")
        agent.run_helper("podman", "exec", "samba-dc", "recycle", "set_retention", sharename, str(recycle_retention))
        agent.run_helper("podman", "exec", "samba-dc", "recycle", "init_repository", sharename)
    else:
        agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "delparm", sharename, "recycle:repository")
        agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "delparm", sharename, "recycle:versions")
        agent.run_helper("podman", "exec", "samba-dc", "recycle", "del_retention", sharename)

def configure_browseable(sharename, browseable=True):
    if browseable:
        agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "delparm", sharename, "browseable")
    else:
        agent.run_helper("podman", "exec", "samba-dc", "net", "conf", "setparm", sharename, "browseable", "no")

def get_user_account_control(user):
    sambatool_cmd = ['podman', 'exec', '-i', 'samba-dc', 'samba-tool']
    getdn_cmd = sambatool_cmd + ['user', 'show', user, '--attributes=userAccountControl']
    proc = subprocess.run(getdn_cmd, check=True, capture_output=True, text=True)
    output = proc.stdout.strip()
    # Extract the DN and userAccountControl value
    dn_str = None
    user_account_control = None
    for line in output.splitlines():
        if line.startswith("dn:"):
            dn_str = line
        elif line.startswith("userAccountControl:"):
            user_account_control = int(line.split(":", 1)[1].strip())
    if not dn_str or user_account_control is None:
        raise Exception("DN or userAccountControl not found")
    return dn_str, user_account_control

def set_user_account_control(dn_str, user_account_control, no_password_expiration):
    UF_DONT_EXPIRE_PASSWORD = 0x10000
    if no_password_expiration == True and not ( user_account_control & UF_DONT_EXPIRE_PASSWORD ):
        user_account_control |= UF_DONT_EXPIRE_PASSWORD # set the flag
    elif no_password_expiration == False and ( user_account_control & ~UF_DONT_EXPIRE_PASSWORD ):
        user_account_control &= ~UF_DONT_EXPIRE_PASSWORD # clear the flag
    else:
        user_account_control = None  # No change needed
    if user_account_control is not None:
        ldbmodify_cmd = ['podman', 'exec', '-i', 'samba-dc', 'ldbmodify', '-H', '/var/lib/samba/private/sam.ldb']
        ldbmodify_input = f'{dn_str}\nchangetype: modify\nreplace: userAccountControl\nuserAccountControl: {user_account_control}\n'
        subprocess.run(ldbmodify_cmd, input=ldbmodify_input, stdout=sys.stderr, check=True, text=True)

def set_or_clear_ldap_attribute(user, attribute, value, check=True):
    sambatool_cmd = ['podman', 'exec', '-i', 'samba-dc', 'samba-tool']
    getdn_cmd = sambatool_cmd + ['user', 'show', user, '--attributes=dn']
    proc = subprocess.run(getdn_cmd, check=True, capture_output=True, text=True)
    dn = proc.stdout.strip()
    if value:
        ldbmodify_cmd = ['podman', 'exec', '-i', 'samba-dc', 'ldbmodify', '-i', '-H', '/var/lib/samba/private/sam.ldb']
        ldbmodify_input = f'{dn}\nchangetype: modify\nreplace: {attribute}\n{attribute}: {value}\n'
    else:
        ldbmodify_cmd = ['podman', 'exec', '-i', 'samba-dc', 'ldbmodify', '-H', '/var/lib/samba/private/sam.ldb']
        ldbmodify_input = f'{dn}\nchangetype: modify\ndelete: {attribute}\n'
    subprocess.run(ldbmodify_cmd, input=ldbmodify_input, stdout=sys.stderr, check=check, text=True)

def _filetime_to_datetime(filetime):
    """Convert a Windows FILETIME (100-nanosecond intervals since 1601-01-01 UTC) to a datetime."""
    if filetime is None or filetime <= 0:
        return None
    return datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc) + \
        datetime.timedelta(microseconds=int(filetime) // 10)

def get_password_settings():
    result = subprocess.run(
        ['podman', 'exec', 'samba-dc', 'samba-tool', 'domain', 'passwordsettings', 'show'],
        check=True,
        capture_output=True,
        text=True,
    )

    password_settings = {
        'expiration': {
            'max_age': int(re.search(r'Maximum password age \(days\): (\d.*)\n', result.stdout).group(1)),
            'min_age': int(re.search(r'Minimum password age \(days\): (\d.*)\n', result.stdout).group(1)),
        },
        'strength': {
            'history_length': int(re.search(r'Password history length: (\d.*)\n', result.stdout).group(1)),
            'password_min_length': int(re.search(r'Minimum password length: (\d.*)\n', result.stdout).group(1)),
            'complexity_check': re.search(r'Password complexity: (.*)\n', result.stdout).group(1) == 'on',
        },
    }

    password_settings['expiration']['enforced'] = password_settings['expiration']['max_age'] > 0 or \
                                                  password_settings['expiration']['min_age'] > 0
    password_settings['strength']['enforced'] = password_settings['strength']['history_length'] > 0 or \
                                                password_settings['strength']['password_min_length'] > 0 or \
                                                password_settings['strength']['complexity_check']

    if not password_settings['expiration']['enforced']:
        password_settings['expiration']['max_age'] = 180
        password_settings['expiration']['min_age'] = 0

    if not password_settings['strength']['enforced']:
        password_settings['strength']['history_length'] = 24
        password_settings['strength']['password_min_length'] = 8
        password_settings['strength']['complexity_check'] = True

    return password_settings

def get_user_password_expiration(user):
    accounts = _get_accounts()
    if user not in accounts:
        raise KeyError(user)

    rec = accounts[user]
    if rec[ACTYPE] != 'U':
        raise KeyError(user)

    password_settings = get_password_settings()
    must_change = rec[ACPWDLASTSET] is None or rec[ACPWDLASTSET] <= 0
    no_password_expiration = bool(rec[ACUAC] & 0x10000)
    expiration = None
    expired = False

    if not must_change and not no_password_expiration and password_settings['expiration']['enforced']:
        pwd_last_set = _filetime_to_datetime(rec[ACPWDLASTSET])
        if pwd_last_set is not None:
            expiry_date = pwd_last_set + datetime.timedelta(days=password_settings['expiration']['max_age'])
            expired = datetime.datetime.now(datetime.timezone.utc) > expiry_date
            expiration = expiry_date.isoformat().replace('+00:00', 'Z')

    return {
        'expired': expired,
        'expiration': expiration,
        'must_change': must_change,
    }

def get_ad_ldap_suffix() -> str:
    """Returns the LDAP base DN suffix derived from the DOMAIN environment variable.
    For example, if DOMAIN is 'ad.example.com', returns 'DC=ad,DC=example,DC=com'.
    """
    parts = os.getenv('DOMAIN', os.environ['REALM'].lower()).split(".")
    return "DC=" + ",DC=".join(parts)

def export_users() -> list:
    """
    Exports all non-system user accounts from Active Directory.
    Returns:
        list: A list of dictionaries, each containing user information including:
            - user: The username.
            - display_name: The user's display name.
            - locked: Whether the account is locked.
            - must_change_password: Whether the user must change their password.
            - no_password_expiration: Whether the password does not expire.
            - mail (optional): The user's email address, if available.
            - phone_extension (optional): The user's phone extension, if available.
            - groups: A sorted list of group names the user belongs to.
    Notes:
        System accounts (krbtgt, administrator, guest, ldapservice) and
        machine accounts (ending with '$') are excluded.
    """
    adb = _get_accounts()
    records = []
    for rk, rec in adb.items():
        if rec[ACTYPE] != 'U':
            continue
        if rec[ACID].lower() != rk:
            continue
        if rec[ACID].lower() in ['krbtgt', 'guest', 'ldapservice', 'administrator']:
            continue
        if rec[ACID].endswith('$'):
            continue
        out = {
            "user": rec[ACID],
            "locked": bool(rec[ACUAC] & 0x2), # ACCOUNTDISABLED
            "must_change_password": rec[ACPWDLASTSET] is None or rec[ACPWDLASTSET] <= 0,
            "no_password_expiration": bool(rec[ACUAC] & 0x10000), # DONT_EXPIRE_PASSWD
        }
        if rec[ACMAIL]:
            out["mail"] = rec[ACMAIL]
        if rec[ACPHONE]:
            out["phone_extension"] = rec[ACPHONE]
        if rec[ACDISPLAY]:
            out["display_name"] = rec[ACDISPLAY]
        groups = []
        # rec[ACGROUPS] contains group DNs (Distinguished Names).
        # The adb dictionary is keyed by both group DNs and canonical names,
        # so we can look up the group name (ACID) using the DN as the key.
        for g in rec[ACGROUPS]:
            if g in adb:
                groups.append(adb[g][ACID])
        out["groups"] = sorted(groups)
        records.append(out)
    return records

def import_users(records: list, skip_existing: bool, progfunc: callable) -> bool:
    """
    Imports user accounts and group memberships into Active Directory.
    Args:
        records: List of user dictionaries with fields:
            - user: Username (required)
            - password: User password (optional)
            - display_name: Display name (optional)
            - locked: Account lock status (optional)
            - groups: List of group names (optional)
            - mail: Email address (optional)
            - phone_extension: Phone extension (optional)
            - must_change_password: Require password change at next login (optional)
            - no_password_expiration: Disable password expiration (optional)
        skip_existing: If True, skip existing users entirely; if False, update them.
        progfunc: Callback function for progress updates, takes int 0-100.
    Returns:
        True if all operations succeeded, False if any errors occurred.
    Note:
        Non-existing groups are created automatically during import.
    """
    import_errors = 0
    LDAPSUFFIX = get_ad_ldap_suffix()
    merge_existing = not skip_existing
    adb = _get_accounts()
    cur_progress = 5.0 # for _get_accounts()
    progfunc(int(cur_progress))

    prog_step = 75.0/(len(records) or 1) # step_recalc

    all_users = set() # imported user names (AD may have more..)
    mod_groups = CaseInsensitiveDict() # new group membership mapping

    # Accumulate LDIF changes
    ldif_changes = CaseInsensitiveDict() # DB of LDIF changes, key is DN
    def ldif_prepare(user, att, val, op='replace'):
        dn = adb[user][ACDN]
        if not dn in ldif_changes:
            ldif_changes[dn] = [(att, val, op)]
        else:
            ldif_changes[dn].append((att, val, op))

    for rec in records:
        user = rec['user']
        all_users.add(user)
        pwd = rec.get('password', '')
        display_name = rec.get('display_name')
        must_change = rec.get('must_change_password') is True
        mail_address = rec.get('mail')
        phone_extension = rec.get('phone_extension')

        # Accumulate changes for userAccountControl attribute (UAC)
        uac_set_flags = 0
        uac_clear_flags = 0
        if rec.get('locked') is True:
            uac_set_flags |= 0x2 # ACCOUNTDISABLED
        elif rec.get('locked') is False:
            uac_clear_flags |= 0x2 # ACCOUNTDISABLED
        if rec.get('no_password_expiration') is True:
            uac_set_flags |= 0x10000 # DONT_EXPIRE_PASSWD
        elif rec.get('no_password_expiration') is False:
            uac_clear_flags |= 0x10000 # DONT_EXPIRE_PASSWD

        # 1. Handle user creation and password reset with samba-tool
        if user in adb:
            udn = adb[user][ACDN]
            if pwd and merge_existing:
                cmd_success = _reset_password(user, pwd)
                if not cmd_success:
                    import_errors += 1
            elif skip_existing:
                cur_progress += 2*prog_step # progress score of skipped commands
                progfunc(int(cur_progress))
                continue # next record ; all further processing (group sync, LDIF changes) is skipped for this user
        else:
            cmd_success = _create_user(user, pwd)
            if not cmd_success:
                import_errors += 1
                continue # Skip further processing for this user
            udn = f'CN={user},CN=Users,' + LDAPSUFFIX # Assuming default DN
            adb[user] = (udn, [], 512, user, [], 'U', None, None, None, None) # (512 = NORMAL_ACCOUNT)
            if not display_name:
                display_name = user.title() # Initialize displayName with the Title Case of username

        # 2a. Add user to its new groups. Non-existing group is created on
        #     the fly.
        for gna in rec.get('groups', []):
            if gna not in adb:
                # gna must be created, initialize it:
                if _create_group(gna):
                    adb[gna] = (f'CN={gna},CN=Users,' + LDAPSUFFIX, [], 0, gna, [], 'G', None, None, None, None)
                else:
                    import_errors += 1
            if gna in mod_groups:
                mod_groups[gna].append(udn)
            else:
                mod_groups[gna] = [udn]
        # 2b. Remove user from groups
        groups = [g.lower() for g in rec.get('groups', [])]
        for gna in adb:
            if adb[gna][ACTYPE] == 'G' and \
                adb[gna][ACDN].lower() != gna.lower() and \
                not gna.lower() in groups and \
                udn in adb[gna][ACMEMBERS]:
                # Found a member that must be removed.
                if not gna in mod_groups:
                    # Initialize with current member list, without udn.
                    mod_groups[gna] = adb[gna][ACMEMBERS].copy()
                    mod_groups[gna].remove(udn)
                else:
                    # List already initialized. Just remove udn from it.
                    if udn in mod_groups[gna]:
                        mod_groups[gna].remove(udn)

        # 3. Prepare user LDIF changes
        if display_name == "" and adb[user][ACDISPLAY] is not None:
            ldif_prepare(user, 'displayName', None, "delete")
        elif display_name:
            ldif_prepare(user, 'displayName', display_name)
        if mail_address == "" and adb[user][ACMAIL] is not None:
            ldif_prepare(user, 'mail', None, "delete")
        elif mail_address:
            ldif_prepare(user, 'mail', mail_address)
        if phone_extension == "" and adb[user][ACPHONE] is not None:
            ldif_prepare(user, 'telephoneNumber', None, "delete")
        elif phone_extension:
            ldif_prepare(user, 'telephoneNumber', phone_extension)
        if must_change:
            ldif_prepare(user, 'pwdLastSet', 0)
        uac = adb[user][ACUAC]
        ldif_prepare(user, 'userAccountControl', (uac | uac_set_flags) & ~uac_clear_flags)

        # Update progress
        cur_progress += prog_step
        progfunc(int(cur_progress))

    # 4. Prepare group LDIF changes
    all_users_dn = { adb[u][ACDN] for u in all_users }
    for gna in mod_groups:
        keep_members = set(adb[gna][ACMEMBERS]) - all_users_dn
        new_members = set(mod_groups[gna])
        member_list = list(new_members | keep_members)
        if member_list:
            ldif_prepare(gna, 'member', member_list)
        else:
            ldif_prepare(gna, 'member', None, 'delete')

    # 5. Apply LDIF changes:
    prog_step = 20.0 / (len(ldif_changes) or 1) # step recalc
    # Since ldbmodify command does not provide a "continue on error"
    # behavior we split LDIF entries into individual ldbmodify runs: one
    # entry, one run. Entries are delimited with NUL chars in both input
    # and output.
    def read_until_nul(binf):
        while True:
            b = binf.read(128)
            if not b:
                break # EOF
            print(b.decode('utf-8', errors="replace"), file=sys.stderr)
            if b'\0' in b:
                break # End of record
    ldbmodifycmd = r"""while read -r -d $'\0' entry ; do ldbmodify -v -H /var/lib/samba/private/sam.ldb <<<"$entry" || { echo -e "Failed LDIF record:\n$entry\n " ; code=1 ; } ; printf "\0" ; done ; exit $code"""
    with subprocess.Popen(
        ['podman', 'exec', '-i', 'samba-dc', 'bash', '-c', ldbmodifycmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=False, # binary stream required for b'\0' terminators
        bufsize=0,
    ) as proc:
        for dn in ldif_changes.keys():
            oentry = ''
            oentry += f'dn: {dn}\n'
            oentry += f'changetype: modify\n'
            for cht in ldif_changes[dn]:
                if cht[2] == 'replace' or cht[2] == 'add':
                    oentry += f'{cht[2]}: {cht[0]}\n'
                    if isinstance(cht[1], list):
                        for v in cht[1]:
                            oentry += f'{cht[0]}: {v}\n'
                    else:
                        oentry += f'{cht[0]}: {cht[1]}\n'
                elif cht[2] == 'delete':
                    oentry += f'delete: {cht[0]}\n'
                oentry += '-\n'
            proc.stdin.write(oentry.encode('utf-8', errors='replace') + b'\0')
            read_until_nul(proc.stdout)
            cur_progress += prog_step
            progfunc(int(cur_progress))
    progfunc(100) # Complete progress scores
    if proc.returncode:
        import_errors += 1
    return import_errors == 0

def _create_group(group):
    addgroup_cmd = ['podman', 'exec', '-i', 'samba-dc', 'samba-tool', 'group', 'create', group]
    proc = subprocess.run(addgroup_cmd, stdout=sys.stderr, text=True)
    return proc.returncode == 0

def _reset_password(user, password) -> bool:
    adduser_cmd = ['podman', 'exec', '-i', 'samba-dc', 'samba-tool', 'user', 'setpassword', user]
    inputdata = password + "\n" + password + "\n"
    proc = subprocess.run(adduser_cmd, input=inputdata, stdout=sys.stderr, text=True)
    return proc.returncode == 0

def _create_user(user, password) -> bool:
    adduser_cmd = ['podman', 'exec', '-i', 'samba-dc', 'samba-tool', 'user', 'create', user]
    if not password:
        adduser_cmd += ['--random-password']
        inputdata = None
    else:
        inputdata = password + "\n" + password + "\n"
    proc = subprocess.run(adduser_cmd, input=inputdata, stdout=sys.stderr, text=True)
    return proc.returncode == 0

class CaseInsensitiveDict(dict):
    """Dict subclass with case-insensitive key lookup.

    Limitations:
    - Only string keys are supported; non-string keys will fail on .lower().
    - Methods other than __setitem__, __getitem__, and __contains__
      remain case-sensitive (get, pop, setdefault, update, etc.).
    - Iteration yields lower-cased keys since stored keys are normalized.
    - Keys that differ only by case are merged silently.
    """
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

def _get_accounts() -> dict:
    """Returns account information indexed by DN and sAMAccountName. Each
    value is a tuple of 10 elements.
    """
    def v(line):
        a, w = line.split(": ", 1)
        if a.endswith(":"):
            try:
                return base64.b64decode(w).decode("utf-8", errors="ignore")
            except Exception:
                pass
        return w

    def _make_record():
        record = list((None,)*10)
        record[ACGROUPS] = []
        record[ACMEMBERS] = []
        record[ACTYPE] = 'U'
        record[ACUAC] = 0
        return record

    def _ldif_unfold(ldif_iter):
        buf = None     # accumulated logical line (without trailing newline)
        for raw in ldif_iter:
            # raw always ends with '\n', except possibly at EOF
            if raw == "\n":
                # Blank line: flush current logical line, then yield blank line
                if buf is not None:
                    yield buf + "\n"
                    buf = None
                yield "\n"
                continue

            if raw.startswith(" "):  # continuation line
                if buf is None:
                    # malformed LDIF: treat as new line without leading space
                    buf = raw.lstrip().rstrip("\n")
                else:
                    buf += raw[1:].rstrip("\n")
            else:
                # New logical line
                if buf is not None:
                    yield buf + "\n"
                buf = raw.rstrip("\n")

        # EOF: flush last buffered logical line (without adding extra blank line)
        if buf is not None:
            yield buf + "\n"

    accounts = CaseInsensitiveDict()
    with subprocess.Popen([
            'podman', 'exec', '-i', 'samba-dc', 'ldbsearch',
            '-H', '/var/lib/samba/private/sam.ldb',
            '-b', get_ad_ldap_suffix(),
            '--paged',
            '(sAMAccountName=*)',
            'sAMAccountName',
            'member',
            'userAccountControl',
            'memberOf',
            'objectClass',
            'pwdLastSet',
            'mail',
            'telephoneNumber',
            'displayName',
        ], text=True, stdout=subprocess.PIPE) as proc_ldbsearch:
            record = _make_record()
            curdn = None
            curna = None
            for ldifline in _ldif_unfold(proc_ldbsearch.stdout):
                ldifline = ldifline.rstrip("\n")
                if not ldifline:
                    # End-Of-Record
                    if curna and curdn:
                        accounts[curna] = record
                        accounts[curdn] = record
                    record = _make_record()
                    curdn = None
                    curna = None
                elif ldifline.startswith("dn:"):
                    curdn = v(ldifline)
                    record[ACDN] = curdn
                elif ldifline.startswith("sAMAccountName:"):
                    curna = v(ldifline)
                    record[ACID] = curna
                elif ldifline.startswith("member:"):
                    record[ACMEMBERS].append(v(ldifline))
                elif ldifline.startswith("memberOf:"):
                    record[ACGROUPS].append(v(ldifline))
                elif ldifline == "objectClass: group":
                    record[ACTYPE] = 'G'
                elif ldifline.startswith("userAccountControl:"):
                    try:
                        record[ACUAC] = int(v(ldifline))
                    except ValueError:
                        # Force to disabled state:
                        record[ACUAC] = 2 # ACCOUNTDISABLE
                elif ldifline.startswith("displayName:"):
                    record[ACDISPLAY] = v(ldifline)
                elif ldifline.startswith("mail:"):
                    record[ACMAIL] = v(ldifline)
                elif ldifline.startswith("telephoneNumber:"):
                    record[ACPHONE] = v(ldifline)
                elif ldifline.startswith("pwdLastSet:"):
                    try:
                        record[ACPWDLASTSET] = int(v(ldifline))
                    except ValueError:
                        # Ignore invalid pwdLastSet values; leave as None
                        pass
    if proc_ldbsearch.returncode != 0:
        print("[ERROR] ldbsearch failed!", file=sys.stderr)
        return CaseInsensitiveDict()
    return accounts
