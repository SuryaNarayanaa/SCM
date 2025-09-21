from datetime import datetime,timezone
import uuid
from db import get_database  # <-- import db directly
from pydantic import BaseModel
from fastapi import APIRouter, status


ep_4=APIRouter()

class BatchRequest(BaseModel):
    purchase_order_id: str
    sales_order_id: str
    status: str
    product_sku: str
    quantity: int

class BatchResponse(BaseModel):
    batch_id: str
    purchase_order_id: str
    sales_order_id: str
    status: str

@ep_4.post("/manufacturing/batches", response_model=BatchResponse, status_code=201)
def create_batch(batch_req: BatchRequest):
    batch_id = start_batch(
        purchase_order_id=batch_req.purchase_order_id,
        sales_order_id=batch_req.sales_order_id
    )

    return BatchResponse(
        batch_id=batch_id,
        purchase_order_id=batch_req.purchase_order_id,
        sales_order_id=batch_req.sales_order_id,
        status="IN_PROGRESS"
    )


def start_batch(purchase_order_id: str, sales_order_id: str) -> str:
    """
    Checks if a document with sales_order_id exists.
    If yes → update it.
    If no → insert a new one.
    Returns the generated batch_id.
    """
    db=get_database()
    collection = db["shipments"]   # <-- use batches collection
    batch_id = f"BATCH-{str(uuid.uuid4())[:8]}"

    existing_doc = collection.find_one({"sales_order_id": sales_order_id})

    if existing_doc:
        collection.update_one(
            {"sales_order_id": sales_order_id},
            {"$set": {
                "sales_order_id": sales_order_id,
                "batch_id": batch_id,
                "batch_mfg_started_status": "IN_PROGRESS",
                "batch_mfg_started_by": "Chandru",
                "batch_mfg_started_time": datetime.now(timezone.utc)
            }}
        )
    else:
        collection.insert_one({
            "sales_order_id": sales_order_id,
            "batch_id": batch_id,
            "batch_mfg_started_status": "IN_PROGRESS",
            "batch_mfg_started_by": "Chandru",
            "batch_mfg_started_time": datetime.now(timezone.utc)
        })

    return batch_id
