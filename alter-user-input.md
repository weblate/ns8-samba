# alter-user input Schema

```txt
http://schema.nethserver.org/samba/alter-user-input.json
```

Alter an existing user. Only the user identifier attibute is mandatory

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [alter-user-input.json](samba/alter-user-input.json "open original schema") |

## alter-user input Type

`object` ([alter-user input](alter-user-input.md))

## alter-user input Examples

```json
{
  "user": "alice",
  "display_name": "Alice Jordan",
  "password": "secret",
  "locked": false,
  "groups": [
    "developers",
    "managers"
  ]
}
```

# alter-user input Properties

| Property                       | Type      | Required | Nullable       | Defined by                                                                                                                                          |
| :----------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [user](#user)                  | `string`  | Required | cannot be null | [alter-user input](alter-user-input-properties-user-identifier.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/user")      |
| [display\_name](#display_name) | `string`  | Optional | cannot be null | [alter-user input](alter-user-input-properties-display-name.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/display_name") |
| [password](#password)          | `string`  | Optional | cannot be null | [alter-user input](alter-user-input-properties-new-password.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/password")     |
| [locked](#locked)              | `boolean` | Optional | cannot be null | [alter-user input](alter-user-input-properties-locked.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/locked")             |
| [groups](#groups)              | `array`   | Optional | cannot be null | [alter-user input](alter-user-input-properties-group-membership.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/groups")   |

## user

The user must exist

`user`

*   is required

*   Type: `string` ([User identifier](alter-user-input-properties-user-identifier.md))

*   cannot be null

*   defined in: [alter-user input](alter-user-input-properties-user-identifier.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/user")

### user Type

`string` ([User identifier](alter-user-input-properties-user-identifier.md))

### user Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## display\_name



`display_name`

*   is optional

*   Type: `string` ([Display name](alter-user-input-properties-display-name.md))

*   cannot be null

*   defined in: [alter-user input](alter-user-input-properties-display-name.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/display_name")

### display\_name Type

`string` ([Display name](alter-user-input-properties-display-name.md))

### display\_name Constraints

**maximum length**: the maximum number of characters for this string is: `32`

## password

If empty, a random password is set

`password`

*   is optional

*   Type: `string` ([New password](alter-user-input-properties-new-password.md))

*   cannot be null

*   defined in: [alter-user input](alter-user-input-properties-new-password.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/password")

### password Type

`string` ([New password](alter-user-input-properties-new-password.md))

### password Constraints

**minimum length**: the minimum number of characters for this string is: `0`

## locked

True, if the user account has been locked, preventing the user from logging in

`locked`

*   is optional

*   Type: `boolean` ([Locked](alter-user-input-properties-locked.md))

*   cannot be null

*   defined in: [alter-user input](alter-user-input-properties-locked.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/locked")

### locked Type

`boolean` ([Locked](alter-user-input-properties-locked.md))

## groups

Set the user as a member of the given list of groups

`groups`

*   is optional

*   Type: `string[]` ([Group identifier](alter-user-input-properties-group-membership-group-identifier.md))

*   cannot be null

*   defined in: [alter-user input](alter-user-input-properties-group-membership.md "http://schema.nethserver.org/samba/alter-user-input.json#/properties/groups")

### groups Type

`string[]` ([Group identifier](alter-user-input-properties-group-membership-group-identifier.md))

# alter-user input Definitions
