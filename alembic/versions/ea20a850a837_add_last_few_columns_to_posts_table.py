"""add last few columns to posts table

Revision ID: ea20a850a837
Revises: 1569255d80da
Create Date: 2024-09-23 19:56:21.563610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea20a850a837'
down_revision: Union[str, None] = '1569255d80da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False),)
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
