# README

## Top-level Schemas

*   [acquire-fsmo input](./acquire-fsmo-input.md "Acquire FSMO roles") – `http://schema.nethserver.org/samba/acquire-fsmo-input.json`

*   [add-group input](./add-group-input.md "Add a group of users to the AD database") – `http://schema.nethserver.org/samba/add-group-input.json`

*   [add-share input](./add-share-input.md "Create a new shared folder") – `http://schema.nethserver.org/samba/add-share-input.json`

*   [add-user input](./add-user-input.md "Add a user to the AD database") – `http://schema.nethserver.org/samba/add-user-input.json`

*   [alter-group input](./alter-group-input.md "Alter an existing group of users") – `http://schema.nethserver.org/samba/alter-group-input.json`

*   [alter-share input](./alter-share-input.md "Alter a shared folder") – `http://schema.nethserver.org/samba/alter-share-input.json`

*   [alter-user input](./alter-user-input.md "Alter an existing user") – `http://schema.nethserver.org/samba/alter-user-input.json`

*   [get-defaults input](./get-defaults-input.md "Compute the values that suit the configure-module action input") – `http://schema.nethserver.org/samba/get-defaults-input.json`

*   [get-defaults output](./get-defaults-output.md "Return values that suit the configure-module action input") – `http://schema.nethserver.org/samba/get-defaults-output.json`

*   [leave-domain input](./leave-domain-input.md "Remove the DC from an Active Directory domain") – `http://schema.nethserver.org/samba/leave-domain-input.json`

*   [list-shares output](./list-shares-output.md "Return the list of shared folders and their attributes") – `http://schema.nethserver.org/samba/list-shares-output.json`

*   [remove-group input](./remove-group-input.md "Remove an existing group of users") – `http://schema.nethserver.org/samba/remove-group-input.json`

*   [remove-share input](./remove-share-input.md "Remove a shared folder and its contents") – `http://schema.nethserver.org/samba/remove-share-input.json`

*   [remove-user input](./remove-user-input.md "Remove an existing user") – `http://schema.nethserver.org/samba/remove-user-input.json`

*   [reset-share-acls input](./reset-share-acls-input.md "Reset ACLs for the shared folder and its contents") – `http://schema.nethserver.org/samba/reset-share-acls-input.json`

*   [set-ipaddress input](./configure-module-input.md "Change the DC IP address") – `http://schema.nethserver.org/samba/configure-module-input.json`

## Other Schemas

### Objects

*   [ACL item](./list-shares-output-defs-acl-item.md "Translation of low-level Windows ACE to a simplified format") – `http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item`

*   [Untitled object in get-defaults input](./get-defaults-input-anyof-0.md) – `http://schema.nethserver.org/samba/get-defaults-input.json#/anyOf/0`

*   [Untitled object in get-defaults input](./get-defaults-input-anyof-1.md) – `http://schema.nethserver.org/samba/get-defaults-input.json#/anyOf/1`

*   [Untitled object in get-defaults output](./get-defaults-output-properties-ipaddress_list-items.md) – `http://schema.nethserver.org/samba/get-defaults-output.json#/properties/ipaddress_list/items`

*   [Untitled object in list-shares output](./list-shares-output-defs-share.md) – `http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share`

### Arrays

*   [Group members](./add-group-input-properties-group-members.md) – `http://schema.nethserver.org/samba/add-group-input.json#/properties/users`

*   [Group members](./alter-group-input-properties-group-members.md) – `http://schema.nethserver.org/samba/alter-group-input.json#/properties/users`

*   [Group membership](./alter-user-input-properties-group-membership.md "Set the user as a member of the given list of groups") – `http://schema.nethserver.org/samba/alter-user-input.json#/properties/groups`

*   [Initial group membership](./add-user-input-properties-initial-group-membership.md "Set the user as a member of the given list of groups") – `http://schema.nethserver.org/samba/add-user-input.json#/properties/groups`

*   [Untitled array in get-defaults output](./get-defaults-output-properties-ipaddress_list.md) – `http://schema.nethserver.org/samba/get-defaults-output.json#/properties/ipaddress_list`

*   [Untitled array in list-shares output](./list-shares-output-properties-shares.md) – `http://schema.nethserver.org/samba/list-shares-output.json#/properties/shares`

*   [Untitled array in list-shares output](./list-shares-output-defs-share-properties-acls.md) – `http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/acls`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
