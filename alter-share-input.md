# alter-share input Schema

```txt
http://schema.nethserver.org/samba/alter-share-input.json
```

Alter a shared folder

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [alter-share-input.json](samba/alter-share-input.json "open original schema") |

## alter-share input Type

`object` ([alter-share input](alter-share-input.md))

## alter-share input Examples

```json
{
  "name": "myshare001",
  "description": "New description"
}
```

# alter-share input Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                           |
| :-------------------------- | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)               | `string` | Required | cannot be null | [alter-share input](alter-share-input-properties-name.md "http://schema.nethserver.org/samba/alter-share-input.json#/properties/name")               |
| [description](#description) | `string` | Optional | cannot be null | [alter-share input](alter-share-input-properties-description.md "http://schema.nethserver.org/samba/alter-share-input.json#/properties/description") |

## name

The name of the share and of the underlying directory

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [alter-share input](alter-share-input-properties-name.md "http://schema.nethserver.org/samba/alter-share-input.json#/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## description

Free text for share comment or description

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [alter-share input](alter-share-input-properties-description.md "http://schema.nethserver.org/samba/alter-share-input.json#/properties/description")

### description Type

`string`
