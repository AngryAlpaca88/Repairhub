from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ServiceDefinition(Base):
    __tablename__ = "service_definitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    default_price = Column(Float, default=0.0)
    default_duration_minutes = Column(Integer, default=60)
    category = Column(String, nullable=True)
    
    templates = relationship("ServiceTemplate", back_populates="service_definition")
    ticket_line_items = relationship("TicketLineItem", back_populates="service_definition")

class ServiceTemplate(Base):
    __tablename__ = "service_templates"

    id = Column(Integer, primary_key=True, index=True)
    service_definition_id = Column(Integer, ForeignKey("service_definitions.id"), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    quantity_required = Column(Integer, default=1)
    
    service_definition = relationship("ServiceDefinition", back_populates="templates")
    part = relationship("Part", back_populates="service_templates")
