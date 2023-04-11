from fastapi import APIRouter
from book import Book

router = APIRouter(prefix="/books", tags=["Book"])

@router.get("")
async def get_all_books():
    pass
