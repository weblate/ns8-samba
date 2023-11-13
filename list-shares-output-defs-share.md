# Untitled object in list-shares output Schema

```txt
http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-shares-output.json\*](samba/list-shares-output.json "open original schema") |

## share Type

`object` ([Details](list-shares-output-defs-share.md))

# share Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                                                           |
| :-------------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)               | `string` | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-share-name.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/name")               |
| [description](#description) | `string` | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-share-description.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/description") |
| [acls](#acls)               | `array`  | Optional | cannot be null | [list-shares output](list-shares-output-defs-share-properties-acls.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/acls")                     |

## name

Name of the share corresponding to the underlying directory name

`name`

*   is optional

*   Type: `string` ([Share name](list-shares-output-defs-share-properties-share-name.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-share-name.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/name")

### name Type

`string` ([Share name](list-shares-output-defs-share-properties-share-name.md))

## description

Free text, known also as "comment"

`description`

*   is optional

*   Type: `string` ([Share description](list-shares-output-defs-share-properties-share-description.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-share-description.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/description")

### description Type

`string` ([Share description](list-shares-output-defs-share-properties-share-description.md))

## acls



`acls`

*   is optional

*   Type: `object[]` ([ACL item](list-shares-output-defs-acl-item.md))

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-share-properties-acls.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/share/properties/acls")

### acls Type

`object[]` ([ACL item](list-shares-output-defs-acl-item.md))
