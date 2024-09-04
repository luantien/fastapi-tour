from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserClaims
from entities.book import OwnerSource
from services import book as BookService
from services.exception import *
from models import BookModel, BookViewModel, SearchBookModel
from services.auth import CognitoAuthorizer, authorizer

router = APIRouter(prefix="/books", tags=["Books"])

# This is a mock data for testing
# BOOKS = [{"id": i, "name": f"Book {i}", "author": f"Author {i%3 + 1}"} for i in range(1, 11)]

@router.get("", status_code=status.HTTP_200_OK, response_model=List[BookViewModel])
async def get_all_books(
    title: str = Query(default=None),
    author_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    user: UserClaims = Depends(authorizer),
    ):
        conds = SearchBookModel(title, author_id, page, size)
        return BookService.get_books(db, conds)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookViewModel)
async def create_book(
    request: BookModel, 
    db: Session = Depends(get_db_context),
    user: UserClaims = Depends(authorizer),
    ):  
        if not user.is_staff:
            raise AccessDeniedError()

        request.owner_id = UUID(user.sub)
        if (isinstance(authorizer, CognitoAuthorizer)):
            request.owner_source = OwnerSource.COGNITO

        return BookService.add_new_book(db, request)

@router.get("/{book_id}", response_model=BookViewModel)
async def get_book_detail(book_id: UUID, db: Session=Depends(get_db_context)):
    book = BookService.get_book_by_id(db, book_id, joined_load=True)
    
    if book is None:
        raise ResourceNotFoundError()

    return book


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookViewModel)
async def update_book(
    book_id: UUID,
    request: BookModel,
    db: Session=Depends(get_db_context),
    ):
        return BookService.update_book(db, book_id, request)
