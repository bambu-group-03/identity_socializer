"""create relationship table

Revision ID: 6a777ccf275f
Revises: 847eee4ea866
Create Date: 2023-10-15 23:56:33.161484

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6a777ccf275f"
down_revision = "847eee4ea866"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "relationships",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("follower_id", sa.String(), nullable=False),
        sa.Column("following_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["following_id"],
            ["users.id"],
            name=op.f("fk_relationships_following_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name=op.f("fk_relationships_follower_id_users"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("relationships")
