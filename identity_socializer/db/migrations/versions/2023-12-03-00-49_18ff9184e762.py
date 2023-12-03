"""Added certified in users table

Revision ID: 18ff9184e762
Revises: ed0c0284f370
Create Date: 2023-12-03 00:49:10.111619

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "18ff9184e762"
down_revision = "ed0c0284f370"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("certified", sa.Boolean(), default=False))
    op.execute("UPDATE users SET certified = FALSE")


def downgrade() -> None:
    op.drop_column("users", "certified")
