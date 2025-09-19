from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI()

# Define a route at the root web address ("/")
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# POST endpoint at /greet
@app.post("/greet")
def greet_user(name: str="Tanish"):
    return {"message": "Hello, " + name + "!"}
