# Contract: store_file

## Function Signature
`store_file(filename: str, data: bytes, metadata: dict = {}) -> str`

## Preconditions
- Data is valid bytes
- Metadata is dict

## Postconditions
- Returns unique file ID
- Stores in database

## Edge Cases
- Large file: throws error