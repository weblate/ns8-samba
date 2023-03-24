# samba-dc

## Volumes

- `config`
- `data`
- `shares`

## Environment variables

- SAMBA_SHARES_DIR, default "/srv/shares" path to the volume containing
  user home dirs and shared folders. Do not change it! In any case do not
  put under /var/lib/samba to avoid conflicts with the backup procedure. 

## Commands

- `expand-config`
- `new-domain`
- `join-domain`
- `samba-add-share`
- `samba-delete-share`
- `samba-reset-acls` Reset the ACLs of a shared directory and its
  contents. If the share was created by `rsyncd-import-shares`, reset also
  the Samba share configuration to NS8 defaults
- `rsyncd-import-shares` Starts a special Rsync server that can resolve
  user and group names and supports Posix ACLs. Configuration parameters
  are passed with RSYNCD_* environment variables, as defined in the
  [core/rsync](https://github.com/NethServer/ns8-core/blob/main/core/rsync/README.md)
  container. Terminate the server by connecting to the `terminate` Rsync
  module. When Rsync completes successfully, the command expects to read
  shares metadata from standard input in TSV format.
