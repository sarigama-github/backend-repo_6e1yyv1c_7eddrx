import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Item, Rental, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# ------------------- Rental Marketplace API -------------------

@app.post("/api/items", response_model=dict)
def create_item(item: Item):
    """Create a new rentable item"""
    try:
        item_id = create_document("item", item)
        return {"id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/items", response_model=List[dict])
def list_items(q: Optional[str] = None, category: Optional[str] = None):
    """List items with optional search and category filter"""
    try:
        filter_dict = {}
        if category:
            filter_dict["category"] = category
        items = get_documents("item", filter_dict)
        # Basic client-side search on returned docs if q provided
        if q:
            q_lower = q.lower()
            items = [i for i in items if q_lower in i.get("title", "").lower() or q_lower in (i.get("description", "") or "").lower()]
        # stringify _id
        for i in items:
            if i.get("_id"):
                i["_id"] = str(i["_id"])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rentals", response_model=dict)
def request_rental(rental: Rental):
    """Create a rental request"""
    try:
        rental_id = create_document("rental", rental)
        return {"id": rental_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rentals", response_model=List[dict])
def list_rentals(owner_email: Optional[str] = None, renter_email: Optional[str] = None):
    """List rentals filtered by owner or renter"""
    try:
        filter_dict = {}
        if owner_email:
            filter_dict["owner_email"] = owner_email
        if renter_email:
            filter_dict["renter_email"] = renter_email
        rentals = get_documents("rental", filter_dict)
        for r in rentals:
            if r.get("_id"):
                r["_id"] = str(r["_id"])
        return rentals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
