"""Pydantic schemas for API request/response validation."""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============ Auth Schemas ============

class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str


# ============ User Schemas ============

class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., pattern="^(owner|manager|technician|cashier)$")


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    is_active: bool
    created_at: datetime


class UserMeResponse(UserResponse):
    """Current user response with additional details."""

    locations: List["LocationResponse"] = []


# ============ Company Schemas ============

class CompanyBase(BaseModel):
    """Base company schema."""

    name: str = Field(..., min_length=1, max_length=255)


class CompanyCreate(CompanyBase):
    """Company creation schema."""

    pass


class CompanyResponse(CompanyBase):
    """Company response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


# ============ Location Schemas ============

class LocationBase(BaseModel):
    """Base location schema."""

    name: str = Field(..., min_length=1, max_length=255)
    address: Optional[str] = None
    phone: Optional[str] = None


class LocationCreate(LocationBase):
    """Location creation schema."""

    pass


class LocationResponse(LocationBase):
    """Location response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    is_active: bool
    created_at: datetime


# ============ Customer Schemas ============

class CustomerBase(BaseModel):
    """Base customer schema."""

    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Customer creation schema."""

    pass


class CustomerUpdate(BaseModel):
    """Customer update schema."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Customer response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    created_at: datetime


# ============ Part/Inventory Schemas ============

class PartBase(BaseModel):
    """Base part schema."""

    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cost: Decimal = Field(..., ge=0, decimal_places=2)
    price: Decimal = Field(..., ge=0, decimal_places=2)
    quantity: int = Field(default=0, ge=0)
    min_quantity: int = Field(default=0, ge=0)


class PartCreate(PartBase):
    """Part creation schema."""

    location_id: Optional[int] = None


class PartUpdate(BaseModel):
    """Part update schema."""

    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    quantity: Optional[int] = Field(None, ge=0)
    min_quantity: Optional[int] = Field(None, ge=0)
    location_id: Optional[int] = None


class PartResponse(PartBase):
    """Part response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    location_id: Optional[int]
    is_active: bool
    created_at: datetime


# ============ Service Schemas ============

class ServiceBase(BaseModel):
    """Base service schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    base_price: Decimal = Field(..., ge=0, decimal_places=2)


class ServiceCreate(ServiceBase):
    """Service creation schema."""

    pass


class ServiceResponse(ServiceBase):
    """Service response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    is_active: bool
    created_at: datetime


# ============ Ticket Schemas ============

class TicketPartCreate(BaseModel):
    """Ticket part creation schema."""

    part_id: int
    quantity: int = Field(default=1, ge=1)
    unit_price: Optional[Decimal] = None  # Override price if needed


class TicketServiceCreate(BaseModel):
    """Ticket service creation schema."""

    service_id: int
    price: Optional[Decimal] = None  # Override price if needed


class TicketBase(BaseModel):
    """Base ticket schema."""

    device_type: Optional[str] = None
    device_brand: Optional[str] = None
    device_model: Optional[str] = None
    serial_number: Optional[str] = None
    issue_description: str = Field(..., min_length=1)
    priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")


class TicketCreate(TicketBase):
    """Ticket creation schema."""

    location_id: int
    customer_id: int
    assigned_user_id: Optional[int] = None
    parts: List[TicketPartCreate] = []
    services: List[TicketServiceCreate] = []
    total_labor: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    profit_override: bool = False
    profit_override_reason: Optional[str] = None


class TicketUpdate(BaseModel):
    """Ticket update schema."""

    device_type: Optional[str] = None
    device_brand: Optional[str] = None
    device_model: Optional[str] = None
    serial_number: Optional[str] = None
    issue_description: Optional[str] = None
    diagnosis: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(intake|diagnosing|waiting_parts|in_progress|ready|completed|cancelled)$")
    priority: Optional[str] = Field(None, pattern="^(low|normal|high|urgent)$")
    assigned_user_id: Optional[int] = None
    estimated_completion: Optional[datetime] = None
    total_labor: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    profit_override: Optional[bool] = None
    profit_override_reason: Optional[str] = None


class TicketPartResponse(BaseModel):
    """Ticket part response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    part_id: int
    quantity: int
    unit_cost: Decimal
    unit_price: Decimal
    part: Optional[PartResponse] = None


class TicketServiceResponse(BaseModel):
    """Ticket service response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    service_id: int
    price: Decimal
    service: Optional[ServiceResponse] = None


class TicketResponse(TicketBase):
    """Ticket response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    location_id: int
    customer_id: int
    assigned_user_id: Optional[int]
    ticket_number: str
    diagnosis: Optional[str]
    status: str
    estimated_completion: Optional[datetime]
    total_parts_cost: Decimal
    total_labor: Decimal
    total_price: Decimal
    profit_override: bool
    profit_override_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    customer: Optional[CustomerResponse] = None
    ticket_parts: List[TicketPartResponse] = []
    ticket_services: List[TicketServiceResponse] = []


# ============ Pricing Schemas ============

class PricingValidation(BaseModel):
    """Pricing validation response."""

    is_valid: bool
    total_parts_cost: Decimal
    total_labor: Decimal
    total_price: Decimal
    pure_profit: Decimal
    minimum_required_profit: Decimal
    requires_override: bool
    message: Optional[str] = None


# Update forward references
UserMeResponse.model_rebuild()
