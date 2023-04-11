from fastapi import FastAPI
from routers import author


app = FastAPI()

app.include_router(author.router)

@app.get("/")
async def health_check():
    return "API Service is up and running!"
