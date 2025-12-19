"""Add role, plan, billing, status columns to account table

Revision ID: 20241218_000001
Revises:
Create Date: 2024-12-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20241218_000001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to account table
    op.add_column('account', sa.Column('role', sa.String(30), nullable=False, server_default='USER'))
    op.add_column('account', sa.Column('plan', sa.String(30), nullable=False, server_default='FREE'))
    op.add_column('account', sa.Column('plan_started_at', sa.DateTime(), nullable=True))
    op.add_column('account', sa.Column('plan_ends_at', sa.DateTime(), nullable=True))
    op.add_column('account', sa.Column('billing_customer_id', sa.String(100), nullable=True))
    op.add_column('account', sa.Column('status', sa.String(30), nullable=False, server_default='ACTIVE'))


def downgrade() -> None:
    # Remove columns from account table
    op.drop_column('account', 'status')
    op.drop_column('account', 'billing_customer_id')
    op.drop_column('account', 'plan_ends_at')
    op.drop_column('account', 'plan_started_at')
    op.drop_column('account', 'plan')
    op.drop_column('account', 'role')
