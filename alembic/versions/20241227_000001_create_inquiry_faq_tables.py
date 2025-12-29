"""Create inquiry and faq tables

Revision ID: 20241227_000001
Revises: 20241218_000001
Create Date: 2024-12-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20241227_000001'
down_revision: Union[str, None] = '20241218_000001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create inquiry table
    op.create_table(
        'inquiry',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(30), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_inquiry_account_created', 'inquiry', ['account_id', 'created_at'])
    op.create_index('idx_inquiry_status_created', 'inquiry', ['status', 'created_at'])

    # Create inquiry_reply table
    op.create_table(
        'inquiry_reply',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('inquiry_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_admin_reply', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['inquiry_id'], ['inquiry.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_inquiry_reply_inquiry', 'inquiry_reply', ['inquiry_id', 'created_at'])

    # Create faq table
    op.create_table(
        'faq',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('category', sa.String(30), nullable=False),
        sa.Column('question', sa.String(500), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by'], ['account.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_faq_category_order', 'faq', ['category', 'display_order'])
    op.create_index('idx_faq_published', 'faq', ['is_published', 'display_order'])

    # Create fulltext index for search
    op.execute('CREATE FULLTEXT INDEX idx_faq_search ON faq(question, answer)')


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('idx_faq_search', table_name='faq')
    op.drop_index('idx_faq_published', table_name='faq')
    op.drop_index('idx_faq_category_order', table_name='faq')
    op.drop_table('faq')

    op.drop_index('idx_inquiry_reply_inquiry', table_name='inquiry_reply')
    op.drop_table('inquiry_reply')

    op.drop_index('idx_inquiry_status_created', table_name='inquiry')
    op.drop_index('idx_inquiry_account_created', table_name='inquiry')
    op.drop_table('inquiry')
