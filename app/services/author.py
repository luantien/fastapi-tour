from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models import AuthorModel
from schemas import Author
from services.exception import ResourceNotFoundError


async def get_authors(async_db: AsyncSession) -> list[Author]:
    result = await async_db.scalars(select(Author).order_by(Author.created_at))
    
    return result.all()

def get_author_by_id(db: Session, author_id: UUID) -> Author:
    return db.scalars(select(Author).filter(Author.id == author_id)).first()

def add_new_author(db: Session, data: AuthorModel) -> Author:
    author = Author(**data.model_dump())

    author.created_at = utils.get_current_utc_time()
    author.updated_at = utils.get_current_utc_time()
    
    db.add(author)
    db.commit()
    db.refresh(author)
    
    return author

def update_author(db: Session, id: UUID, data: AuthorModel) -> Author:
    author = get_author_by_id(db, id)

    if author is None:
        raise ResourceNotFoundError()
    
    author.full_name = data.full_name
    author.gender = data.gender
    author.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(author)

    return author

def delete_author(db: Session, id: UUID) -> None:
    author = get_author_by_id(db, id)

    if author is None:
        raise ResourceNotFoundError()
    
    db.delete(author)
    db.commit()
