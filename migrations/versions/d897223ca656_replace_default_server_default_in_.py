"""replace default->server_default in updated_at

Revision ID: d897223ca656
Revises: 918a8ab713ad
Create Date: 2026-06-30 18:54:43.653620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd897223ca656'
down_revision: Union[str, Sequence[str], None] = '918a8ab713ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'updated_at',
        server_default=sa.text("now()")
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users',
        'updated_at',
        server_default=None
    )
