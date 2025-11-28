from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    REGIONAL_MANAGER = "REGIONAL_MANAGER"
    STORE_MANAGER = "STORE_MANAGER"
    TECHNICIAN = "TECHNICIAN"
    CASHIER = "CASHIER"
    VIEWER = "VIEWER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    role = Column(String, default=UserRole.TECHNICIAN) # Storing enum as string for simplicity
    
    # Foreign Keys
    primary_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    
    # Relationships
    primary_location = relationship("Location", back_populates="users")
    tickets_assigned = relationship("Ticket", back_populates="assigned_technician")
    tickets_created = relationship("Ticket", back_populates="created_by_user")
