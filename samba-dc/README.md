# samba-dc


## Environment variables

- SAMBA_SHARES_DIR, default "/srv/shares" path to the volume containing
  user home dirs and shared folders. Do not change it! In any case do not
  put under /var/lib/samba to avoid conflicts with the backup procedure. 
