from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_database
from app.domain.models.user import UserResponse
from app.domain.models.order import OrderCreate, OrderResponse
from app.api.deps import get_current_user
from app.api.endpoints.cart import get_cart
from app.services import logistics as logistics_service
from bson import ObjectId
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(order_in: OrderCreate, current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    
    # 1. Get current cart
    cart = await get_cart(current_user)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
        
    # 2. Get address
    address = await db.addresses.find_one({"_id": ObjectId(order_in.address_id), "user_id": current_user.id})
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    address.pop("_id")
    
    # 3. Create order
    new_order = {
        "user_id": current_user.id,
        "items": [item.model_dump() for item in cart.items],
        "total_price": cart.total_price,
        "address": address,
        "status": "confirmed",
        "payment_status": "completed",
        "created_at": datetime.utcnow(),
    }
    
    # 4. Call Logistics Service (Shiprocket-style) to create shipment
    shipment = logistics_service.create_shipment(new_order)
    new_order["logistics_provider"] = shipment["courier_name"]
    new_order["tracking_id"] = shipment["awb_code"]
    new_order["shiprocket_order_id"] = shipment["shiprocket_order_id"]
    new_order["tracking_url"] = shipment["tracking_url"]
    new_order["estimated_delivery"] = shipment["estimated_delivery"]
    new_order["shipment_status"] = shipment["status"]
    new_order["freight_charge"] = shipment["freight_charge"]
    
    result = await db.orders.insert_one(new_order)
    
    # 5. Clear cart
    await db.carts.delete_one({"user_id": current_user.id})
    
    new_order["_id"] = str(result.inserted_id)
    return new_order

@router.get("/", response_model=List[OrderResponse])
async def get_orders(current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    cursor = db.orders.find({"user_id": current_user.id}).sort("created_at", -1)
    orders = await cursor.to_list(length=50)
    for order in orders:
        order["_id"] = str(order["_id"])
    return orders

@router.get("/{order_id}/track")
async def track_order(order_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Track shipment via logistics service."""
    db = get_database()
    order = await db.orders.find_one({"_id": ObjectId(order_id), "user_id": current_user.id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not order.get("tracking_id"):
        raise HTTPException(status_code=400, detail="No tracking info available")
    
    tracking = logistics_service.track_shipment(order["tracking_id"])
    return tracking
