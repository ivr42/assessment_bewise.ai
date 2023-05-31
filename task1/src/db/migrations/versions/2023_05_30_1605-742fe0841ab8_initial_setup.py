"""Initial setup

Revision ID: 742fe0841ab8
Revises:
Create Date: 2023-05-30 16:05:38.949401

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "742fe0841ab8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "question",
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("question", sa.TEXT(), nullable=False),
        sa.Column("answer", sa.TEXT(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("question")
    # ### end Alembic commands ###