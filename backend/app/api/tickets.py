"""Tickets API endpoints."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.auth import get_current_user
from app.core.config import settings
from app.core.security import UserRole
from app.db.session import get_db
from app.models import AuditLog, Customer, Part, Service, Ticket, TicketPart, TicketService, User
from app.schemas import (
    PricingValidation,
    TicketCreate,
    TicketResponse,
    TicketUpdate,
)
from app.services.pricing import validate_ticket_pricing

router = APIRouter()


def generate_ticket_number() -> str:
    """Generate a unique ticket number."""
    return f"TKT-{uuid.uuid4().hex[:8].upper()}"


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, alias="status"),
    location_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
):
    """List tickets for the current user's company."""
    query = (
        select(Ticket)
        .options(
            selectinload(Ticket.customer),
            selectinload(Ticket.ticket_parts).selectinload(TicketPart.part),
            selectinload(Ticket.ticket_services).selectinload(TicketService.service),
        )
        .where(Ticket.company_id == current_user.company_id)
        .order_by(Ticket.created_at.desc())
    )

    if status_filter:
        query = query.where(Ticket.status == status_filter)

    if location_id:
        query = query.where(Ticket.location_id == location_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific ticket by ID."""
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.customer),
            selectinload(Ticket.ticket_parts).selectinload(TicketPart.part),
            selectinload(Ticket.ticket_services).selectinload(TicketService.service),
        )
        .where(Ticket.id == ticket_id, Ticket.company_id == current_user.company_id)
    )
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new repair ticket."""
    # Verify customer exists and belongs to company
    customer_result = await db.execute(
        select(Customer).where(
            Customer.id == ticket_data.customer_id,
            Customer.company_id == current_user.company_id,
        )
    )
    if customer_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Calculate parts cost and validate pricing
    total_parts_cost = Decimal("0")
    parts_to_add = []

    for part_data in ticket_data.parts:
        part_result = await db.execute(
            select(Part).where(
                Part.id == part_data.part_id,
                Part.company_id == current_user.company_id,
            )
        )
        part = part_result.scalar_one_or_none()
        if part is None:
            raise HTTPException(status_code=404, detail=f"Part {part_data.part_id} not found")

        unit_price = part_data.unit_price if part_data.unit_price is not None else part.price
        parts_to_add.append({
            "part": part,
            "quantity": part_data.quantity,
            "unit_cost": part.cost,
            "unit_price": unit_price,
        })
        total_parts_cost += part.cost * part_data.quantity

    # Calculate services total
    total_services = Decimal("0")
    services_to_add = []

    for service_data in ticket_data.services:
        service_result = await db.execute(
            select(Service).where(
                Service.id == service_data.service_id,
                Service.company_id == current_user.company_id,
            )
        )
        service = service_result.scalar_one_or_none()
        if service is None:
            raise HTTPException(status_code=404, detail=f"Service {service_data.service_id} not found")

        price = service_data.price if service_data.price is not None else service.base_price
        services_to_add.append({
            "service": service,
            "price": price,
        })
        total_services += price

    # Calculate total price
    total_price = total_services + ticket_data.total_labor

    # Add parts pricing
    for part_info in parts_to_add:
        total_price += part_info["unit_price"] * part_info["quantity"]

    # Validate pricing if parts are used
    if parts_to_add:
        pricing_validation = validate_ticket_pricing(
            total_parts_cost=total_parts_cost,
            total_labor=ticket_data.total_labor,
            total_price=total_price,
            minimum_profit=Decimal(str(settings.MINIMUM_PURE_PROFIT)),
        )

        if not pricing_validation.is_valid:
            # Check if user can override
            if not UserRole.can_override_profit(current_user.role):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Pricing violation: {pricing_validation.message}. Minimum profit of ${settings.MINIMUM_PURE_PROFIT} required.",
                )

            # User can override - check if they requested it
            if not ticket_data.profit_override:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Pricing violation: {pricing_validation.message}. Set profit_override=true with a reason to proceed.",
                )

            if not ticket_data.profit_override_reason:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="profit_override_reason is required when overriding profit rules.",
                )

    # Create ticket
    ticket = Ticket(
        company_id=current_user.company_id,
        location_id=ticket_data.location_id,
        customer_id=ticket_data.customer_id,
        assigned_user_id=ticket_data.assigned_user_id,
        ticket_number=generate_ticket_number(),
        device_type=ticket_data.device_type,
        device_brand=ticket_data.device_brand,
        device_model=ticket_data.device_model,
        serial_number=ticket_data.serial_number,
        issue_description=ticket_data.issue_description,
        priority=ticket_data.priority,
        total_parts_cost=total_parts_cost,
        total_labor=ticket_data.total_labor,
        total_price=total_price,
        profit_override=ticket_data.profit_override,
        profit_override_reason=ticket_data.profit_override_reason,
    )
    db.add(ticket)
    await db.flush()

    # Add parts
    for part_info in parts_to_add:
        ticket_part = TicketPart(
            ticket_id=ticket.id,
            part_id=part_info["part"].id,
            quantity=part_info["quantity"],
            unit_cost=part_info["unit_cost"],
            unit_price=part_info["unit_price"],
        )
        db.add(ticket_part)

    # Add services
    for service_info in services_to_add:
        ticket_service = TicketService(
            ticket_id=ticket.id,
            service_id=service_info["service"].id,
            price=service_info["price"],
        )
        db.add(ticket_service)

    # Log profit override if used
    if ticket_data.profit_override:
        audit_log = AuditLog(
            company_id=current_user.company_id,
            user_id=current_user.id,
            action="profit_override",
            entity_type="ticket",
            entity_id=ticket.id,
            new_values={
                "reason": ticket_data.profit_override_reason,
                "total_price": str(total_price),
                "total_parts_cost": str(total_parts_cost),
            },
            notes=f"User {current_user.email} overrode profit rules: {ticket_data.profit_override_reason}",
        )
        db.add(audit_log)

    await db.commit()
    await db.refresh(ticket)

    # Reload with relationships
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.customer),
            selectinload(Ticket.ticket_parts).selectinload(TicketPart.part),
            selectinload(Ticket.ticket_services).selectinload(TicketService.service),
        )
        .where(Ticket.id == ticket.id)
    )
    return result.scalar_one()


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a ticket."""
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.company_id == current_user.company_id,
        )
    )
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update fields
    update_data = ticket_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    await db.commit()
    await db.refresh(ticket)

    # Reload with relationships
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.customer),
            selectinload(Ticket.ticket_parts).selectinload(TicketPart.part),
            selectinload(Ticket.ticket_services).selectinload(TicketService.service),
        )
        .where(Ticket.id == ticket.id)
    )
    return result.scalar_one()


@router.post("/{ticket_id}/validate-pricing", response_model=PricingValidation)
async def validate_pricing(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Validate pricing for a ticket."""
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.ticket_parts))
        .where(
            Ticket.id == ticket_id,
            Ticket.company_id == current_user.company_id,
        )
    )
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return validate_ticket_pricing(
        total_parts_cost=ticket.total_parts_cost,
        total_labor=ticket.total_labor,
        total_price=ticket.total_price,
        minimum_profit=Decimal(str(settings.MINIMUM_PURE_PROFIT)),
    )
