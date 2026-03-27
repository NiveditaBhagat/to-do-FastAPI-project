"""Create phone number for user column

Revision ID: f390520760f0
Revises: 
Create Date: 2026-03-27 23:18:51.658836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f390520760f0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
