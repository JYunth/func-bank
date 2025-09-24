# Contract: handle_crud

## Function Signature
`handle_crud(method: str, table: str, data: dict = None, id: int = None) -> dict`

## Preconditions
- Method is GET/POST/PUT/DELETE
- Table exists

## Postconditions
- Returns standardized response dict
- Throws error for invalid requests

## Edge Cases
- Invalid method: throws error