# Authentication & RBAC

> **Learning Path**: [Stage 08: API Development & Microservices](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-08-api-development--microservices) ▸ **Step 8.1: Authentication & RBAC**

Secure password hashing, API key generation, and Role-Based Access Control (RBAC).

## Key Features

- **PBKDF2-HMAC-SHA256**: Cryptographically salted password hashing using standard library `hashlib`.
- **Timing-Attack Resistance**: `hmac.compare_digest` for constant-time hash and API key verification.
- **RBAC Decorators**: `@require_role(Role.ADMIN)` hierarchy validation.

## Quick Start

```python
from api_development.authentication import hash_password, verify_password, Role, require_role

hashed = hash_password("my_secret_pass")
assert verify_password("my_secret_pass", hashed) is True
```
