"""create user table

Revision ID: a2c79e6002c4
Revises: 298754da4bd0
Create Date: 2023-04-13 10:01:32.392241

"""
from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa

from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = 'a2c79e6002c4'
down_revision = '298754da4bd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User Table
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    # Update Book Table
    op.add_column("books", sa.Column("owner_id", sa.UUID, nullable=True))
    op.create_foreign_key("fk_book_owner", "books", "users", ["owner_id"],['id'])

    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "fastapi_tour@sample.com", 
            "username": "fa_admin",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "FastApi",
            "last_name": "Admin",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_column("books", "owner_id")
    # Rollback foreign key
    op.drop_table("users")
