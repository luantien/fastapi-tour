from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from services.auth import token_interceptor
from database import get_db_context

from schemas import Author, Book, User
from models import BookModel, BookViewModel

router = APIRouter(prefix="/books", tags=["Book"])

@router.get("")
async def get_all_books(
    title: str = Query(default=None),
    author_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)
    )-> List[BookViewModel]:
        # Default of joinedload is LEFT OUTER JOIN
        query = db.query(Book).options(
            joinedload(Book.author, innerjoin=True),
            joinedload(Book.owner))

        if title is not None:
            query = query.filter(Book.title.like(f"{title}%"))
        if author_id is not None:
            query = query.filter(Book.author_id == author_id)
        
        return query.offset((page-1)*size).limit(size).all()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(request: BookModel, 
        user: User = Depends(token_interceptor),
        db: Session=Depends(get_db_context)) -> BookViewModel:
    author = db.query(Author).filter(Author.id == request.author_id).first()
    if author is None:
        raise HTTPException(status_code=422, detail="Invalid author information")
    
    new_book = Book(**request.dict())
    new_book.created_at = datetime.utcnow()

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.get("/{book_id}")
async def get_book_detail(book_id: UUID, db: Session=Depends(get_db_context)) -> BookViewModel:
    return db.query(Book).filter(Book.id == book_id)\
            .options(joinedload(Book.author, innerjoin=True))\
            .first()

@router.put("/{book_id}")
async def update_book(book_id: UUID, request: BookModel, db: Session=Depends(get_db_context)) -> BookViewModel:
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
          raise HTTPException(status_code=404, detail="Item not found")
    
    if book.author_id != request.author_id:
        changed_author = db.query(Author).filter(Author.id == request.author_id).first()
        if changed_author is None:
            raise HTTPException(status_code=422, detail="Invalid author information")
        else:
            book.author_id = request.author_id
    
    book.title = request.title
    book.description = request.description
    book.mode = request.mode
    book.rating = request.rating
    book.updated_at = datetime.utcnow()
            
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book
