from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_database
from app.domain.models.user import UserResponse
from app.domain.models.cart import UpdateCartRequest, CartResponse, CartItemResponse
from app.api.deps import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    cart = await db.carts.find_one({"user_id": current_user.id})
    
    if not cart:
        return CartResponse(items=[], total_price=0.0)
        
    # We have cart items, let's fetch product details
    items_response = []
    total_price = 0.0
    
    for item in cart.get("items", []):
        try:
            product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
            if product:
                price = product.get("price", 0.0)
                quantity = item["quantity"]
                items_response.append(CartItemResponse(
                    product_id=str(product["_id"]),
                    quantity=quantity,
                    name=product.get("name", "Unknown"),
                    price=price,
                    image_url=product.get("image_url", "")
                ))
                total_price += price * quantity
        except Exception:
            continue
            
    return CartResponse(items=items_response, total_price=total_price)

@router.post("/sync", response_model=CartResponse)
async def sync_cart(request: UpdateCartRequest, current_user: UserResponse = Depends(get_current_user)):
    db = get_database()
    
    cart_data = {
        "user_id": current_user.id,
        "items": [item.model_dump() for item in request.items]
    }
    
    await db.carts.update_one(
        {"user_id": current_user.id},
        {"$set": cart_data},
        upsert=True
    )
    
    # Return updated cart
    return await get_cart(current_user)
