# Contract: read_record

## Function Signature
`read_record(table: str, id: int) -> dict | None`

## Preconditions
- Table exists
- ID is valid integer

## Postconditions
- Returns record dict if found
- Returns None if not found
- Throws error for connection issues

## Edge Cases
- Non-existent table: throws error
- Invalid ID: throws error