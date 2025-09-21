from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_database
from datetime import datetime, timezone

# Create an APIRouter instance for this endpoint
ep_2 = APIRouter()

# ---------- DATABASE ----------
db=get_database()
orders_collection = db["orders_accepted"]   # Use same collection as Task 1

# ---------- MODELS ----------
class PurchaseOrderRequest(BaseModel):
    sales_order_id: str

# ---------- HELPER ----------
def generate_purchase_order_id():
    count = orders_collection.count_documents({})
    return f"PO-{datetime.now().year}-{count+1:03d}"

# ---------- ROUTE ----------
@ep_2.post("/procurement/orders")
def create_purchase_order(order: PurchaseOrderRequest):
    purchase_order_id = generate_purchase_order_id()
    now = datetime.utcnow()

    # Check if sales_order_id exists in orders_accepted
    existing_doc = orders_collection.find_one({"sales_order_id": order.sales_order_id})

    if existing_doc:
        # Update existing document with purchase order info
        orders_collection.update_one(
            {"sales_order_id": order.sales_order_id},
            {"$set": {
                "purchase_order_id": purchase_order_id,
                "purchase_order_created_status": "PARTS_ORDERED",
                "purchase_order_created_by": "Your Name",
                "purchase_order_created_time": now
            }}
        )
    else:
        # Create new document if sales_order_id not found
        new_doc = {
            "sales_order_id": order.sales_order_id,
            "purchase_order_id": purchase_order_id,
            "purchase_order_created_status": "PARTS_ORDERED",
            "purchase_order_created_by": "Your Name",
            "purchase_order_created_time": now
        }
        orders_collection.insert_one(new_doc)

    return {
        "purchase_order_id": purchase_order_id,
        "sales_order_id": order.sales_order_id,
        "status": "PARTS_ORDERED"
    }
