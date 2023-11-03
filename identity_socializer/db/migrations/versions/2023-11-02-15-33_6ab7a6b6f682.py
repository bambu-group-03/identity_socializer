"""Create unique constraint for username and followers

Revision ID: 6ab7a6b6f682
Revises: 22ac5d68869b
Create Date: 2023-11-02 15:33:12.693147

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "6ab7a6b6f682"
down_revision = "22ac5d68869b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_user_username", "users", ["username"])
    op.create_unique_constraint(
        "uq_follower_following",
        "relationships",
        ["follower_id", "following_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_user_username", "users")
    op.drop_constraint("uq_follower_following", "relationships")
