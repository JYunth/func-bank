# Contract: encode_jwt

## Function Signature
`encode_jwt(payload: dict, secret: str, expires_hours: int = 24) -> str`

## Preconditions
- Payload is dict
- Secret is string

## Postconditions
- Returns signed JWT
- Throws error for invalid payload

## Edge Cases
- Invalid secret: throws error