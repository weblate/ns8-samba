# New password Schema

```txt
http://schema.nethserver.org/samba/alter-user-input.json#/properties/password
```

If empty, a random password is set

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [alter-user-input.json\*](samba/alter-user-input.json "open original schema") |

## password Type

`string` ([New password](alter-user-input-properties-new-password.md))

## password Constraints

**minimum length**: the minimum number of characters for this string is: `0`
