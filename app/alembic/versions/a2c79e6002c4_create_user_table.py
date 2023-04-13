"""create user table

Revision ID: a2c79e6002c4
Revises: 298754da4bd0
Create Date: 2023-04-13 10:01:32.392241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c79e6002c4'
down_revision = '298754da4bd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User Table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=False, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False)
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    # Update Book Table
    op.add_column("books", sa.Column("owner_id", sa.UUID, nullable=False))
    op.create_foreign_key("fk_book_owner", "books", "users", ["owner_id"],['id'])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_column("books", "owner_id")
    # Rollback foreign key
    op.drop_table("users")
