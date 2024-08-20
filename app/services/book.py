from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from schemas import Book
from models.book import BookModel, SearchBookModel
from services import author as AuthorService
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError, InvalidInputError


def get_books(db: Session, conds: SearchBookModel) -> List[Book]:
    # Default of joinedload is LEFT OUTER JOIN
    query = select(Book).options(
        joinedload(Book.author, innerjoin=True),
        joinedload(Book.owner))
    
    if conds.title is not None:
        query = query.filter(Book.title.like(f"{conds.title}%"))
    if conds.author_id is not None:
        query = query.filter(Book.author_id == conds.author_id)
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()


def get_book_by_id(db: Session, id: UUID, /, joined_load = False) -> Book:
    query = select(Book).filter(Book.id == id)
    
    if joined_load:
        query.options(joinedload(Book.author, innerjoin=True))
    
    return db.scalars(query).first()
    

def add_new_book(db: Session, data: BookModel) -> Book:
    author = AuthorService.get_author_by_id(db, data.author_id)
        
    if author is None:
        raise InvalidInputError("Invalid author information")

    book = Book(**data.model_dump())
    book.created_at = get_current_utc_time()
    book.updated_at = get_current_utc_time()

    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book

def update_book(db: Session, id: UUID, data: BookModel) -> Book:
    book = get_book_by_id(db, id)

    if book is None:
        raise ResourceNotFoundError()

    if data.author_id != book.author_id:
        author = AuthorService.get_author_by_id(db, data.author_id)
        if author is None:
            raise InvalidInputError("Invalid author information")
    
    book.title = data.title
    book.description = data.description
    book.mode = data.mode
    book.rating = data.rating
    book.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(book)
    
    return book
