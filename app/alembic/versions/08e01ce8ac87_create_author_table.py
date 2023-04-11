"""create author table

Revision ID: 08e01ce8ac87
Revises: 
Create Date: 2023-04-11 16:08:31.435890

"""
from alembic import op
import sqlalchemy as sa
from schemas.base_entity import Gender


# revision identifiers, used by Alembic.
revision = '08e01ce8ac87'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'authors',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('gender', sa.Enum(Gender), nullable=False, default=Gender.NONE),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('authors')
    op.execute("DROP TYPE gender;")
