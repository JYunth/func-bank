# Contract: update_record

## Function Signature
`update_record(table: str, id: int, data: dict) -> bool`

## Preconditions
- Table exists
- ID exists
- Data contains valid updates

## Postconditions
- Returns True if updated
- Returns False if record not found
- Throws error for conflicts or invalid data

## Edge Cases
- Record not found: returns False
- Version conflict (optimistic locking): throws error