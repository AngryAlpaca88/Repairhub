from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # Future multi-tenant fields can go here

    locations = relationship("Location", back_populates="company")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    timezone = Column(String, default="UTC")
    tax_rate = Column(Integer, default=0) # Stored as basis points or percentage? Let's assume percentage for now or handle in logic.
    
    company = relationship("Company", back_populates="locations")
    users = relationship("User", back_populates="primary_location")
    inventory_items = relationship("InventoryItem", back_populates="location")
    tickets = relationship("Ticket", back_populates="location")
