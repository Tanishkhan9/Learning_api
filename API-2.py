# Import required libraries
from fastapi import FastAPI, HTTPException   # FastAPI for API creation + HTTP errors
from pydantic import BaseModel              # For request/response data validation
from typing import List, Optional           # For type hints (list of objects, optional fields)

# Initialize FastAPI app
app = FastAPI(title="Full CRUD API Example", description="A demo FastAPI project", version="1.0.0")

# -------------------------------
# In-memory "database"
# (this will reset every time the app restarts)
# -------------------------------
database = []

# -------------------------------
# Data Model for Items
# -------------------------------
class Item(BaseModel):
    id: int                                # Unique ID of the item
    name: str                              # Name of the item
    description: Optional[str] = None       # Optional description of the item

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def home():
    """Root endpoint: Welcome message"""
    return {"message": "Welcome to Full CRUD FastAPI Example"}

# -------------------------------
# READ: Get all items
# -------------------------------
@app.get("/items", response_model=List[Item])
def get_items():
    """Fetch all items from the database"""
    return database

# -------------------------------
# READ: Get single item by ID
# -------------------------------
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Fetch one item by ID
    - Returns the item if found
    - Raises 404 if not found
    """
    for item in database:
        if item.id == item_id:   # If ID matches, return item
            return item
    # If not found
    raise HTTPException(status_code=404, detail="Item not found")

# -------------------------------
# CREATE: Add new item
# -------------------------------
@app.post("/items", response_model=Item)
def create_item(item: Item):
    """
    Create a new item
    - Checks if ID already exists
    - Adds item to database
    """
    # Prevent duplicate IDs
    for existing in database:
        if existing.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")

    # Add item to in-memory DB
    database.append(item)
    return item

# -------------------------------
# UPDATE: Update item by ID
# -------------------------------
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    """
    Update an existing item by ID
    - If found, replaces old data with new
    - If not found, raises 404
    """
    for index, existing_item in enumerate(database):
        if existing_item.id == item_id:
            # Ensure ID in URL matches ID in request body
            if updated_item.id != item_id:
                raise HTTPException(status_code=400, detail="Item ID in body must match URL ID")
            database[index] = updated_item   # Replace item
            return updated_item

    # If item not found
    raise HTTPException(status_code=404, detail="Item not found")

# -------------------------------
# DELETE: Remove item by ID
# -------------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Delete an item by ID
    - Removes item from database if found
    - If not found, raises 404
    """
    for index, existing_item in enumerate(database):
        if existing_item.id == item_id:
            # Remove from list
            database.pop(index)
            return {"message": f"Item with ID {item_id} deleted successfully"}

    # If not found
    raise HTTPException(status_code=404, detail="Item not found")
