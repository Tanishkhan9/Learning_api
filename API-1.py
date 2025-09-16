# Import required libraries
from fastapi import FastAPI, HTTPException   # FastAPI framework + error handling
from pydantic import BaseModel              # For request validation and data models
from typing import List                     # For typing hints (list of objects)

# Initialize FastAPI application
app = FastAPI(title="FastAPI Example: Fetch & Request Data")

# In-memory database (just a Python list for now)
# ⚠️ This resets when you restart the app
database = []

# Define a data model using Pydantic
class Item(BaseModel):
    id: int                     # Unique identifier for each item
    name: str                   # Name of the item
    description: str = None      # Optional description field (default: None)

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def home():
    """Root endpoint, just a welcome message"""
    return {"message": "Welcome to FastAPI example API"}

# -------------------------------
# GET: Fetch all items
# -------------------------------
@app.get("/items", response_model=List[Item])
def get_items():
    """Fetch all items from the in-memory database"""
    return database

# -------------------------------
# GET: Fetch a single item by ID
# -------------------------------
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Fetch a single item by ID
    - Loops through database
    - Returns item if found
    - Else raises 404 error
    """
    for item in database:
        if item.id == item_id:   # Match item by ID
            return item
    # If no item found, raise an error
    raise HTTPException(status_code=404, detail="Item not found")

# -------------------------------
# POST: Create a new item
# -------------------------------
@app.post("/items", response_model=Item)
def create_item(item: Item):
    """
    Add a new item to the database
    - Checks for duplicate IDs
    - Appends item to in-memory DB
    """
    # Ensure ID is unique
    for existing in database:
        if existing.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")

    # If ID is unique, add item
    database.append(item)
    return item
