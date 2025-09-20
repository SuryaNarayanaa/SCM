from fastapi import APIRouter
from pydantic import BaseModel
from db import get_database

ep_7 = APIRouter()

class UpdateShipmentRequest(BaseModel):
    sales_order_id: str
    status: str
    delivered_at: str

@ep_7.put("/shipping/shipments/{shipment_id}")
def update_shipment(shipment_id: str, request: UpdateShipmentRequest):
    if request.status != "DELIVERED":
        return {"error": "Invalid status"}
    
    db = get_database()
    shipments_collection = db['shipments']
    
    existing = shipments_collection.find_one({"sales_order_id": request.sales_order_id})
    
    if existing:
        shipments_collection.update_one(
            {"sales_order_id": request.sales_order_id},
            {"$set": {
                "sales_order_id": request.sales_order_id,
                "shipment_id": shipment_id,
                "shipment_final_status": "DELIVERED",
                "shipment_final_by": "SURYA"
            }}
        )
    else:
        shipments_collection.insert_one({
            "sales_order_id": request.sales_order_id,
            "shipment_id": shipment_id,
            "shipment_final_status": "DELIVERED",
            "shipment_final_by": "SURYA"
        })
    
    return {
        "sales_order_id": request.sales_order_id,
        "final_status": "DELIVERED",
        "message": "Order delivery confirmed."
    }