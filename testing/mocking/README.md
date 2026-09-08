# Mocking & Isolation

> **Learning Path**: [Stage 07: Testing & Quality Assurance](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-07-testing--quality-assurance) ▸ **Step 7.2: Mocking & Isolation**

Test isolation patterns with `unittest.mock`: `MagicMock`, `patch`, `create_autospec`, side effects, and `AsyncMock`.

## Key Concepts

- **Autospec**: Preventing false positive tests via `create_autospec(..., instance=True)`.
- **Side Effects**: Testing error recovery, retries, and sequential responses.
- **AsyncMock**: Isolating async coroutines and HTTP API calls.

## Quick Start

```bash
python -m testing.mocking.mock_examples
```
