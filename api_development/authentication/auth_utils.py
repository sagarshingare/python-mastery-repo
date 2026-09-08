"""Authentication utilities: secure password hashing, API key verification, and RBAC.

Uses standard library hashlib.pbkdf2_hmac and hmac.compare_digest for constant-time
timing-attack-safe comparisons, requiring zero third-party dependencies.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from enum import Enum
from functools import wraps
from typing import Any, Callable


class Role(str, Enum):
    """User roles for Role-Based Access Control (RBAC)."""

    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


# Role hierarchy weights for comparison
ROLE_HIERARCHY: dict[Role, int] = {
    Role.GUEST: 1,
    Role.USER: 2,
    Role.ADMIN: 3,
    Role.SUPERADMIN: 4,
}


def hash_password(password: str, salt: bytes | None = None, iterations: int = 100_000) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a secure random salt.

    Returns:
        Hex-encoded string formatted as ``salt_hex$iterations$hash_hex``.
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{salt.hex()}${iterations}${pw_hash.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored ``salt$iterations$hash`` string.

    Uses ``hmac.compare_digest`` to prevent timing attacks.
    """
    try:
        salt_hex, iter_str, hash_hex = hashed_password.split("$")
        salt = bytes.fromhex(salt_hex)
        iterations = int(iter_str)
        expected_hash = bytes.fromhex(hash_hex)
    except (ValueError, AttributeError):
        return False

    computed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(computed, expected_hash)


def generate_api_key(prefix: str = "ak_live") -> str:
    """Generate a high-entropy URL-safe API key."""
    return f"{prefix}_{secrets.token_urlsafe(32)}"


def verify_api_key(provided_key: str, expected_key: str) -> bool:
    """Verify an API key using constant-time string comparison."""
    return hmac.compare_digest(provided_key, expected_key)


def has_sufficient_permission(user_role: Role, required_role: Role) -> bool:
    """Check whether a user's role satisfies the required role in hierarchy."""
    user_weight = ROLE_HIERARCHY.get(user_role, 0)
    required_weight = ROLE_HIERARCHY.get(required_role, float("inf"))
    return user_weight >= required_weight


def require_role(required_role: Role) -> Callable[..., Any]:
    """Decorator to enforce minimum role permissions on a function."""

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check for 'current_user' or 'user_role' keyword argument
            user_role = kwargs.get("user_role")
            if user_role is None and "current_user" in kwargs:
                current_user = kwargs["current_user"]
                user_role = getattr(current_user, "role", current_user.get("role") if isinstance(current_user, dict) else None)

            if isinstance(user_role, str):
                try:
                    user_role = Role(user_role)
                except ValueError:
                    raise PermissionError(f"Invalid role: {user_role}")

            if user_role is None or not has_sufficient_permission(user_role, required_role):
                raise PermissionError(
                    f"Access denied: required minimum role '{required_role.value}', got '{user_role}'"
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
