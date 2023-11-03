# Untitled string in reset-share-acls input Schema

```txt
http://schema.nethserver.org/samba/reset-share-acls-input.json#/properties/permissions
```

Permissions granted to the given group and to everyone else

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [reset-share-acls-input.json\*](samba/reset-share-acls-input.json "open original schema") |

## permissions Type

`string`

## permissions Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | :---------- |
| `"erw"`   |             |
| `"ergrw"` |             |
| `"grw"`   |             |
