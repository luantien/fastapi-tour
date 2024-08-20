from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.author import AuthorModel, AuthorViewModel
from services.exception import ResourceNotFoundError
from services import author as AuthorService

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("", response_model=list[AuthorViewModel])
async def get_all_authors(async_db: AsyncSession = Depends(get_async_db_context)):
    return await AuthorService.get_authors(async_db)


@router.get("/{author_id}", status_code=status.HTTP_200_OK, response_model=AuthorViewModel)
async def get_author_by_id(author_id: UUID, db: Session = Depends(get_db_context)):    
    author = AuthorService.get_author_by_id(db, author_id)

    if author is None:
        raise ResourceNotFoundError()

    return author


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AuthorViewModel)
async def create_author(request: AuthorModel, db: Session = Depends(get_db_context)):
    return AuthorService.add_new_author(db, request)


@router.put("/{author_id}", status_code=status.HTTP_200_OK, response_model=AuthorViewModel)
async def update_author(
    author_id: UUID,
    request: AuthorModel,
    db: Session = Depends(get_db_context),
    ):
        return AuthorService.update_author(db, author_id, request)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID, db: Session = Depends(get_db_context)):
    AuthorService.delete_author(db, author_id)
