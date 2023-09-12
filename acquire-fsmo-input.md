# acquire-fsmo input Schema

```txt
http://schema.nethserver.org/samba/acquire-fsmo-input.json
```

Acquire FSMO roles

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [acquire-fsmo-input.json](samba/acquire-fsmo-input.json "open original schema") |

## acquire-fsmo input Type

`object` ([acquire-fsmo input](acquire-fsmo-input.md))

## acquire-fsmo input Examples

```json
{
  "adminuser": "administrator",
  "adminpass": "Nethesis,1234"
}
```

# acquire-fsmo input Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                          |
| :---------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [adminuser](#adminuser) | `string` | Required | cannot be null | [acquire-fsmo input](acquire-fsmo-input-properties-adminuser.md "http://schema.nethserver.org/samba/acquire-fsmo-input.json#/properties/adminuser") |
| [adminpass](#adminpass) | `string` | Required | cannot be null | [acquire-fsmo input](acquire-fsmo-input-properties-adminpass.md "http://schema.nethserver.org/samba/acquire-fsmo-input.json#/properties/adminpass") |

## adminuser



`adminuser`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [acquire-fsmo input](acquire-fsmo-input-properties-adminuser.md "http://schema.nethserver.org/samba/acquire-fsmo-input.json#/properties/adminuser")

### adminuser Type

`string`

### adminuser Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## adminpass



`adminpass`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [acquire-fsmo input](acquire-fsmo-input-properties-adminpass.md "http://schema.nethserver.org/samba/acquire-fsmo-input.json#/properties/adminpass")

### adminpass Type

`string`

### adminpass Constraints

**minimum length**: the minimum number of characters for this string is: `1`
