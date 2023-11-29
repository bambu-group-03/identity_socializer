"""create pushtoken table

Revision ID: ed0c0284f370
Revises: 10115e2a0ca3
Create Date: 2023-11-28 22:19:44.321195

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ed0c0284f370"
down_revision = "10115e2a0ca3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pushtokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("pushtoken", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_unique_constraint(
        "uq_user_push_token",
        "pushtokens",
        ["user_id", "pushtoken"],
    )


def downgrade() -> None:
    op.drop_table("pushtokens")
