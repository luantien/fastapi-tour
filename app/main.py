from fastapi import FastAPI
from routers import author, book, user, auth


app = FastAPI()

app.include_router(author.router)
app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
