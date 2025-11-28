from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import enum

class TicketStatus(str, enum.Enum):
    NEW = "NEW"
    DIAGNOSTICS = "DIAGNOSTICS"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    WAITING_PARTS = "WAITING_PARTS"
    IN_PROGRESS = "IN_PROGRESS"
    READY_PICKUP = "READY_PICKUP"
    COMPLETED = "COMPLETED"
    WARRANTY_RETURN = "WARRANTY_RETURN"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    assigned_technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String, default=TicketStatus.NEW)
    priority = Column(String, default="Normal")
    
    issue_description = Column(Text, nullable=True)
    diagnostic_notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    customer_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_completion = Column(DateTime, nullable=True)
    actual_completion = Column(DateTime, nullable=True)
    
    customer = relationship("Customer", back_populates="tickets")
    device = relationship("Device", back_populates="tickets")
    location = relationship("Location", back_populates="tickets")
    assigned_technician = relationship("User", foreign_keys=[assigned_technician_id], back_populates="tickets_assigned")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="tickets_created")
    line_items = relationship("TicketLineItem", back_populates="ticket")

class TicketLineItem(Base):
    __tablename__ = "ticket_line_items"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    
    item_type = Column(String, nullable=False) # "SERVICE", "PART", "FEE", "DISCOUNT"
    
    # Optional links
    service_definition_id = Column(Integer, ForeignKey("service_definitions.id"), nullable=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=True)
    
    name = Column(String, nullable=False) # Snapshot of name
    quantity = Column(Integer, default=1)
    unit_cost = Column(Float, default=0.0) # Cost to us
    unit_price = Column(Float, default=0.0) # Price to customer
    
    ticket = relationship("Ticket", back_populates="line_items")
    service_definition = relationship("ServiceDefinition", back_populates="ticket_line_items")
    # part relationship if needed, but usually we just link to Part for cost reference
