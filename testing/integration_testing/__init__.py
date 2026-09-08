"""Integration testing package."""

from testing.integration_testing.integration_patterns import (
    UserRecord,
    UserRepository,
    db_session_fixture,
    run_all,
    test_transaction_rollback_isolation,
    test_user_lifecycle_integration,
    transactional_scope,
)

__all__ = [
    "UserRepository",
    "UserRecord",
    "db_session_fixture",
    "transactional_scope",
    "test_user_lifecycle_integration",
    "test_transaction_rollback_isolation",
    "run_all",
]
