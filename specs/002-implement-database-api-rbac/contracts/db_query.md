# Contract: query_records

## Function Signature
`query_records(table: str, filters: dict, limit: int = 100) -> list[dict]`

## Preconditions
- Table exists
- Filters are valid dict

## Postconditions
- Returns list of matching records
- Limited to specified limit

## Edge Cases
- No matches: returns empty list