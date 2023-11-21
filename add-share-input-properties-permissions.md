# Untitled string in add-share input Schema

```txt
http://schema.nethserver.org/samba/add-share-input.json#/properties/permissions
```

Permissions granted to the given group and to everyone else

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [add-share-input.json\*](samba/add-share-input.json "open original schema") |

## permissions Type

`string`

## permissions Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | :---------- |
| `"erw"`   |             |
| `"ergrw"` |             |
| `"grw"`   |             |
