from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.domain.models.user import UserResponse
from app.services import payments as payment_service

router = APIRouter()


class CreatePaymentRequest(BaseModel):
    amount: float
    order_id: str  # our internal order_id


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    internal_order_id: str


@router.post("/create")
async def create_payment(req: CreatePaymentRequest, current_user: UserResponse = Depends(get_current_user)):
    """
    Creates a payment order (Razorpay-style).
    Frontend receives the order_id and opens the payment modal.
    """
    receipt = f"rcpt_{req.order_id}"
    payment_order = payment_service.create_order(req.amount, receipt)
    return payment_order


@router.post("/verify")
async def verify_payment(req: VerifyPaymentRequest, current_user: UserResponse = Depends(get_current_user)):
    """
    Verifies that payment was successful.
    In production, this verifies the Razorpay signature cryptographically.
    """
    from app.core.database import get_database
    
    result = payment_service.verify_payment(
        req.razorpay_order_id,
        req.razorpay_payment_id,
        req.razorpay_signature
    )

    if result["verified"]:
        db = get_database()
        await db.orders.update_one(
            {"_id": req.internal_order_id},
            {"$set": {
                "payment_status": "completed",
                "payment_id": req.razorpay_payment_id,
            }}
        )

    return result
