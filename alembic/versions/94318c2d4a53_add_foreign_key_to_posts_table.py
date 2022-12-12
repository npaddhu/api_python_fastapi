"""add foreign-key to posts table

Revision ID: 94318c2d4a53
Revises: 2da48d047bca
Create Date: 2022-12-11 22:38:03.558410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94318c2d4a53'
down_revision = '2da48d047bca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')   
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
