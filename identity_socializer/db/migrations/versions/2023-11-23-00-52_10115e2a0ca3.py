"""Added logger table

Revision ID: 10115e2a0ca3
Revises: 56865ec352df
Create Date: 2023-11-23 00:52:33.084105

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "10115e2a0ca3"
down_revision = "56865ec352df"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "logger",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("event", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("logger")
