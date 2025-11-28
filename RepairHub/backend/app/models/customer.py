from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, index=True, nullable=True)
    notes = Column(Text, nullable=True)
    is_vip = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    marketing_opt_in = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    devices = relationship("Device", back_populates="customer")
    tickets = relationship("Ticket", back_populates="customer")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    brand = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    color = Column(String, nullable=True)
    imei_serial = Column(String, index=True, nullable=True)
    notes = Column(Text, nullable=True)
    
    customer = relationship("Customer", back_populates="devices")
    tickets = relationship("Ticket", back_populates="device")
