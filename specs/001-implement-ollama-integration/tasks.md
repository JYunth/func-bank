# Tasks: Implement Ollama Integration Components

**Input**: Design documents from `/specs/001-implement-ollama-integration/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Extract: Python 3.11, ollama library, pytest, single project structure
2. Load optional design documents:
   → data-model.md: Extract entities → validation tasks
   → contracts/: 4 function contracts → contract test tasks
   → research.md: Python + ollama decisions → setup tasks
   → quickstart.md: 4 test scenarios → integration test tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: function implementations
   → Integration: error handling
   → Polish: unit tests, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests? Yes
   → All entities have validations? Yes
   → All functions implemented? Yes
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure

## Phase 3.1: Setup
- [x] T001 Create project structure: src/ and tests/ directories at repository root
- [x] T002 Initialize Python 3.11 project with ollama dependency in requirements.txt
- [x] T003 Configure pytest and black/flake8 linting in pyproject.toml

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T004 [P] Contract test for generate_embedding function in tests/contract/test_generate_embedding.py
- [x] T005 [P] Contract test for simple_chat function in tests/contract/test_simple_chat.py
- [x] T006 [P] Contract test for chat_with_history function in tests/contract/test_chat_with_history.py
- [x] T007 [P] Contract test for chat_with_tools function in tests/contract/test_chat_with_tools.py
- [x] T008 [P] Integration test for embedding generation scenario in tests/integration/test_embedding_generation.py
- [x] T009 [P] Integration test for simple chat response scenario in tests/integration/test_simple_chat_response.py
- [x] T010 [P] Integration test for chat with history scenario in tests/integration/test_chat_with_history.py
- [x] T011 [P] Integration test for chat with tools scenario in tests/integration/test_chat_with_tools.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T012 Implement generate_embedding function in src/ollama_integration.py
- [x] T013 Implement simple_chat function in src/ollama_integration.py
- [x] T014 Implement chat_with_history function in src/ollama_integration.py
- [x] T015 Implement chat_with_tools function in src/ollama_integration.py
- [x] T016 Add input validation for all functions in src/ollama_integration.py
- [x] T017 Add error handling and logging in src/ollama_integration.py

## Phase 3.4: Integration
- [x] T018 Validate Ollama service connection handling

## Phase 3.5: Polish
- [x] T019 [P] Unit tests for data validation in tests/unit/test_validation.py
- [x] T020 Performance tests (no specific targets defined)
- [x] T021 [P] Update README.md with usage examples
- [x] T022 Code cleanup and remove duplication

## Dependencies
- Setup (T001-T003) before all other tasks
- Tests (T004-T011) before implementation (T012-T017)
- Implementation (T012-T017) before integration (T018) and polish (T019-T022)
- T012-T015 can be sequential due to same file (src/ollama_integration.py)
- T016-T017 depend on T012-T015

## Parallel Example
```
# Launch T004-T011 together (all contract and integration tests):
Task: "Contract test for generate_embedding function in tests/contract/test_generate_embedding.py"
Task: "Contract test for simple_chat function in tests/contract/test_simple_chat.py"
Task: "Contract test for chat_with_history function in tests/contract/test_chat_with_history.py"
Task: "Contract test for chat_with_tools function in tests/contract/test_chat_with_tools.py"
Task: "Integration test for embedding generation scenario in tests/integration/test_embedding_generation.py"
Task: "Integration test for simple chat response scenario in tests/integration/test_simple_chat_response.py"
Task: "Integration test for chat with history scenario in tests/integration/test_chat_with_history.py"
Task: "Integration test for chat with tools scenario in tests/integration/test_chat_with_tools.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify all tests fail before implementing any functions
- Commit after each task completion
- Avoid: vague tasks, same file conflicts
- All tasks specify exact file paths for immediate execution

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each of 4 contract files → 1 contract test task [P]

2. **From Data Model**:
   - 4 entities → validation tasks integrated into implementation

3. **From User Stories**:
   - 4 acceptance scenarios → 4 integration test tasks [P]

4. **Ordering**:
   - Setup → Tests → Core Implementation → Integration → Polish
   - Dependencies prevent parallel execution where files overlap

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have validation tasks
- [x] All tests come before implementation
- [x] Parallel tasks are independent (different files)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task