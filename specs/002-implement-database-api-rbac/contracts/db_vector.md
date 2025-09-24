# Contract: vector_search

## Function Signature
`vector_search(table: str, embedding: list[float], limit: int = 10, embedding_column: str = 'embedding') -> list[dict]`

## Preconditions
- Table has column specified by embedding_column
- Embedding is valid vector

## Postconditions
- Returns records sorted by similarity using the specified column
- Throws error if pgvector not available or column doesn't exist

## Edge Cases
- No matches: returns empty list
- Invalid column name: throws error