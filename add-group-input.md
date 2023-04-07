# add-group input Schema

```txt
http://schema.nethserver.org/samba/add-group-input.json
```

Add a group of users to the AD database

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [add-group-input.json](samba/add-group-input.json "open original schema") |

## add-group input Type

`object` ([add-group input](add-group-input.md))

## add-group input Examples

```json
{
  "group": "developers",
  "description": "",
  "users": [
    "bob",
    "alice"
  ]
}
```

# add-group input Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                                    |
| :-------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [group](#group)             | `string` | Required | cannot be null | [add-group input](add-group-input-properties-group-identifier.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/group")                 |
| [description](#description) | `string` | Optional | cannot be null | [add-group input](add-group-input-properties-extended-group-description.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/description") |
| [users](#users)             | `array`  | Required | cannot be null | [add-group input](add-group-input-properties-group-members.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/users")                    |

## group



`group`

*   is required

*   Type: `string` ([Group identifier](add-group-input-properties-group-identifier.md))

*   cannot be null

*   defined in: [add-group input](add-group-input-properties-group-identifier.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/group")

### group Type

`string` ([Group identifier](add-group-input-properties-group-identifier.md))

### group Constraints

**maximum length**: the maximum number of characters for this string is: `255`

**minimum length**: the minimum number of characters for this string is: `1`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[a-zA-Z][-._a-zA-Z0-9]*$
```

[try pattern](https://regexr.com/?expression=%5E%5Ba-zA-Z%5D%5B-._a-zA-Z0-9%5D*%24 "try regular expression with regexr.com")

## description



`description`

*   is optional

*   Type: `string` ([Extended group description](add-group-input-properties-extended-group-description.md))

*   cannot be null

*   defined in: [add-group input](add-group-input-properties-extended-group-description.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/description")

### description Type

`string` ([Extended group description](add-group-input-properties-extended-group-description.md))

### description Constraints

**maximum length**: the maximum number of characters for this string is: `256`

## users



`users`

*   is required

*   Type: `string[]` ([User identifier](add-group-input-properties-group-members-user-identifier.md))

*   cannot be null

*   defined in: [add-group input](add-group-input-properties-group-members.md "http://schema.nethserver.org/samba/add-group-input.json#/properties/users")

### users Type

`string[]` ([User identifier](add-group-input-properties-group-members-user-identifier.md))

# add-group input Definitions
