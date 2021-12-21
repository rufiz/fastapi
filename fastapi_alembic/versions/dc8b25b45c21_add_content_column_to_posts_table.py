"""add content column to posts table

Revision ID: dc8b25b45c21
Revises: 98ff2224a868
Create Date: 2021-12-20 22:59:02.407576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc8b25b45c21'
down_revision = '98ff2224a868'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
