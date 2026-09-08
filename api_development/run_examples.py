"""Runner for API development examples."""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI
from starlette.testclient import TestClient

from api_development.authentication.auth_utils import (
    Role,
    generate_api_key,
    hash_password,
    require_role,
    verify_api_key,
    verify_password,
)
from api_development.fastapi.crud_api import router as item_router
from api_development.jwt.jwt_handler import (
    InvalidSignatureError,
    TokenExpiredError,
    decode_jwt,
    encode_jwt,
)
from api_development.production_api.production_patterns import (
    register_health_probes,
    register_problem_details_handler,
    setup_production_middleware,
)
from api_development.rate_limiting.rate_limiter import (
    RateLimitExceeded,
    SlidingWindowRateLimiter,
    TokenBucket,
    rate_limit,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def demonstrate_authentication() -> None:
    print("\n--- 1. Authentication & RBAC ---")
    pw = "SuperSecurePassword#2026"
    hashed = hash_password(pw)
    print(f"Hashed password format: {hashed[:35]}...")
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False
    print("Password verification succeeded (constant-time timing attack safe).")

    api_key = generate_api_key()
    print(f"Generated API key: {api_key}")
    assert verify_api_key(api_key, api_key) is True
    assert verify_api_key(api_key, "invalid_key") is False

    @require_role(Role.ADMIN)
    def sensitive_admin_action(*, user_role: Role) -> str:
        return f"Action performed by {user_role.value}"

    print(f"Admin call: {sensitive_admin_action(user_role=Role.ADMIN)}")
    try:
        sensitive_admin_action(user_role=Role.USER)
    except PermissionError as e:
        print(f"RBAC successfully blocked user role: {e}")


def demonstrate_jwt() -> None:
    print("\n--- 2. JSON Web Token (JWT) ---")
    secret = "my-top-secret-signing-key"
    payload = {"sub": "user_42", "email": "dev@example.com", "role": "admin"}

    token = encode_jwt(payload, secret, expires_in_seconds=3600)
    print(f"Generated JWT: {token[:40]}...")

    decoded = decode_jwt(token, secret)
    print(f"Decoded JWT claims: sub={decoded['sub']}, email={decoded['email']}, role={decoded['role']}")
    assert decoded["sub"] == "user_42"

    # Tampering test
    try:
        tampered = token[:-4] + "abcd"
        decode_jwt(tampered, secret)
    except InvalidSignatureError:
        print("Signature tampering successfully detected and rejected.")

    # Expiration test
    expired_token = encode_jwt(payload, secret, expires_in_seconds=-10)
    try:
        decode_jwt(expired_token, secret)
    except TokenExpiredError:
        print("Expired token successfully detected and rejected.")


def demonstrate_rate_limiting() -> None:
    print("\n--- 3. Rate Limiting ---")
    # Token bucket
    bucket = TokenBucket(capacity=3, refill_rate=1.0)
    consumed = [bucket.consume() for _ in range(4)]
    print(f"Token bucket burst 4 requests with capacity 3: {consumed}")
    assert consumed == [True, True, True, False]

    # Sliding window
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=1.0)
    client_a = "client_ip_192.168.1.10"
    assert limiter.is_allowed(client_a) is True
    assert limiter.is_allowed(client_a) is True
    assert limiter.is_allowed(client_a) is False
    print(f"Sliding window (2 req/sec) successfully throttled third request.")


def demonstrate_fastapi_and_production() -> None:
    print("\n--- 4. FastAPI CRUD & Production Middleware ---")
    app = FastAPI(title="Mastery API Demo")
    setup_production_middleware(app)
    register_problem_details_handler(app)
    register_health_probes(app)
    app.include_router(item_router)

    client = TestClient(app)

    # Health check
    res = client.get("/healthz")
    print(f"GET /healthz -> {res.status_code} {res.json()}")
    assert res.status_code == 200
    assert "x-correlation-id" in res.headers
    assert "x-process-time-ms" in res.headers

    # Create item
    create_res = client.post("/items/", json={"title": "Keyboard", "price": 89.99, "category": "electronics"})
    print(f"POST /items/ -> {create_res.status_code} {create_res.json()}")
    assert create_res.status_code == 201
    item_id = create_res.json()["id"]

    # List items
    list_res = client.get("/items/?category=electronics")
    print(f"GET /items/ -> {list_res.status_code} (total={list_res.json()['total']})")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # Delete item
    del_res = client.delete(f"/items/{item_id}")
    print(f"DELETE /items/{item_id} -> {del_res.status_code}")
    assert del_res.status_code == 204


def main() -> None:
    demonstrate_authentication()
    demonstrate_jwt()
    demonstrate_rate_limiting()
    demonstrate_fastapi_and_production()
    print("\nAll API development demonstrations completed successfully!")


if __name__ == "__main__":
    main()
