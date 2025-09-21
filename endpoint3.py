from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

app = FastAPI()

# MongoDB connection
MONGO_URI = "mongodb+srv://deepa:deepu8%40KM@cluster0.pgqv2i8.mongodb.net/teamdb?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["teamdb"]
collection = db["shipments"]

# ---------- MODELS ----------
class PartsArrivalRequest(BaseModel):
    purchase_order_id: str
    sales_order_id: str
    received_by: str

# ---------- ROUTE ----------
@app.post("/procurement/arrivals")
def log_parts_arrival(request: PartsArrivalRequest):
    # Check if sales_order_id exists
    existing_doc = collection.find_one({"sales_order_id": request.sales_order_id})
    
    now = datetime.utcnow()
    
    if existing_doc:
        # Update existing doc
        collection.update_one(
            {"sales_order_id": request.sales_order_id},
            {"$set": {
                "purchase_order_id": request.purchase_order_id,
                "purchase_order_received_status": "PARTS_RECEIVED",
                "purchase_order_received_by": "Sruthi A",
                "purchase_order_received_time": now
            }}
        )
    else:
        # Insert new doc
        new_doc = {
            "sales_order_id": request.sales_order_id,
            "purchase_order_id": request.purchase_order_id,
            "purchase_order_received_status": "PARTS_RECEIVED",
            "purchase_order_received_by": "Sruthi A",
            "purchase_order_received_time": now
        }
        collection.insert_one(new_doc)
    
    # Success response
    return {
        "purchase_order_id": request.purchase_order_id,
        "sales_order_id": request.sales_order_id,
        "status": "PARTS_RECEIVED",
        "received_by": request.received_by,
        "message": "Parts received and ready for manufacturing."
    }