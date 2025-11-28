"""Inventory service for stock management."""
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Part


async def get_low_stock_parts(
    db: AsyncSession,
    company_id: int,
    location_id: Optional[int] = None,
) -> list[Part]:
    """
    Get all parts that are at or below their minimum quantity.

    Args:
        db: Database session
        company_id: Company ID to filter by
        location_id: Optional location ID to filter by

    Returns:
        List of parts with low stock
    """
    query = (
        select(Part)
        .where(
            Part.company_id == company_id,
            Part.is_active == True,
            Part.quantity <= Part.min_quantity,
        )
        .order_by(Part.quantity)
    )

    if location_id:
        query = query.where(Part.location_id == location_id)

    result = await db.execute(query)
    return list(result.scalars().all())


async def adjust_part_quantity(
    db: AsyncSession,
    part: Part,
    adjustment: int,
    commit: bool = True,
) -> Part:
    """
    Adjust a part's quantity.

    Args:
        db: Database session
        part: Part to adjust
        adjustment: Amount to add (positive) or subtract (negative)
        commit: Whether to commit the transaction

    Returns:
        Updated part

    Raises:
        ValueError: If adjustment would result in negative quantity
    """
    new_quantity = part.quantity + adjustment
    if new_quantity < 0:
        raise ValueError(
            f"Cannot adjust quantity to negative. "
            f"Current: {part.quantity}, Adjustment: {adjustment}"
        )

    part.quantity = new_quantity

    if commit:
        await db.commit()
        await db.refresh(part)

    return part


def calculate_reorder_quantity(
    current_quantity: int,
    min_quantity: int,
    target_stock_days: int = 30,
    daily_usage: Optional[Decimal] = None,
) -> int:
    """
    Calculate suggested reorder quantity.

    Args:
        current_quantity: Current stock level
        min_quantity: Minimum stock level
        target_stock_days: Target days of stock to maintain
        daily_usage: Average daily usage (if known)

    Returns:
        Suggested reorder quantity
    """
    if daily_usage is not None and daily_usage > 0:
        # Calculate based on usage
        target_quantity = int(daily_usage * target_stock_days)
        return max(0, target_quantity - current_quantity)

    # Default: reorder to 2x minimum quantity
    target_quantity = min_quantity * 2
    return max(0, target_quantity - current_quantity)
