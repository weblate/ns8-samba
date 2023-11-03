# set-ipaddress input Schema

```txt
http://schema.nethserver.org/samba/configure-module-input.json
```

Change the DC IP address

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [configure-module-input.json](samba/configure-module-input.json "open original schema") |

## set-ipaddress input Type

`object` ([set-ipaddress input](configure-module-input.md))

## set-ipaddress input Examples

```json
{
  "ipaddress": "10.15.21.100"
}
```

# set-ipaddress input Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                   |
| :---------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ipaddress](#ipaddress) | `string` | Required | cannot be null | [set-ipaddress input](configure-module-input-properties-ipaddress.md "http://schema.nethserver.org/samba/configure-module-input.json#/properties/ipaddress") |

## ipaddress



`ipaddress`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [set-ipaddress input](configure-module-input-properties-ipaddress.md "http://schema.nethserver.org/samba/configure-module-input.json#/properties/ipaddress")

### ipaddress Type

`string`

### ipaddress Constraints

**IPv4**: the string must be an IPv4 address (dotted quad), according to [RFC 2673, section 3.2](https://tools.ietf.org/html/rfc2673 "check the specification")
