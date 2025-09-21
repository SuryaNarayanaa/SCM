from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_database
from datetime import datetime, timezone

# Create an APIRouter instance for this endpoint
ep_5 = APIRouter()

# --- Pydantic Model for Request Body ---
class UpdateManufacturingRequest(BaseModel):
    sales_order_id: str
    status: str

# --- API Endpoint Definition ---
@ep_5.put("/manufacturing/batches/{batch_id}")
def update_manufacturing_status(batch_id: str, request: UpdateManufacturingRequest):
    """
    Updates the status of an ongoing manufacturing batch, 
    typically to mark it as complete.
    """
    # Basic validation for the incoming status
    if request.status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Only 'COMPLETED' is allowed."
        )

    # Get the current time in UTC
    completion_time = datetime.now(timezone.utc).isoformat()

    # Get database connection and collection
    db = get_database()
    batches_collection = db['shipments'] # Using a descriptive collection name
    
    # Check if a document with the sales_order_id already exists
    existing_batch = batches_collection.find_one({"sales_order_id": request.sales_order_id})
    
    # Prepare the data for the database operation
    batch_data = {
        "sales_order_id": request.sales_order_id,
        "batch_id": batch_id,
        "batch_mfg_completed_status": "COMPLETED",
        "batch_mfg_completed_by": "SURYA", # As requested
        "batch_mfg_completed_time": completion_time
    }

    if existing_batch:
        # If present, update the existing document
        batches_collection.update_one(
            {"sales_order_id": request.sales_order_id},
            {"$set": batch_data}
        )
    else:
        # If not present, create a new document
        batches_collection.insert_one(batch_data)
        
    # Return the success response
    return {
        "sales_order_id": request.sales_order_id,
        "batch_id": batch_id,
        "new_status": "COMPLETED",
        "message": "Product assembly is complete."
    }