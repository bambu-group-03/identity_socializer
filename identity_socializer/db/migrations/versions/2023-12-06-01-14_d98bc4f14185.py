"""add interests in users

Revision ID: d98bc4f14185
Revises: e4141c4c1350
Create Date: 2023-12-06 01:14:15.002499

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d98bc4f14185"
down_revision = "e4141c4c1350"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("interests", sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "interests")
