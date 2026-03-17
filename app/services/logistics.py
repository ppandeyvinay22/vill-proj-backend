"""
Mock Shiprocket Logistics Service

In production, replace the mock functions with real Shiprocket API calls:
  Base URL: https://apiv2.shiprocket.in/v1/external
  Auth: POST /auth/login → bearer token
  Create Shipment: POST /orders/create/adhoc
  Track: GET /courier/track/awb/{awb}

This mock mirrors the exact data contract so swapping is trivial.
"""

import uuid
import random
from datetime import datetime, timedelta

# Simulated courier partners (Shiprocket aggregates these)
COURIER_PARTNERS = [
    {"id": 1, "name": "Delhivery", "etd": "2-4 days", "rate": 49},
    {"id": 2, "name": "DTDC", "etd": "3-5 days", "rate": 39},
    {"id": 3, "name": "Ecom Express", "etd": "3-5 days", "rate": 45},
    {"id": 4, "name": "BlueDart", "etd": "1-3 days", "rate": 69},
]


def create_shipment(order_data: dict) -> dict:
    """
    Simulates Shiprocket POST /orders/create/adhoc

    In production this sends:
      - order_id, order_date
      - billing/shipping address
      - item details, weight, dimensions
      - payment method (prepaid/COD)

    Returns shipment details with AWB, courier, and estimated delivery.
    """
    courier = random.choice(COURIER_PARTNERS)
    awb = f"AWB{uuid.uuid4().hex[:10].upper()}"
    etd_days = int(courier["etd"].split("-")[1].strip().split(" ")[0])

    return {
        "shiprocket_order_id": f"SR-{uuid.uuid4().hex[:8].upper()}",
        "awb_code": awb,
        "courier_company_id": courier["id"],
        "courier_name": courier["name"],
        "freight_charge": courier["rate"],
        "estimated_delivery": (datetime.utcnow() + timedelta(days=etd_days)).isoformat(),
        "status": "PICKUP_SCHEDULED",
        "tracking_url": f"https://shiprocket.co/tracking/{awb}",
        "pickup_scheduled_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }


def track_shipment(awb: str) -> dict:
    """
    Simulates Shiprocket GET /courier/track/awb/{awb}

    Returns tracking events timeline.
    """
    now = datetime.utcnow()
    events = [
        {
            "date": (now - timedelta(hours=random.randint(1, 48))).isoformat(),
            "status": "PICKUP_SCHEDULED",
            "location": "Village Hub Warehouse, Rajasthan",
            "description": "Shipment pickup scheduled"
        },
        {
            "date": (now - timedelta(hours=random.randint(0, 24))).isoformat(),
            "status": "PICKED_UP",
            "location": "Village Hub Warehouse, Rajasthan",
            "description": "Shipment picked up by courier"
        },
        {
            "date": now.isoformat(),
            "status": "IN_TRANSIT",
            "location": "Sorting Facility, Delhi NCR",
            "description": "Shipment in transit"
        }
    ]

    return {
        "awb_code": awb,
        "current_status": "IN_TRANSIT",
        "events": events,
    }


def cancel_shipment(awb: str) -> dict:
    """Simulates shipment cancellation."""
    return {
        "awb_code": awb,
        "status": "CANCELLED",
        "message": "Shipment cancelled successfully"
    }
