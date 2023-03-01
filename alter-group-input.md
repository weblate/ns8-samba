# alter-group input Schema

```txt
http://schema.nethserver.org/samba/alter-group-input.json
```

Alter an existing group of users

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [alter-group-input.json](samba/alter-group-input.json "open original schema") |

## alter-group input Type

`object` ([alter-group input](alter-group-input.md))

## alter-group input Examples

```json
{
  "group": "developers",
  "description": "Product developers",
  "users": [
    "bob",
    "sanya",
    "alice"
  ]
}
```

# alter-group input Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                                          |
| :-------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [group](#group)             | `string` | Required | cannot be null | [alter-group input](alter-group-input-properties-group-identifier.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/group")                 |
| [description](#description) | `string` | Optional | cannot be null | [alter-group input](alter-group-input-properties-extended-group-description.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/description") |
| [users](#users)             | `array`  | Optional | cannot be null | [alter-group input](alter-group-input-properties-group-members.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/users")                    |

## group



`group`

*   is required

*   Type: `string` ([Group identifier](alter-group-input-properties-group-identifier.md))

*   cannot be null

*   defined in: [alter-group input](alter-group-input-properties-group-identifier.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/group")

### group Type

`string` ([Group identifier](alter-group-input-properties-group-identifier.md))

### group Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## description



`description`

*   is optional

*   Type: `string` ([Extended group description](alter-group-input-properties-extended-group-description.md))

*   cannot be null

*   defined in: [alter-group input](alter-group-input-properties-extended-group-description.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/description")

### description Type

`string` ([Extended group description](alter-group-input-properties-extended-group-description.md))

## users



`users`

*   is optional

*   Type: `string[]` ([User identifier](alter-group-input-properties-group-members-user-identifier.md))

*   cannot be null

*   defined in: [alter-group input](alter-group-input-properties-group-members.md "http://schema.nethserver.org/samba/alter-group-input.json#/properties/users")

### users Type

`string[]` ([User identifier](alter-group-input-properties-group-members-user-identifier.md))

# alter-group input Definitions
