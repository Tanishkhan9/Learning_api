from fastapi import FastAPI 
app = FastAPI() 
@app.get("/hello/{name}/{age}") 
async def hello(name,age):
     return {"name": name, "age":age}
