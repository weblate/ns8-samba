# reset-share-acls input Schema

```txt
http://schema.nethserver.org/samba/reset-share-acls-input.json
```

Reset ACLs for the shared folder and its contents

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [reset-share-acls-input.json](samba/reset-share-acls-input.json "open original schema") |

## reset-share-acls input Type

`object` ([reset-share-acls input](reset-share-acls-input.md))

## reset-share-acls input Examples

```json
{
  "name": "myshare001",
  "group": "g1",
  "permissions": "ergrw"
}
```

# reset-share-acls input Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                                          |
| :-------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [name](#name)               | `string` | Required | cannot be null | [reset-share-acls input](reset-share-acls-input-properties-name.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/name")               |
| [group](#group)             | `string` | Required | cannot be null | [reset-share-acls input](reset-share-acls-input-properties-group.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/group")             |
| [permissions](#permissions) | `string` | Required | cannot be null | [reset-share-acls input](reset-share-acls-input-properties-permissions.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/permissions") |

## name

The name of the share and of the underlying directory

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [reset-share-acls input](reset-share-acls-input-properties-name.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## group

The name of the group with initial permissions

`group`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [reset-share-acls input](reset-share-acls-input-properties-group.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/group")

### group Type

`string`

### group Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## permissions

Permissions granted to the given group and to everyone else

`permissions`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [reset-share-acls input](reset-share-acls-input-properties-permissions.md "http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/permissions")

### permissions Type

`string`

### permissions Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | :---------- |
| `"erw"`   |             |
| `"ergrw"` |             |
| `"grw"`   |             |
