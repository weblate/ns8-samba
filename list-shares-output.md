# list-shares output Schema

```txt
http://schema.nethserver.org/samba/list-shares-output.json
```

Return the list of shared folders and their attributes

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-shares-output.json](samba/list-shares-output.json "open original schema") |

## list-shares output Type

`object` ([list-shares output](list-shares-output.md))

## list-shares output Examples

```json
{
  "shares": [
    {
      "name": "myshare001",
      "description": "First share",
      "acls": [
        {
          "subject": "BUILTIN\\Administrators",
          "rights": "full"
        },
        {
          "subject": "Domain Controllers",
          "rights": "special"
        },
        {
          "subject": "g1",
          "rights": "rw"
        },
        {
          "subject": "Everyone",
          "rights": "ro"
        }
      ]
    },
    {
      "name": "myshare002",
      "description": "Second share",
      "acls": [
        {
          "subject": "BUILTIN\\Administrators",
          "rights": "full"
        },
        {
          "subject": "Domain Controllers",
          "rights": "special"
        },
        {
          "subject": "Everyone",
          "rights": "rw"
        }
      ]
    }
  ]
}
```

# list-shares output Properties

| Property          | Type    | Required | Nullable       | Defined by                                                                                                                                    |
| :---------------- | :------ | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| [shares](#shares) | `array` | Required | cannot be null | [list-shares output](list-shares-output-properties-shares.md "http://schema.nethserver.org/samba/list-shares-output.json#/properties/shares") |

## shares



`shares`

*   is required

*   Type: `object[]` ([Details](list-shares-output-defs-share.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-properties-shares.md "http://schema.nethserver.org/samba/list-shares-output.json#/properties/shares")

### shares Type

`object[]` ([Details](list-shares-output-defs-share.md))

# list-shares output Definitions

## Definitions group share

Reference this group by using

```json
{"$ref":"http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share"}
```

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                                                           |
| :-------------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)               | `string` | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-share-name.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/name")               |
| [description](#description) | `string` | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-share-description.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/description") |
| [acls](#acls)               | `array`  | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-acls.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/acls")                     |

### name

Name of the share corresponding to the underlying directory name

`name`

*   is optional

*   Type: `string` ([Share name](list-shares-output-defs-share-properties-share-name.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-share-name.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/name")

#### name Type

`string` ([Share name](list-shares-output-defs-share-properties-share-name.md))

### description

Free text, known also as "comment"

`description`

*   is optional

*   Type: `string` ([Share description](list-shares-output-defs-share-properties-share-description.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-share-description.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/description")

#### description Type

`string` ([Share description](list-shares-output-defs-share-properties-share-description.md))

### acls



`acls`

*   is optional

*   Type: `object[]` ([ACL item](list-shares-output-defs-acl-item.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-acls.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/acls")

#### acls Type

`object[]` ([ACL item](list-shares-output-defs-acl-item.md))

## Definitions group acl\_item

Reference this group by using

```json
{"$ref":"http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item"}
```

| Property            | Type          | Required | Nullable       | Defined by                                                                                                                                                                   |
| :------------------ | :------------ | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [subject](#subject) | `string`      | Required | cannot be null | [list-shares output](list-shares-output-defs-acl-item-properties-subject.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/subject") |
| [rights](#rights)   | Not specified | Required | cannot be null | [list-shares output](list-shares-output-defs-acl-item-properties-rights.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/rights")   |

### subject



`subject`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-acl-item-properties-subject.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/subject")

#### subject Type

`string`

### rights



`rights`

*   is required

*   Type: unknown

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-acl-item-properties-rights.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/rights")

#### rights Type

unknown

#### rights Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |
| :---------- | :---------- |
| `"full"`    |             |
| `"ro"`      |             |
| `"rw"`      |             |
| `"special"` |             |
