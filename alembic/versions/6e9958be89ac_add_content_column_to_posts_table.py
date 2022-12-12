"""add content column to posts table

Revision ID: 6e9958be89ac
Revises: 58ea19e0ca6d
Create Date: 2022-12-11 22:12:14.780854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9958be89ac'
down_revision = '58ea19e0ca6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
