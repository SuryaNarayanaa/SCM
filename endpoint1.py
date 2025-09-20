from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from fastapi import APIRouter, status
import os
from db import get_database
from dotenv import load_dotenv
import uuid

ep_1 = APIRouter()

# Load environment variables


# Request schema
class OrderItem(BaseModel):
    product_sku: str
    quantity: int

class OrderRequest(BaseModel):
    customer_id: str
    items: list[OrderItem]
    shipping_address: str

# API route: Create order
@ep_1.post("/orders", status_code=201)
def create_order(order: OrderRequest):
    # Generate sales order ID
    db = get_database()
    collection = db['shipments']
    sales_order_id = f"ORD-MTO-{uuid.uuid4().hex[:6].upper()}"

    # Check if already exists
    existing_order = collection.find_one({"sales_order_id": sales_order_id})

    if existing_order:
        # Update existing
        collection.update_one(
            {"sales_order_id": sales_order_id},
            {"$set": {
                "customer_order_created_status": "ACCEPTED",
                "customer_order_created_by": "Vijaya Varshini",  # <-- your name
                "customer_order_created_time": datetime.utcnow()
            }}
        )
    else:
        # Insert new order
        new_order = {
            "sales_order_id": sales_order_id,
            "customer_id": order.customer_id,
            "items": [item.dict() for item in order.items],
            "shipping_address": order.shipping_address,
            "customer_order_created_status": "ACCEPTED",
            "customer_order_created_by": "Vijaya Varshini",  # <-- your name
            "customer_order_created_time": datetime.utcnow()
        }
        collection.insert_one(new_order)

    return {
        "sales_order_id": sales_order_id,
        "status": "ACCEPTED",
        "message": "Your order has been accepted and is pending production."
    }

