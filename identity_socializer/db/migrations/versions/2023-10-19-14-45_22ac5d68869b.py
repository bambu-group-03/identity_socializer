"""create admin table

Revision ID: 22ac5d68869b
Revises: 847eee4ea866
Create Date: 2023-10-19 14:45:52.775871

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "22ac5d68869b"
down_revision = "847eee4ea866"
branch_labels = None
depends_on = None


def upgrade() -> None:
    length = 200

    op.create_table(
        "admins",
        sa.Column("id", sa.String(length), nullable=False),
        sa.Column("email", sa.String(length), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("admins")
