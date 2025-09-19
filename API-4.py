from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Advanced FastAPI Example", version="1.0.0")

# Pydantic model for user
class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

# In-memory "database"
users_db = {}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Advanced FastAPI API!"}

# ----------------------------
# GET: Read with path & query
# ----------------------------
@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., description="The ID of the user"),
    details: bool = Query(False, description="Include detailed info?")
):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    if details:
        return {"user": user}
    return {"user": {"id": user.id, "name": user.name}}

# ----------------------------
# POST: Create new user
# ----------------------------
@app.post("/users")
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    users_db[user.id] = user
    return {"message": "User created successfully", "user": user}

# ----------------------------
# PUT: Update existing user
# ----------------------------
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = updated_user
    return {"message": "User updated successfully", "user": updated_user}

# ----------------------------
# DELETE: Remove a user
# ----------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = users_db.pop(user_id)
    return {"message": "User deleted successfully", "user": deleted}
