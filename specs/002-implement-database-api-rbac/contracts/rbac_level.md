# Contract: verify_role_level

## Function Signature
`verify_role_level(token: str, min_level: int, secret: str) -> bool`

## Preconditions
- Token valid
- Level is int

## Postconditions
- Returns True if level >= min
- Levels customizable

## Edge Cases
- Invalid level: throws error