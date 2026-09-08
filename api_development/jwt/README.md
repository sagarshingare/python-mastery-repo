# JSON Web Tokens (JWT)

> **Learning Path**: [Stage 08: API Development & Microservices](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-08-api-development--microservices) ▸ **Step 8.2: JSON Web Tokens**

RFC 7519 standard JSON Web Token implementation in pure Python.

## Key Features

- **HS256 Signing & Verification**: Standard HMAC-SHA256 digital signatures with zero external C-extension dependencies.
- **Payload Claims**: Standard `iat` (issued at) and `exp` (expiration timestamp) validation.
- **Tamper Detection**: `InvalidSignatureError` raised upon payload or signature mutation.

## Quick Start

```python
from api_development.jwt import encode_jwt, decode_jwt

token = encode_jwt({"sub": "user_42", "role": "admin"}, secret="secret_key", expires_in_seconds=3600)
claims = decode_jwt(token, secret="secret_key")
assert claims["sub"] == "user_42"
```
