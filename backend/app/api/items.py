"""
Example CRUD API - Items.
This demonstrates the pattern for database-backed endpoints.
Replace or extend this for your own models.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.db.models import Item

router = APIRouter(prefix="/items", tags=["items"])


# --- Schemas ---


class ItemCreate(BaseModel):
    """Schema for creating an item."""

    name: str
    description: str | None = None


class ItemResponse(BaseModel):
    """Schema for item responses."""

    id: int
    name: str
    description: str | None

    model_config = {"from_attributes": True}


# --- Endpoints ---


@router.get("", response_model=list[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[Item]:
    """List all items with pagination."""
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return list(result.scalars().all())


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
) -> Item:
    """Create a new item."""
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    await db.flush()
    await db.refresh(db_item)
    return db_item


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Item:
    """Get a specific item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete an item."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
