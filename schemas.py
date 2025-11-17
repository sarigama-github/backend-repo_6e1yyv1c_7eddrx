"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Item(BaseModel):
    """
    Rentable items posted by users
    Collection name: "item"
    """
    title: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Details about the item")
    category: str = Field(..., description="Item category e.g., Tools, Electronics")
    daily_price: float = Field(..., ge=0, description="Daily rental price")
    owner_name: str = Field(..., description="Owner's name")
    owner_email: str = Field(..., description="Owner's contact email")
    location: Optional[str] = Field(None, description="Pickup location")
    images: Optional[List[str]] = Field(default=None, description="Image URLs")

class Rental(BaseModel):
    """
    Rental requests/reservations for items
    Collection name: "rental"
    """
    item_id: str = Field(..., description="ID of the item being rented")
    item_title: str = Field(..., description="Snapshot of the item title at time of request")
    owner_email: str = Field(..., description="Owner's email")
    renter_name: str = Field(..., description="Renter's name")
    renter_email: str = Field(..., description="Renter's email")
    start_date: str = Field(..., description="ISO date string for start date")
    end_date: str = Field(..., description="ISO date string for end date")
    message: Optional[str] = Field(None, description="Optional note from renter")
    status: str = Field("pending", description="Request status: pending|approved|declined")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
