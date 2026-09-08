# FastAPI Production CRUD

> **Learning Path**: [Stage 08: API Development & Microservices](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-08-api-development--microservices) ▸ **Step 8.4: FastAPI Production CRUD**

Production CRUD REST service using modern FastAPI and Pydantic v2 schemas.

## Key Features

- **Pydantic v2 Models**: `ItemCreate`, `ItemUpdate`, `ItemResponse` using `ConfigDict` and `model_dump()`.
- **Dependency Injection**: Decoupled thread-safe repository access via `Depends(get_repository)`.
- **REST Endpoints**: Full CRUD with status codes (201 Created, 204 No Content, 404 Not Found), query filtering, and pagination.

## Running the Router

```bash
python -m api_development.run_examples
```
