"""Added ubication in users table

Revision ID: 56865ec352df
Revises: 6ab7a6b6f682
Create Date: 2023-11-15 10:38:07.551638

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "56865ec352df"
down_revision = "6ab7a6b6f682"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("ubication", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "ubication")
