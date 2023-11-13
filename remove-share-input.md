# remove-share input Schema

```txt
http://schema.nethserver.org/samba/remove-share-input.json
```

Remove a shared folder and its contents

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [remove-share-input.json](samba/remove-share-input.json "open original schema") |

## remove-share input Type

`object` ([remove-share input](remove-share-input.md))

## remove-share input Examples

```json
{
  "name": "myshare001"
}
```

# remove-share input Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                |
| :------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name) | `string` | Required | cannot be null | [remove-share input](remove-share-input-properties-name.md "http://schema.nethserver.org/samba/remove-share-input.json#/properties/name") |

## name

The name of the share and of the underlying directory

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [remove-share input](remove-share-input-properties-name.md "http://schema.nethserver.org/samba/remove-share-input.json#/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`
