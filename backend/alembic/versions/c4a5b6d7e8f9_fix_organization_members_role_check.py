"""fix organization_members role check constraint

Revision ID: c4a5b6d7e8f9
Revises: 7e06c488df90
Create Date: 2026-08-04 13:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a5b6d7e8f9'
down_revision: Union[str, Sequence[str], None] = '7e06c488df90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "DO $$ BEGIN CREATE TYPE role AS ENUM ('ADMIN', 'MANAGER', 'EDITOR', 'VIEWER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "ALTER TABLE organization_members DROP CONSTRAINT IF EXISTS organization_members_role_check"
    )
    op.execute(
        "ALTER TABLE organization_members ALTER COLUMN role TYPE role USING role::role"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE organization_members ALTER COLUMN role TYPE VARCHAR(20) USING role::text"
    )
    op.execute(
        "ALTER TABLE organization_members ADD CONSTRAINT organization_members_role_check CHECK (role IN ('ADMIN', 'MANAGER', 'EDITOR', 'VIEWER'))"
    )
    op.execute("DROP TYPE IF EXISTS role")
