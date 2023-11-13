# ACL item Schema

```txt
http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item
```

Translation of low-level Windows ACE to a simplified format

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-shares-output.json\*](samba/list-shares-output.json "open original schema") |

## acl\_item Type

`object` ([ACL item](list-shares-output-defs-acl-item.md))

# acl\_item Properties

| Property            | Type          | Required | Nullable       | Defined by                                                                                                                                                                   |
| :------------------ | :------------ | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [subject](#subject) | `string`      | Required | cannot be null | [list-shares output](list-shares-output-defs-acl-item-properties-subject.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/subject") |
| [rights](#rights)   | Not specified | Required | cannot be null | [list-shares output](list-shares-output-defs-acl-item-properties-rights.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/rights")   |

## subject



`subject`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-acl-item-properties-subject.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/subject")

### subject Type

`string`

## rights



`rights`

*   is required

*   Type: unknown

*   cannot be null

*   defined in: [list-shares output](list-shares-output-defs-acl-item-properties-rights.md "http://schema.nethserver.org/samba/list-shares-output.json#/$defs/acl_item/properties/rights")

### rights Type

unknown

### rights Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |
| :---------- | :---------- |
| `"full"`    |             |
| `"ro"`      |             |
| `"rw"`      |             |
| `"special"` |             |
