"""
Mock Razorpay Payment Service

In production, replace with real Razorpay SDK:
  pip install razorpay
  import razorpay
  client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
  order = client.order.create({"amount": 50000, "currency": "INR"})

This mock mirrors the real Razorpay data contract.
"""

import uuid
import time


def create_order(amount_inr: float, receipt: str) -> dict:
    """
    Simulates Razorpay POST /v1/orders

    In production:
      client.order.create({
          "amount": amount * 100,  # Razorpay uses paise
          "currency": "INR",
          "receipt": receipt,
      })
    """
    return {
        "id": f"order_{uuid.uuid4().hex[:16]}",
        "entity": "order",
        "amount": int(amount_inr * 100),  # paise
        "amount_paid": 0,
        "amount_due": int(amount_inr * 100),
        "currency": "INR",
        "receipt": receipt,
        "status": "created",
        "created_at": int(time.time()),
    }


def verify_payment(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> dict:
    """
    Simulates Razorpay Payment Verification

    In production:
      client.utility.verify_payment_signature({
          'razorpay_order_id': order_id,
          'razorpay_payment_id': payment_id,
          'razorpay_signature': signature
      })

    For the mock, we always return success.
    """
    return {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "status": "captured",
        "method": "upi",  # or card, netbanking
        "verified": True,
    }


def create_refund(payment_id: str, amount: float) -> dict:
    """Simulates Razorpay refund."""
    return {
        "id": f"rfnd_{uuid.uuid4().hex[:16]}",
        "payment_id": payment_id,
        "amount": int(amount * 100),
        "currency": "INR",
        "status": "processed",
    }
