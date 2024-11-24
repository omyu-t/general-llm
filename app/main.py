from fastapi import FastAPI
from app.api.endpoints import infuse

app = FastAPI()

app.include_router(infuse.router)

@app.get("/")
async def health_check():
    return {"message": "Hello, World!"}
