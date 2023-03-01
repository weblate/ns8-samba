# README

## Top-level Schemas

*   [add-group input](./add-group-input.md "Add a group of users to the AD database") – `http://schema.nethserver.org/samba/add-group-input.json`

*   [add-user input](./add-user-input.md "Add a user to the AD database") – `http://schema.nethserver.org/samba/add-user-input.json`

*   [alter-group input](./alter-group-input.md "Alter an existing group of users") – `http://schema.nethserver.org/samba/alter-group-input.json`

*   [alter-user input](./alter-user-input.md "Alter an existing user") – `http://schema.nethserver.org/samba/alter-user-input.json`

*   [get-defaults input](./get-defaults-input.md "Compute the values that suit the configure-module action input") – `http://schema.nethserver.org/samba/get-defaults-input.json`

*   [get-defaults output](./get-defaults-output.md "Return values that suit the configure-module action input") – `http://schema.nethserver.org/samba/get-defaults-output.json`

*   [remove-group input](./remove-group-input.md "Remove an existing group of users") – `http://schema.nethserver.org/samba/remove-group-input.json`

*   [remove-user input](./remove-user-input.md "Remove an existing user") – `http://schema.nethserver.org/samba/remove-user-input.json`

*   [set-ipaddress input](./configure-module-input.md "Change the DC IP address") – `http://schema.nethserver.org/samba/configure-module-input.json`

*   [set-routes input](./set-routes-input.md "Decide if DC traffic is routed through the cluster VPN") – `http://schema.nethserver.org/samba/set-routes-input.json`

*   [set-routes output](./set-routes-output.md "Just an empty object, representing a successful response") – `http://schema.nethserver.org/samba/set-routes-output.json`

## Other Schemas

### Objects

*   [Untitled object in get-defaults output](./get-defaults-output-properties-ipaddress_list-items.md) – `http://schema.nethserver.org/samba/get-defaults-output.json#/properties/ipaddress_list/items`

### Arrays

*   [Group members](./add-group-input-properties-group-members.md) – `http://schema.nethserver.org/samba/add-group-input.json#/properties/users`

*   [Group members](./alter-group-input-properties-group-members.md) – `http://schema.nethserver.org/samba/alter-group-input.json#/properties/users`

*   [Group membership](./alter-user-input-properties-group-membership.md "Set the user as a member of the given list of groups") – `http://schema.nethserver.org/samba/alter-user-input.json#/properties/groups`

*   [Initial group membership](./add-user-input-properties-initial-group-membership.md "Set the user as a member of the given list of groups") – `http://schema.nethserver.org/samba/add-user-input.json#/properties/groups`

*   [Untitled array in get-defaults output](./get-defaults-output-properties-ipaddress_list.md) – `http://schema.nethserver.org/samba/get-defaults-output.json#/properties/ipaddress_list`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
