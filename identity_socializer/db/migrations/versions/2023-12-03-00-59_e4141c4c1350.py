"""Added certified_requests table

Revision ID: e4141c4c1350
Revises: 18ff9184e762
Create Date: 2023-12-03 00:59:23.183303

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e4141c4c1350"
down_revision = "18ff9184e762"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "certified_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("dni", sa.String(), nullable=True),
        sa.Column("img1_url", sa.String(), nullable=True),
        sa.Column("img2_url", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("certified_requests")
