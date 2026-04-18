"""Add soft delete (deleted_at) and avatar_url to users

Revision ID: a1b2c3d4e5f6
Revises: de6823b62528
Create Date: 2026-04-18 15:29:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "de6823b62528"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add soft-delete column (nullable, no default — non-deleted rows stay NULL)
    op.add_column(
        "users",
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )
    # Add avatar URL column
    op.add_column(
        "users",
        sa.Column("avatar_url", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
    op.drop_column("users", "deleted_at")
