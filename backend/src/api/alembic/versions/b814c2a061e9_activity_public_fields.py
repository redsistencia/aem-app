"""Add public activity fields while preserving existing activity data.

Revision ID: b814c2a061e9
Revises: 72fa45b05282
"""
from alembic import op
import sqlalchemy as sa

revision = "b814c2a061e9"
down_revision = "72fa45b05282"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("activities", sa.Column("date", sa.Date(), nullable=True))
    op.add_column("activities", sa.Column("slug", sa.String(), nullable=True))
    op.add_column("activities", sa.Column("image_url", sa.String(), nullable=True))
    op.add_column("activities", sa.Column("sent", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.execute("UPDATE activities SET date = CAST(activity_date AS DATE), slug = 'actividad-' || CAST(id AS VARCHAR)")
    op.execute("UPDATE activities SET description = '' WHERE description IS NULL")
    with op.batch_alter_table("activities") as batch:
        batch.alter_column("date", existing_type=sa.Date(), nullable=False)
        batch.alter_column("slug", existing_type=sa.String(), nullable=False)
        batch.alter_column("title", existing_type=sa.String(30), type_=sa.String(150), existing_nullable=False)
        batch.alter_column("description", existing_type=sa.String(255), type_=sa.String(450), nullable=False)
        batch.alter_column("activity_date", existing_type=sa.TIMESTAMP(), nullable=True)
        batch.create_index("ix_activities_slug", ["slug"], unique=True)


def downgrade() -> None:
    op.execute("UPDATE activities SET activity_date = CAST(date AS TIMESTAMP) WHERE activity_date IS NULL")
    with op.batch_alter_table("activities") as batch:
        batch.drop_index("ix_activities_slug")
        batch.alter_column("activity_date", existing_type=sa.TIMESTAMP(), nullable=False)
        batch.alter_column("title", existing_type=sa.String(150), type_=sa.String(30), existing_nullable=False)
        batch.alter_column("description", existing_type=sa.String(450), type_=sa.String(255), nullable=True)
        batch.drop_column("sent")
        batch.drop_column("image_url")
        batch.drop_column("slug")
        batch.drop_column("date")
