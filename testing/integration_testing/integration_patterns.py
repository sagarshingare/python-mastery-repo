"""Integration testing patterns: Database fixtures, lifecycle management,
transaction isolation, and cross-component workflows.
"""

from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator, Optional

from api_development.authentication.auth_utils import hash_password, verify_password


@dataclass
class UserRecord:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: float


class UserRepository:
    """Data access layer backed by SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection

    def create_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """
        )

    def add_user(self, username: str, email: str, raw_password: str) -> UserRecord:
        pw_hash = hash_password(raw_password)
        now = time.time()
        cursor = self.conn.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, pw_hash, now),
        )
        return UserRecord(
            id=cursor.lastrowid,  # type: ignore[arg-type]
            username=username,
            email=email,
            password_hash=pw_hash,
            created_at=now,
        )

    def get_by_username(self, username: str) -> Optional[UserRecord]:
        cursor = self.conn.execute(
            "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return UserRecord(
            id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            created_at=row[4],
        )


@contextmanager
def db_session_fixture() -> Generator[sqlite3.Connection, None, None]:
    """Integration fixture that provides an isolated in-memory SQLite database.

    Uses autocommit mode (isolation_level=None) so test transactions and savepoints
    can be controlled explicitly without Python sqlite3 auto-commit interference.
    """
    conn = sqlite3.connect(":memory:", isolation_level=None)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def transactional_scope(conn: sqlite3.Connection) -> Generator[sqlite3.Connection, None, None]:
    """Pattern for transaction isolation in integration tests using SQLite SAVEPOINT.

    Rolls back to the savepoint at teardown to preserve a clean state
    without modifying persistent records.
    """
    conn.execute("SAVEPOINT test_isolation;")
    try:
        yield conn
    finally:
        conn.execute("ROLLBACK TO test_isolation;")
        conn.execute("RELEASE test_isolation;")


def test_user_lifecycle_integration() -> None:
    """Integration test verifying repository, hashing, and database queries."""
    with db_session_fixture() as conn:
        repo = UserRepository(conn)
        repo.create_table()

        # Step 1: Create user
        user = repo.add_user("sagar_admin", "sagar@example.com", "SecurePass123!")
        assert user.id is not None
        assert user.username == "sagar_admin"

        # Step 2: Query user
        fetched = repo.get_by_username("sagar_admin")
        assert fetched is not None
        assert fetched.email == "sagar@example.com"

        # Step 3: Verify password integrity via auth module
        assert verify_password("SecurePass123!", fetched.password_hash) is True
        assert verify_password("WrongPassword", fetched.password_hash) is False

        # Step 4: Verify non-existent user returns None
        assert repo.get_by_username("non_existent") is None

    print("✓ Full user lifecycle integration test passed.")


def test_transaction_rollback_isolation() -> None:
    """Integration test verifying transactional isolation pattern."""
    with db_session_fixture() as conn:
        repo = UserRepository(conn)
        repo.create_table()

        # Insert base data outside the isolated test block
        repo.add_user("base_user", "base@example.com", "BasePass")

        # Isolated test transaction
        with transactional_scope(conn):
            repo.add_user("temp_user", "temp@example.com", "TempPass")
            assert repo.get_by_username("temp_user") is not None

        # After rollback, temp_user is gone, base_user remains
        assert repo.get_by_username("temp_user") is None
        assert repo.get_by_username("base_user") is not None

    print("✓ Transactional rollback isolation test passed.")


def run_all() -> None:
    print("\n--- Testing: Integration Testing Patterns ---")
    test_user_lifecycle_integration()
    test_transaction_rollback_isolation()


if __name__ == "__main__":
    run_all()
