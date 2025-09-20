import random
import string
from fastapi import APIRouter, status
from pydantic import BaseModel
from db import get_database

# Create an APIRouter instance for this endpoint
ep_6 = APIRouter()

# --- Helper Functions to Generate IDs ---
def generate_shipment_id(carrier: str) -> str:
    """Generates a unique shipment ID. Ex: SHP-DEL-123456"""
    carrier_prefix = carrier[:3].upper()
    random_digits = ''.join(random.choices(string.digits, k=6))
    return f"SHP-{carrier_prefix}-{random_digits}"

def generate_tracking_number(carrier: str) -> str:
    """Generates a unique tracking number. Ex: DE123456789IN"""
    carrier_prefix = carrier[:2].upper()
    random_digits = ''.join(random.choices(string.digits, k=9))
    return f"{carrier_prefix}{random_digits}IN"

# --- Pydantic Model for Request Body ---
class CreateShipmentRequest(BaseModel):
    sales_order_id: str
    carrier: str
    shipping_method: str

# --- API Endpoint Definition ---
@ep_6.post("/shipping/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(request: CreateShipmentRequest):
    """
    Triggered after manufacturing is complete. 
    This API arranges for the finished product to be shipped to the customer.
    """
    # Generate unique IDs for the shipment
    shipment_id = generate_shipment_id(request.carrier)
    tracking_number = generate_tracking_number(request.carrier)
    
    # Get database connection and collection
    db = get_database()
    shipments_collection = db['shipments']
    
    # Check if a document with the sales_order_id already exists
    existing_shipment = shipments_collection.find_one({"sales_order_id": request.sales_order_id})
    
    # Prepare the data to be inserted or updated
    shipment_data = {
        "sales_order_id": request.sales_order_id,
        "shipment_id": shipment_id,
        "shipment_inprogress_status": "SHIPPED",
        "Shipment_inprogress_by": "SURYA", # As requested
        "tracking_number": tracking_number,
        # You can also add other details from the request if needed
        "carrier": request.carrier,
        "shipping_method": request.shipping_method
    }

    if existing_shipment:
        # If it exists, update the document
        shipments_collection.update_one(
            {"sales_order_id": request.sales_order_id},
            {"$set": shipment_data}
        )
    else:
        # If not present, create a new document
        shipments_collection.insert_one(shipment_data)
        
    # Return the success response
    return {
        "shipment_id": shipment_id,
        "sales_order_id": request.sales_order_id,
        "status": "SHIPPED",
        "tracking_number": tracking_number
    }