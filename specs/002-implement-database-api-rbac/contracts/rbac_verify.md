# Contract: verify_role

## Function Signature
`verify_role(token: str, required_role: str, secret: str) -> bool`

## Preconditions
- Token is valid
- Role is string

## Postconditions
- Returns True if role matches or higher
- But since role agnostic, checks exact match

## Edge Cases
- Invalid token: throws error