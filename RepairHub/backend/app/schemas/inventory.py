from typing import Optional
from pydantic import BaseModel

class PartBase(BaseModel):
    name: str
    sku: Optional[str] = None
    cost: float = 0.0
    list_price: float = 0.0

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True
