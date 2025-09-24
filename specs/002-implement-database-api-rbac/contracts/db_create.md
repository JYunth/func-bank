# Contract: create_record

## Function Signature
`create_record(table: str, data: dict) -> int`

## Preconditions
- Table exists in database (schema agnostic)
- Data dict contains keys matching table columns (discovered at runtime)
- Database connection available

## Postconditions
- New record inserted with auto-generated ID
- Returns the ID (int)
- Throws error if insertion fails

## Edge Cases
- Invalid table name: throws error
- Data key mismatch with columns: throws error
- Connection failure: throws error