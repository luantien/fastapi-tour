"""create book table

Revision ID: 298754da4bd0
Revises: 08e01ce8ac87
Create Date: 2023-04-11 18:16:30.456110

"""
from alembic import op
import sqlalchemy as sa
from schemas.book import BookMode

# revision identifiers, used by Alembic.
revision = '298754da4bd0'
down_revision = '08e01ce8ac87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(BookMode), nullable=False, default=BookMode.DRAFT),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('author_id', sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_book_author', 'books', 'authors', ['author_id'], ['id'])


def downgrade() -> None:
    op.drop_table('books')
    op.execute("DROP TYPE bookmode;")
