# leave-domain input Schema

```txt
http://schema.nethserver.org/samba/leave-domain-input.json
```

Remove the DC from an Active Directory domain

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [leave-domain-input.json](samba/leave-domain-input.json "open original schema") |

## leave-domain input Type

`object` ([leave-domain input](leave-domain-input.md))

## leave-domain input Examples

```json
{
  "adminuser": "administrator",
  "adminpass": "Nethesis,1234",
  "designated_survivor": "dc1.mydomain.org"
}
```

# leave-domain input Properties

| Property                                     | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :------------------------------------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [adminuser](#adminuser)                      | `string` | Required | cannot be null | [leave-domain input](leave-domain-input-properties-adminuser.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/adminuser")                     |
| [adminpass](#adminpass)                      | `string` | Required | cannot be null | [leave-domain input](leave-domain-input-properties-adminpass.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/adminpass")                     |
| [designated\_survivor](#designated_survivor) | `string` | Required | cannot be null | [leave-domain input](leave-domain-input-properties-designated_survivor.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/designated_survivor") |

## adminuser



`adminuser`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [leave-domain input](leave-domain-input-properties-adminuser.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/adminuser")

### adminuser Type

`string`

### adminuser Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## adminpass



`adminpass`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [leave-domain input](leave-domain-input-properties-adminpass.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/adminpass")

### adminpass Type

`string`

### adminpass Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## designated\_survivor



`designated_survivor`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [leave-domain input](leave-domain-input-properties-designated_survivor.md "http://schema.nethserver.org/samba/leave-domain-input.json#/properties/designated_survivor")

### designated\_survivor Type

`string`

### designated\_survivor Constraints

**minimum length**: the minimum number of characters for this string is: `1`
