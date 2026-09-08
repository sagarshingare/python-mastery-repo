"""RFC 7519 JSON Web Token (JWT) implementation using pure Python and standard library.

Supports HS256 (HMAC-SHA256) signature verification, payload expiration (exp),
issued-at timestamps (iat), and base64url encoding/decoding without external dependencies.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any


class JWTError(Exception):
    """Base exception for JWT processing errors."""


class TokenExpiredError(JWTError):
    """Raised when the token expiration timestamp (exp) is in the past."""


class InvalidSignatureError(JWTError):
    """Raised when token signature verification fails."""


class DecodeError(JWTError):
    """Raised when the token format is invalid or cannot be decoded."""


def _base64url_encode(data: bytes) -> str:
    """Encode bytes into base64url string without trailing '=' padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data_str: str) -> bytes:
    """Decode base64url string, adding back '=' padding if necessary."""
    padding = 4 - (len(data_str) % 4)
    if padding != 4:
        data_str += "=" * padding
    try:
        return base64.urlsafe_b64decode(data_str.encode("ascii"))
    except Exception as exc:
        raise DecodeError(f"Invalid base64url data: {exc}") from exc


def encode_jwt(
    payload: dict[str, Any],
    secret: str,
    algorithm: str = "HS256",
    expires_in_seconds: int = 3600,
) -> str:
    """Encode a dictionary payload into a signed JWT token string.

    Args:
        payload: Custom claims to store in token.
        secret: Secret key used for signing.
        algorithm: Hashing algorithm (defaults to 'HS256').
        expires_in_seconds: Token lifetime from creation time in seconds.

    Returns:
        Formatted JWT string: ``header.payload.signature``
    """
    if algorithm != "HS256":
        raise NotImplementedError(f"Algorithm '{algorithm}' is not supported. Use 'HS256'.")

    now = int(time.time())
    full_payload = {
        "iat": now,
        "exp": now + expires_in_seconds,
        **payload,
    }

    header = {
        "alg": algorithm,
        "typ": "JWT",
    }

    header_bytes = json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_bytes = json.dumps(full_payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    header_b64 = _base64url_encode(header_bytes)
    payload_b64 = _base64url_encode(payload_bytes)

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_jwt(
    token: str,
    secret: str,
    verify_expiration: bool = True,
    leeway_seconds: int = 0,
) -> dict[str, Any]:
    """Decode and verify a signed JWT token string.

    Args:
        token: Full JWT string (header.payload.signature).
        secret: Secret key used for signing.
        verify_expiration: If True, validate that ``exp`` has not elapsed.
        leeway_seconds: Clock skew leeway allowance in seconds.

    Returns:
        Decoded payload dictionary.

    Raises:
        DecodeError: If token structure is invalid.
        InvalidSignatureError: If token signature does not match secret.
        TokenExpiredError: If token has expired.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise DecodeError("JWT token must consist of exactly 3 parts separated by dots.")

    header_b64, payload_b64, signature_b64 = parts

    # Verify signature
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_sig = _base64url_decode(signature_b64)

    if not hmac.compare_digest(actual_sig, expected_sig):
        raise InvalidSignatureError("Signature verification failed: token signature is invalid.")

    # Parse payload
    try:
        payload_bytes = _base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        raise DecodeError(f"Could not deserialize payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise DecodeError("Decoded payload must be a JSON object.")

    # Verify expiration
    if verify_expiration and "exp" in payload:
        now = time.time()
        exp = payload["exp"]
        if not isinstance(exp, (int, float)):
            raise DecodeError("'exp' claim must be a number.")
        if now > (exp + leeway_seconds):
            raise TokenExpiredError(f"Token has expired: exp={exp}, now={int(now)}")

    return payload
