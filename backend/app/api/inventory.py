"""Inventory API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models import Part, User
from app.schemas import PartCreate, PartResponse, PartUpdate

router = APIRouter()


@router.get("/parts", response_model=List[PartResponse])
async def list_parts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: Optional[str] = Query(None, min_length=1),
    location_id: Optional[int] = None,
    low_stock: bool = False,
    skip: int = 0,
    limit: int = 50,
):
    """List parts/inventory for the current user's company."""
    query = (
        select(Part)
        .where(Part.company_id == current_user.company_id, Part.is_active == True)
        .order_by(Part.name)
    )

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Part.name.ilike(search_term),
                Part.sku.ilike(search_term),
                Part.description.ilike(search_term),
            )
        )

    if location_id:
        query = query.where(Part.location_id == location_id)

    if low_stock:
        query = query.where(Part.quantity <= Part.min_quantity)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/parts/{part_id}", response_model=PartResponse)
async def get_part(
    part_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific part by ID."""
    result = await db.execute(
        select(Part).where(
            Part.id == part_id,
            Part.company_id == current_user.company_id,
        )
    )
    part = result.scalar_one_or_none()

    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    return part


@router.post("/parts", response_model=PartResponse, status_code=status.HTTP_201_CREATED)
async def create_part(
    part_data: PartCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new part/inventory item."""
    # Check for duplicate SKU
    existing = await db.execute(
        select(Part).where(
            Part.sku == part_data.sku,
            Part.company_id == current_user.company_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Part with SKU '{part_data.sku}' already exists",
        )

    part = Part(
        company_id=current_user.company_id,
        location_id=part_data.location_id,
        sku=part_data.sku,
        name=part_data.name,
        description=part_data.description,
        cost=part_data.cost,
        price=part_data.price,
        quantity=part_data.quantity,
        min_quantity=part_data.min_quantity,
    )
    db.add(part)
    await db.commit()
    await db.refresh(part)
    return part


@router.patch("/parts/{part_id}", response_model=PartResponse)
async def update_part(
    part_id: int,
    part_data: PartUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a part."""
    result = await db.execute(
        select(Part).where(
            Part.id == part_id,
            Part.company_id == current_user.company_id,
        )
    )
    part = result.scalar_one_or_none()

    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    # Check SKU uniqueness if changing
    update_data = part_data.model_dump(exclude_unset=True)
    if "sku" in update_data and update_data["sku"] != part.sku:
        existing = await db.execute(
            select(Part).where(
                Part.sku == update_data["sku"],
                Part.company_id == current_user.company_id,
                Part.id != part_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Part with SKU '{update_data['sku']}' already exists",
            )

    for field, value in update_data.items():
        setattr(part, field, value)

    await db.commit()
    await db.refresh(part)
    return part


@router.delete("/parts/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part(
    part_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a part (set is_active to False)."""
    result = await db.execute(
        select(Part).where(
            Part.id == part_id,
            Part.company_id == current_user.company_id,
        )
    )
    part = result.scalar_one_or_none()

    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    part.is_active = False
    await db.commit()


@router.post("/parts/{part_id}/adjust-quantity", response_model=PartResponse)
async def adjust_quantity(
    part_id: int,
    adjustment: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Adjust part quantity (positive to add, negative to subtract)."""
    result = await db.execute(
        select(Part).where(
            Part.id == part_id,
            Part.company_id == current_user.company_id,
        )
    )
    part = result.scalar_one_or_none()

    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    new_quantity = part.quantity + adjustment
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reduce quantity below 0. Current: {part.quantity}, Adjustment: {adjustment}",
        )

    part.quantity = new_quantity
    await db.commit()
    await db.refresh(part)
    return part
