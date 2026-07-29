"""add is_deleted

Revision ID: cf7ba6c01ccb
Revises: 
Create Date: 2026-07-29 14:16:25.969540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf7ba6c01ccb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'todos',
        sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False)
    )


def downgrade() -> None:
   p.drop_column('todos', 'is_deleted')
