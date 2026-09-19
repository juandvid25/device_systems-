"""fase_6_definir_asociaciones_modelos

Revision ID: e4aae249d75e
Revises: 87d0de98ab70
Create Date: 2026-09-18 15:37:03.247457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4aae249d75e'
down_revision: Union[str, Sequence[str], None] = '87d0de98ab70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
