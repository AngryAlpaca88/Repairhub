from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TicketStatus(str, Enum):
    NEW = "NEW"
    DIAGNOSTICS = "DIAGNOSTICS"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    WAITING_PARTS = "WAITING_PARTS"
    IN_PROGRESS = "IN_PROGRESS"
    READY_PICKUP = "READY_PICKUP"
    COMPLETED = "COMPLETED"
    WARRANTY_RETURN = "WARRANTY_RETURN"

class TicketLineItemBase(BaseModel):
    item_type: str
    name: str
    quantity: int = 1
    unit_cost: float = 0.0
    unit_price: float = 0.0
    service_definition_id: Optional[int] = None
    part_id: Optional[int] = None

class TicketLineItemCreate(TicketLineItemBase):
    pass

class TicketLineItem(TicketLineItemBase):
    id: int
    ticket_id: int

    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    status: TicketStatus = TicketStatus.NEW
    priority: str = "Normal"
    issue_description: Optional[str] = None
    diagnostic_notes: Optional[str] = None
    internal_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    estimated_completion: Optional[datetime] = None

class TicketCreate(TicketBase):
    customer_id: int
    device_id: int
    location_id: int
    assigned_technician_id: Optional[int] = None
    line_items: List[TicketLineItemCreate] = []

class TicketUpdate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    customer_id: int
    device_id: int
    location_id: int
    created_by_user_id: int
    created_at: datetime
    line_items: List[TicketLineItem] = []

    class Config:
        from_attributes = True
