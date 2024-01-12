# add-share input Schema

```txt
http://schema.nethserver.org/samba/add-share-input.json
```

Create a new shared folder

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [add-share-input.json](samba/add-share-input.json "open original schema") |

## add-share input Type

`object` ([add-share input](add-share-input.md))

## add-share input Examples

```json
{
  "name": "myshare001",
  "description": "First share"
}
```

```json
{
  "name": "myshare001",
  "description": "First share",
  "group": "g1",
  "permissions": "ergrw"
}
```

# add-share input Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                     |
| :-------------------------- | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)               | `string` | Required | cannot be null | [add-share input](add-share-input-properties-name.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/name")               |
| [description](#description) | `string` | Optional | cannot be null | [add-share input](add-share-input-properties-description.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/description") |
| [group](#group)             | `string` | Optional | cannot be null | [add-share input](add-share-input-properties-group.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/group")             |
| [permissions](#permissions) | `string` | Optional | cannot be null | [add-share input](add-share-input-properties-permissions.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/permissions") |

## name

The name of the share and of the underlying directory

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [add-share input](add-share-input-properties-name.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## description

Free text for share comment or description

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [add-share input](add-share-input-properties-description.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/description")

### description Type

`string`

## group

The name of the group with initial permissions

`group`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [add-share input](add-share-input-properties-group.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/group")

### group Type

`string`

### group Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## permissions

Permissions granted to the given group and to everyone else

`permissions`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [add-share input](add-share-input-properties-permissions.md "http://schema.nethserver.org/samba/add-share-input.json#/properties/permissions")

### permissions Type

`string`

### permissions Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | :---------- |
| `"erw"`   |             |
| `"ergrw"` |             |
| `"grw"`   |             |
