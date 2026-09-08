"""Production-ready FastAPI CRUD API demonstrating modern Pydantic v2 schemas,
dependency injection, error handling, status codes, and pagination.
"""

from __future__ import annotations

import threading
from typing import Any, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Pydantic v2 Schemas
# ---------------------------------------------------------------------------


class ItemBase(BaseModel):
    """Common attributes for an inventory item."""

    title: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Detailed item description")
    price: float = Field(..., gt=0, description="Unit price in USD")
    category: str = Field("general", min_length=1, max_length=50, description="Category tag")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)


class ItemResponse(ItemBase):
    """Schema for returned items including system-assigned fields."""

    id: str
    created_at_epoch: float

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    """Generic pagination wrapper."""

    total: int
    skip: int
    limit: int
    items: list[ItemResponse]


# ---------------------------------------------------------------------------
# In-Memory Repository
# ---------------------------------------------------------------------------


class ItemRepository:
    """Thread-safe in-memory store for items."""

    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create(self, data: ItemCreate) -> dict[str, Any]:
        import time

        with self._lock:
            item_id = str(uuid4())[:8]
            record = {
                "id": item_id,
                **data.model_dump(),
                "created_at_epoch": time.time(),
            }
            self._items[item_id] = record
            return dict(record)

    def get(self, item_id: str) -> dict[str, Any] | None:
        with self._lock:
            record = self._items.get(item_id)
            return dict(record) if record else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 10,
        category: str | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        with self._lock:
            records = list(self._items.values())
            if category:
                records = [r for r in records if r["category"] == category]
            total = len(records)
            sliced = records[skip : skip + limit]
            return [dict(r) for r in sliced], total

    def update(self, item_id: str, data: ItemUpdate) -> dict[str, Any] | None:
        with self._lock:
            if item_id not in self._items:
                return None
            record = self._items[item_id]
            updates = {k: v for k, v in data.model_dump().items() if v is not None}
            record.update(updates)
            return dict(record)

    def delete(self, item_id: str) -> bool:
        with self._lock:
            if item_id in self._items:
                del self._items[item_id]
                return True
            return False


# Singleton repository instance
_repo = ItemRepository()


def get_repository() -> ItemRepository:
    """FastAPI dependency for accessing the item repository."""
    return _repo


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    repo: ItemRepository = Depends(get_repository),
) -> ItemResponse:
    """Create a new item."""
    record = repo.create(payload)
    return ItemResponse(**record)


@router.get("/", response_model=PaginatedResponse)
def list_items(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
    category: Optional[str] = Query(None, description="Optional category filter"),
    repo: ItemRepository = Depends(get_repository),
) -> PaginatedResponse:
    """List items with pagination and optional category filtering."""
    items_data, total = repo.list_all(skip=skip, limit=limit, category=category)
    items = [ItemResponse(**item) for item in items_data]
    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: str,
    repo: ItemRepository = Depends(get_repository),
) -> ItemResponse:
    """Get a single item by unique ID."""
    record = repo.get(item_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID '{item_id}' not found.",
        )
    return ItemResponse(**record)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str,
    payload: ItemUpdate,
    repo: ItemRepository = Depends(get_repository),
) -> ItemResponse:
    """Update an existing item."""
    record = repo.update(item_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID '{item_id}' not found.",
        )
    return ItemResponse(**record)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_item(
    item_id: str,
    repo: ItemRepository = Depends(get_repository),
) -> Response:
    """Delete an item by ID."""
    deleted = repo.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID '{item_id}' not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
