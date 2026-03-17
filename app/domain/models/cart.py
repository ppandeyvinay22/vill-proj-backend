from pydantic import BaseModel, Field
from typing import List

class CartItemBase(BaseModel):
    product_id: str
    quantity: int

class CartItemResponse(CartItemBase):
    name: str
    price: float
    image_url: str

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_price: float

class UpdateCartRequest(BaseModel):
    items: List[CartItemBase]
