"""Create unique constraint for username in users table

Revision ID: 6ab7a6b6f682
Revises: 22ac5d68869b
Create Date: 2023-11-02 15:33:12.693147

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6ab7a6b6f682"
down_revision = "22ac5d68869b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_user_username", "users", ["username"])


def downgrade() -> None:
    op.drop_constraint("uq_user_username", "users")