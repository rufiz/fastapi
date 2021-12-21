"""create posts table

Revision ID: 98ff2224a868
Revises: 
Create Date: 2021-12-20 22:44:19.988152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98ff2224a868'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
