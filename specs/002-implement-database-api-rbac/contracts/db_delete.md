# Contract: delete_record

## Function Signature
`delete_record(table: str, id: int) -> bool`

## Preconditions
- Table exists
- ID is valid

## Postconditions
- Returns True if deleted
- Returns False if not found
- Soft delete if deleted_at column exists

## Edge Cases
- Record not found: returns False