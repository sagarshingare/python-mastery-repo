# API Development Module

> **Learning Path**: [Stage 08: API Development & Microservices](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-08-api-development--microservices) (Prerequisites: [Stage 01](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python), [Stage 07](file:///Users/sagarshingare/Documents/python-mastery-repo/testing))

Comprehensive guide and production patterns for modern Python web APIs, covering FastAPI, Flask, authentication, JSON Web Tokens (JWT), rate limiting, and observability.

---

## Step-by-Step Learning Sequence

| Step | Subfolder | Focus Area |
|:---|:---|:---|
| **Step 8.1** | [`authentication/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/authentication) | Password hashing (PBKDF2-HMAC-SHA256), timing-safe verify, RBAC |
| **Step 8.2** | [`jwt/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/jwt) | RFC 7519 HMAC-SHA256 tokens, signature verification, expiration checks |
| **Step 8.3** | [`rate_limiting/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/rate_limiting) | Thread-safe Token Bucket & Sliding Window algorithms |
| **Step 8.4** | [`fastapi/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/fastapi) | Production CRUD API, Pydantic v2 schemas, dependency injection, pagination |
| **Step 8.5** | [`flask/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/flask) | Flask application factory, blueprints, JSON error handlers |
| **Step 8.6** | [`production_api/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development/production_api) | Correlation IDs, process timing headers, RFC 7807, health checks |
| **Step 8.7** | Root Runner | `python -m api_development.run_examples` (Live demonstration of all services) |

---

## Architecture Overview

```
api_development/
├── authentication/
│   ├── __init__.py
│   └── auth_utils.py          # Password hashing (PBKDF2), API keys, RBAC
├── fastapi/
│   ├── __init__.py
│   └── crud_api.py            # Production CRUD API, Pydantic v2 schemas, DI
├── flask/
│   ├── __init__.py
│   └── flask_app.py           # Flask factory, blueprints, JSON error handlers
├── jwt/
│   ├── __init__.py
│   └── jwt_handler.py         # RFC 7519 HS256 JWT encoding, verification, exp checks
├── production_api/
│   ├── __init__.py
│   └── production_patterns.py # Correlation IDs, process timing, RFC 7807, health checks
├── rate_limiting/
│   ├── __init__.py
│   └── rate_limiter.py        # Token Bucket & Sliding Window algorithms
├── fastapi_app.py             # Single-file reference FastAPI prediction endpoint
├── run_examples.py            # Comprehensive test runner & demonstration
├── examples.py                # Convenience entry point
└── README.md
```

---

## 1. Authentication & RBAC

Secure password hashing uses standard library PBKDF2-HMAC-SHA256 with cryptographically random 16-byte salts, timing-attack-resistant constant-time digest comparisons via `hmac.compare_digest`.

```python
from api_development.authentication import hash_password, verify_password, Role, require_role

# Hash and verify
hashed = hash_password("secret_pass")
assert verify_password("secret_pass", hashed) is True

# Role-based access control
@require_role(Role.ADMIN)
def admin_only_action(*, user_role: Role):
    return "authorized"
```

---

## 2. JSON Web Tokens (JWT)

Pure Python RFC 7519 implementation using HMAC-SHA256:
- Expiration validation (`exp`)
- Issued-at tracking (`iat`)
- Cryptographic tampering detection (`InvalidSignatureError`)
- Zero external C-extension or third-party package dependencies

```python
from api_development.jwt import encode_jwt, decode_jwt

token = encode_jwt({"sub": "user_123", "role": "admin"}, secret="my-secret", expires_in_seconds=3600)
payload = decode_jwt(token, secret="my-secret")
```

---

## 3. Rate Limiting

Includes two thread-safe rate-limiting algorithms:
1. **Token Bucket (`TokenBucket`)**: Smooth replenishment at a fixed rate, allowing burst capacity.
2. **Sliding Window Log (`SlidingWindowRateLimiter`)**: Accurate per-client rate enforcement without boundary burst issues.

```python
from api_development.rate_limiting import SlidingWindowRateLimiter, TokenBucket

# Max 100 requests per 60-second sliding window
limiter = SlidingWindowRateLimiter(max_requests=100, window_seconds=60.0)
if limiter.is_allowed("client_ip"):
    ...
```

---

## 4. FastAPI Production CRUD

Follows modern FastAPI & Pydantic v2 best practices:
- Type-validated schemas (`BaseModel`, `Field`, `ConfigDict`)
- Automatic OpenAPI documentation
- Structured dependency injection (`Depends(get_repository)`)
- Pagination, status codes, query filtering, and 404 handling

---

## 5. Production Observability Patterns

- **Correlation IDs**: Trace distributed requests across microservices via `X-Correlation-ID`.
- **Latency Monitoring**: Automatic `X-Process-Time-Ms` response header.
- **Problem Details**: RFC 7807 standardized structured JSON error responses.
- **Kubernetes Probes**: `/healthz` (liveness) and `/readyz` (readiness).

---

## Running the Examples

```bash
python -m api_development.run_examples
# or
python -m api_development.examples
```
