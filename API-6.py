from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define input model
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "tanish" and request.password == "12345":
        return {"status": "success", "token": "abc123xyz"}
    return {"status": "error", "message": "Invalid credentials"}
