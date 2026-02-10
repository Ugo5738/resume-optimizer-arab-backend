"""make_job_description_nullable

Revision ID: b1f2c3d4e5f6
Revises: aee8ffda7711
Create Date: 2026-02-10 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f2c3d4e5f6'
down_revision = 'aee8ffda7711'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('jobs', 'job_description',
                    existing_type=sa.Text(),
                    nullable=True)


def downgrade() -> None:
    op.execute("UPDATE jobs SET job_description = '' WHERE job_description IS NULL")
    op.alter_column('jobs', 'job_description',
                    existing_type=sa.Text(),
                    nullable=False)
