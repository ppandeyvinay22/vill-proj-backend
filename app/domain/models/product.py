from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    category: str
    stock: int = 100

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str = Field(alias="_id")

class ProductInDB(ProductBase):
    id: str = Field(alias="_id")
