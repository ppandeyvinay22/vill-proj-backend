from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_database
from app.domain.models.user import UserResponse
from app.domain.models.address import AddressCreate, AddressResponse
from app.api.deps import get_current_user
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=AddressResponse)
async def create_address(address: AddressCreate, current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    address_data = address.model_dump()
    address_data["user_id"] = current_user.id
    
    if address.is_default:
        await db.addresses.update_many({"user_id": current_user.id}, {"$set": {"is_default": False}})
        
    result = await db.addresses.insert_one(address_data)
    address_data["_id"] = str(result.inserted_id)
    return address_data

@router.get("/", response_model=List[AddressResponse])
async def get_addresses(current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    cursor = db.addresses.find({"user_id": current_user.id})
    addresses = await cursor.to_list(length=10)
    for addr in addresses:
        addr["_id"] = str(addr["_id"])
    return addresses

@router.delete("/{address_id}")
async def delete_address(address_id: str, current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    result = await db.addresses.delete_one({"_id": ObjectId(address_id), "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted"}
