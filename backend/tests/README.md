# Stellecta LucidAI Backend - Test Suite

This directory contains the test suite for the Stellecta LucidAI Multi-LLM Backend.

## Test Structure

```
tests/
├── unit/                       # Unit tests for individual components
│   ├── test_evaluation.py      # Evaluation Service tests
│   ├── test_router.py          # Multi-LLM Router tests
│   ├── test_policies.py        # Routing Policy Engine tests
│   └── test_mentor_engine.py   # Mentor Engine tests
│
├── integration/                # Integration tests for component interactions
│   └── test_supervisor_flow.py # Supervisor Agent flow tests
│
├── e2e/                        # End-to-end tests
│   └── test_chat_endpoint.py   # Chat API E2E tests
│
├── conftest.py                 # Pytest fixtures and configuration
└── README.md                   # This file
```

## Running Tests

### Prerequisites

Ensure you have installed test dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
# From backend directory
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/

# Specific test file
pytest tests/unit/test_evaluation.py

# Specific test class
pytest tests/unit/test_evaluation.py::TestEvaluationService

# Specific test method
pytest tests/unit/test_evaluation.py::TestEvaluationService::test_evaluate_single_returns_all_dimensions
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

### Run with Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only E2E tests
pytest -m e2e

# Run only async tests
pytest -m asyncio

# Exclude slow tests
pytest -m "not slow"
```

### Verbose Output

```bash
# Verbose output with full diffs
pytest -vv

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Test Coverage Goals

### Phase 0 (Current)

- **Unit Tests**: Core components (Evaluation, Router, Policies, Mentor Engine)
- **Integration Tests**: Supervisor Agent flow
- **E2E Tests**: Chat API endpoint
- **Target Coverage**: 70%+

### Future Phases

- Add tests for LVO business logic
- Add tests for H-PEM calculation algorithms
- Add tests for Gamification mechanics
- Add tests for Blockchain integration
- Add tests for Training Data Pipeline
- Performance/load testing
- Security testing

## Writing New Tests

### Test File Naming

- Unit tests: `test_<component>.py` in `tests/unit/`
- Integration tests: `test_<integration_name>.py` in `tests/integration/`
- E2E tests: `test_<endpoint/feature>.py` in `tests/e2e/`

### Test Function Naming

Use descriptive names that explain what is being tested:

```python
# Good
def test_evaluation_service_flags_low_quality_responses():
    pass

# Bad
def test_evaluation():
    pass
```

### Using Fixtures

Common fixtures are defined in `conftest.py`:

```python
import pytest

def test_something(sample_llm_request, sample_student_context):
    # Use fixtures directly as arguments
    assert sample_llm_request.user_message is not None
```

### Async Tests

Mark async tests with `@pytest.mark.asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Mocking

Use `unittest.mock` for mocking:

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch('app.llm.router.MultiLLMRouter._execute_single')
async def test_with_mock(mock_execute):
    mock_execute.return_value = LLMResponse(...)
    # Test logic
```

## Test Database

Tests use an in-memory SQLite database for fast, isolated testing:

```python
# Defined in conftest.py
TEST_DATABASE_URL = "sqlite:///:memory:"
```

Each test function gets a fresh database via the `db_session` fixture.

## Continuous Integration

Tests should pass before committing:

```bash
# Pre-commit check
pytest --cov=app --cov-report=term-missing

# If all tests pass, commit
git add .
git commit -m "Your commit message"
```

## Troubleshooting

### ImportError: No module named 'app'

Ensure you're running pytest from the `backend/` directory:

```bash
cd backend
pytest
```

### Database errors

If you encounter database-related errors, ensure test fixtures are properly used:

```python
def test_database_operation(db_session):
    # Use db_session fixture
    result = db_session.query(Model).all()
```

### Async test warnings

If you see warnings about async tests, ensure you have `pytest-asyncio` installed:

```bash
pip install pytest-asyncio
```

And mark async tests properly:

```python
@pytest.mark.asyncio
async def test_async_operation():
    pass
```

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on other tests
2. **Clear Assertions**: Use clear, specific assertions
3. **Test One Thing**: Each test should test one specific behavior
4. **Use Fixtures**: Reuse common setup code via fixtures
5. **Mock External Services**: Don't call real LLM APIs in tests (use mocks)
6. **Fast Tests**: Keep tests fast (< 1s per test if possible)
7. **Descriptive Names**: Use descriptive test names
8. **Document Complex Tests**: Add docstrings to complex test cases

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
