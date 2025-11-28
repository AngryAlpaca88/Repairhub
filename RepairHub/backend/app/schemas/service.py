from typing import Optional
from pydantic import BaseModel

class ServiceDefinitionBase(BaseModel):
    name: str
    default_price: float = 0.0
    default_duration_minutes: int = 60

class ServiceDefinitionCreate(ServiceDefinitionBase):
    pass

class ServiceDefinition(ServiceDefinitionBase):
    id: int

    class Config:
        from_attributes = True
