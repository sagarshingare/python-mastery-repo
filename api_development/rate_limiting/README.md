# Rate Limiting

> **Learning Path**: [Stage 08: API Development & Microservices](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-08-api-development--microservices) ▸ **Step 8.3: Rate Limiting**

Thread-safe Token Bucket and Sliding Window rate limiting algorithms for API endpoints and gateways.

## Key Algorithms

- **`TokenBucket`**: Burst-tolerant token consumption with continuous rate replenishment.
- **`SlidingWindowRateLimiter`**: Sliding timestamp log preventing boundary-burst traffic spikes.
- **`@rate_limit`**: Python function decorator with configurable key extraction and retry calculations.

## Quick Start

```python
from api_development.rate_limiting import SlidingWindowRateLimiter, TokenBucket

bucket = TokenBucket(capacity=10, refill_rate=2.0)
if bucket.consume():
    # Process request
    pass
```
