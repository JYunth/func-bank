# Contract: handle_multipart

## Function Signature
`handle_multipart(request) -> dict`

## Preconditions
- Request is multipart

## Postconditions
- Returns parsed files and data
- Throws error for size limits

## Edge Cases
- No files: returns empty