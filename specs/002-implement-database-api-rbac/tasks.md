# Tasks: Implement Database, API, and RBAC Components

**Input**: Design documents from `/specs/002-implement-database-api-rbac/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack (PostgreSQL, SQLAlchemy, PyJWT), libraries, structure
2. Load optional design documents:
   → data-model.md: Agnostic design - no specific entities → no model tasks
   → contracts/: 13 files → 13 contract test tasks
   → research.md: Extract decisions → setup tasks (dependencies, pgvector)
   → quickstart.md: Extract test scenarios → integration tests
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: 13 contract tests, 4 integration tests
   → Core: 13 function implementations (DB, API, RBAC)
   → Integration: DB connection, logging, error handling
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests? Yes
   → All entities have models? N/A (agnostic)
   → All endpoints implemented? Yes (API contracts)
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [x] T001 Create project structure: src/func_bank/ for components, tests/unit/, tests/contract/, tests/integration/
- [x] T002 Initialize Python project with SQLAlchemy, psycopg2, PyJWT, pgvector dependencies via uv
- [x] T003 [P] Configure linting and formatting tools (black, flake8) in pyproject.toml

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T004 [P] Contract test for create_record in tests/contract/test_db_create.py
- [x] T005 [P] Contract test for read_record in tests/contract/test_db_read.py
- [x] T006 [P] Contract test for update_record in tests/contract/test_db_update.py
- [x] T007 [P] Contract test for delete_record in tests/contract/test_db_delete.py
- [x] T008 [P] Contract test for query_records in tests/contract/test_db_query.py
- [x] T009 [P] Contract test for vector_search in tests/contract/test_db_vector.py
- [x] T010 [P] Contract test for store_file in tests/contract/test_db_files.py
- [x] T011 [P] Contract test for handle_crud in tests/contract/test_api_crud.py
- [x] T012 [P] Contract test for handle_multipart in tests/contract/test_api_multipart.py
- [x] T013 [P] Contract test for encode_jwt in tests/contract/test_jwt_encode.py
- [x] T014 [P] Contract test for decode_jwt in tests/contract/test_jwt_decode.py
- [x] T015 [P] Contract test for verify_role in tests/contract/test_rbac_verify.py
- [x] T016 [P] Contract test for verify_role_level in tests/contract/test_rbac_level.py
- [x] T017 [P] Integration test for CRUD operations in tests/integration/test_crud_operations.py
- [x] T018 [P] Integration test for JWT auth flow in tests/integration/test_jwt_auth.py
- [x] T019 [P] Integration test for RBAC verification in tests/integration/test_rbac_integration.py
- [x] T020 [P] Integration test for API with DB and RBAC in tests/integration/test_api_integration.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T021 [P] Implement create_record function in src/func_bank/db_create.py
- [x] T022 [P] Implement read_record function in src/func_bank/db_read.py
- [x] T023 [P] Implement update_record function in src/func_bank/db_update.py
- [x] T024 [P] Implement delete_record function in src/func_bank/db_delete.py
- [x] T025 [P] Implement query_records function in src/func_bank/db_query.py
- [x] T026 [P] Implement vector_search function in src/func_bank/db_vector.py
- [x] T027 [P] Implement store_file function in src/func_bank/db_files.py
- [x] T028 [P] Implement handle_crud function in src/func_bank/api_crud.py
- [x] T029 [P] Implement handle_multipart function in src/func_bank/api_multipart.py
- [x] T030 [P] Implement encode_jwt function in src/func_bank/jwt_encode.py
- [x] T031 [P] Implement decode_jwt function in src/func_bank/jwt_decode.py
- [x] T032 [P] Implement verify_role function in src/func_bank/rbac_verify.py
- [x] T033 [P] Implement verify_role_level function in src/func_bank/rbac_level.py

## Phase 3.4: Integration
- [x] T034 Set up database connection and session management in src/func_bank/db_connection.py
- [x] T035 Implement structured logging and metrics for all components
- [x] T036 Add error handling and well-documented exceptions across all functions
- [x] T037 Integrate components: ensure API uses DB and RBAC seamlessly

## Phase 3.5: Polish
- [x] T038 [P] Unit tests for validation and edge cases in tests/unit/test_validation.py
- [x] T039 Performance tests for CRUD operations (<100ms average) in tests/unit/test_performance.py
- [x] T040 [P] Update README.md with usage examples and integration guide
- [x] T041 [P] Add docstrings and type hints to all functions
- [x] T042 Run all tests and ensure passing (Note: DB tests require PostgreSQL running)

## Dependencies
- Setup (T001-T003) before everything
- Tests (T004-T020) before implementation (T021-T033)
- Implementation (T021-T033) before integration (T034-T037)
- Integration before polish (T038-T042)
- No blocking dependencies within [P] tasks

## Parallel Example
```
# Launch T004-T016 together (contract tests):
Task: "Contract test for create_record in tests/contract/test_db_create.py"
Task: "Contract test for read_record in tests/contract/test_db_read.py"
... (up to T016)

# Launch T017-T020 together (integration tests):
Task: "Integration test for CRUD operations in tests/integration/test_crud_operations.py"
Task: "Integration test for JWT auth flow in tests/integration/test_jwt_auth.py"
Task: "Integration test for RBAC verification in tests/integration/test_rbac_integration.py"
Task: "Integration test for API with DB and RBAC in tests/integration/test_api_integration.py"

# Launch T021-T033 together (core implementations):
Task: "Implement create_record function in src/func_bank/db_create.py"
... (up to T033)
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Agnostic design: no schema assumptions in implementations
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each API contract → implementation task [P]
   
2. **From Data Model**:
   - Agnostic design → no entity-specific tasks
   
3. **From User Stories**:
   - Each acceptance scenario → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Core → Integration → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks (N/A for agnostic)
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [x] No task modifies same file as another [P] task