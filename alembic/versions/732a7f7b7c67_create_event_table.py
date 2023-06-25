"""create event table

Revision ID: 732a7f7b7c67
Revises: 
Create Date: 2023-06-24 12:17:54.884318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '732a7f7b7c67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'events',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(50)),
        sa.Column('reason', sa.String(100)),
        sa.Column('event_data', sa.String(256)),
        sa.Column('created_at', sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('events')
