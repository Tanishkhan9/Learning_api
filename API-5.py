import uvicorn
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def index():
    return {"message":"Hello Tanish"}

if __name__=="__main__":
    uvicorn.run("app:app",host="127.0.0.1",port=8000,reload=True)
