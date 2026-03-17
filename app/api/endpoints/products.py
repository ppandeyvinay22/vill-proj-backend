from fastapi import APIRouter, HTTPException, status
from app.core.database import get_database
from app.domain.models.product import ProductResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def get_products():
    db = get_database()
    cursor = db.products.find({})
    products = await cursor.to_list(length=100)
    
    # Optional seeding logic if empty
    if not products:
        seed_data = [
            {
                "name": "Organic Village Honey",
                "description": "Pure, unadulterated honey collected from local village bee hives.",
                "price": 449,
                "image_url": "https://images.pexels.com/photos/1638280/pexels-photo-1638280.jpeg?auto=compress&cs=tinysrgb&w=800",
                "category": "Pantry",
                "stock": 50
            },
            {
                "name": "Hand-Ground Spices Mix",
                "description": "A traditional blend of roasted and ground spices, perfect for curries.",
                "price": 199,
                "image_url": "https://images.pexels.com/photos/2802527/pexels-photo-2802527.jpeg?auto=compress&cs=tinysrgb&w=800",
                "category": "Spices",
                "stock": 100
            },
            {
                "name": "Farm Fresh Desi Ghee",
                "description": "Aromatic, golden clarified butter made using traditional bilona method.",
                "price": 799,
                "image_url": "https://images.pexels.com/photos/4110256/pexels-photo-4110256.jpeg?auto=compress&cs=tinysrgb&w=800",
                "category": "Dairy",
                "stock": 30
            },
            {
                "name": "Organic Jaggery Powder",
                "description": "Natural sweetener made from sugarcane juice, rich in minerals.",
                "price": 149,
                "image_url": "https://images.pexels.com/photos/5946081/pexels-photo-5946081.jpeg?auto=compress&cs=tinysrgb&w=800",
                "category": "Pantry",
                "stock": 80
            },
            {
                "name": "Cold-Pressed Mustard Oil",
                "description": "Traditional kachi ghani mustard oil for authentic cooking flavor.",
                "price": 299,
                "image_url": "https://images.pexels.com/photos/33783/olive-oil-salad-dressing-cooking-olive.jpg?auto=compress&cs=tinysrgb&w=800",
                "category": "Oils",
                "stock": 60
            },
            {
                "name": "Village Turmeric Powder",
                "description": "High-curcumin turmeric, hand-ground from organically grown roots.",
                "price": 179,
                "image_url": "https://images.pexels.com/photos/4198370/pexels-photo-4198370.jpeg?auto=compress&cs=tinysrgb&w=800",
                "category": "Spices",
                "stock": 90
            }
        ]
        await db.products.insert_many(seed_data)
        cursor = db.products.find({})
        products = await cursor.to_list(length=100)

    # Format _id to string for Pydantic
    for prod in products:
        prod["_id"] = str(prod["_id"])
        
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    db = get_database()
    from bson import ObjectId
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Product ID format")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    product["_id"] = str(product["_id"])
    return product
