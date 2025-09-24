# Contract: decode_jwt

## Function Signature
`decode_jwt(token: str, secret: str) -> dict | None`

## Preconditions
- Token is string
- Secret matches

## Postconditions
- Returns payload dict or None
- Throws error for malformed token

## Edge Cases
- Expired token: returns None