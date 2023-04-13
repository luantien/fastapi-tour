from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, get_db_context
from sqlalchemy.orm import Session
from starlette import status
from schemas.author import Author
from models.author import AuthorModel, AuthorViewModel

router = APIRouter(prefix="/authors", tags=["Author"])

def http_exception():
    return HTTPException(status_code=404, detail="Item not found")

@router.get("", response_model=list[AuthorViewModel])
async def get_all_authors(db: Session = Depends(get_db_context)):
    return db.query(Author).all()

@router.get("/{author_id}")
async def get_author_by_id(author_id: UUID, db: Session = Depends(get_db_context))-> AuthorViewModel:
    author = db.query(Author)\
                    .filter(Author.id == author_id)\
                    .first()
    if author is not None:
        return author
    raise http_exception()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(request: AuthorModel, db: Session = Depends(get_db_context)) -> None:
    author = Author(**request.dict())
    author.created_at = datetime.utcnow()

    db.add(author)
    db.commit()


@router.put("/{author_id}")
async def update_author(author_id: UUID, request: AuthorModel, db: Session = Depends(get_db_context)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise http_exception()
    author.full_name = request.full_name
    author.gender = request.gender
    author.updated_at = datetime.utcnow()
    
    db.add(author)
    db.commit()
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID, db: Session = Depends(get_db_context)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise http_exception()
    
    db.delete(author)
    db.commit()
