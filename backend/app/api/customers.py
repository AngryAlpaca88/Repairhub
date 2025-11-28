"""Customers API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models import Customer, User
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: Optional[str] = Query(None, min_length=1),
    skip: int = 0,
    limit: int = 50,
):
    """List customers for the current user's company."""
    query = (
        select(Customer)
        .where(Customer.company_id == current_user.company_id)
        .order_by(Customer.last_name, Customer.first_name)
    )

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Customer.first_name.ilike(search_term),
                Customer.last_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.phone.ilike(search_term),
            )
        )

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific customer by ID."""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.company_id == current_user.company_id,
        )
    )
    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new customer."""
    customer = Customer(
        company_id=current_user.company_id,
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=customer_data.email,
        phone=customer_data.phone,
        address=customer_data.address,
        notes=customer_data.notes,
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a customer."""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.company_id == current_user.company_id,
        )
    )
    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a customer."""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.company_id == current_user.company_id,
        )
    )
    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db.delete(customer)
    await db.commit()
