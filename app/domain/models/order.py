from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from app.domain.models.cart import CartItemResponse
from app.domain.models.address import AddressBase

class OrderBase(BaseModel):
    items: List[CartItemResponse]
    total_price: float
    address: AddressBase
    status: str = "pending"
    payment_status: str = "pending"
    logistics_provider: str = "Delhivery"
    tracking_id: Optional[str] = None
    shiprocket_order_id: Optional[str] = None
    tracking_url: Optional[str] = None
    estimated_delivery: Optional[str] = None
    shipment_status: Optional[str] = None
    freight_charge: Optional[float] = None
    payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"extra": "ignore"}

class OrderCreate(BaseModel):
    address_id: str

class OrderResponse(OrderBase):
    id: str = Field(alias="_id")
