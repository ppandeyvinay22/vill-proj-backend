from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    full_name: str
    address_line: str
    city: str
    state: str
    pincode: str
    phone_number: str
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: str = Field(alias="_id")

class AddressInDB(AddressBase):
    user_id: str
