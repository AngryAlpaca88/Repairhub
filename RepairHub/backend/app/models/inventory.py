from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_name = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    parts = relationship("Part", back_populates="supplier")

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    sku = Column(String, unique=True, index=True, nullable=True)
    cost = Column(Float, default=0.0)
    list_price = Column(Float, default=0.0)
    low_stock_threshold = Column(Integer, default=5)
    
    supplier = relationship("Supplier", back_populates="parts")
    inventory_items = relationship("InventoryItem", back_populates="part")
    service_templates = relationship("ServiceTemplate", back_populates="part")

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    quantity_on_hand = Column(Integer, default=0)
    
    location = relationship("Location", back_populates="inventory_items")
    part = relationship("Part", back_populates="inventory_items")
    
class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    reason = Column(String, nullable=True) # e.g. "ticket_usage", "purchase", "adjustment"
    reference_id = Column(Integer, nullable=True) # e.g. ticket_id
    created_at = Column(DateTime, default=datetime.utcnow)
