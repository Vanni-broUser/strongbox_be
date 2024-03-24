'''Note

Revision ID: da303251e4e6
Revises:
Create Date: 2024-03-23 22:25:02.698001

'''
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'da303251e4e6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('note',
                  sa.Column('content', sa.Text(), nullable=True),
                  sa.Column('title', sa.String(), nullable=False),
                  sa.Column('datetime', sa.DateTime(timezone=True), nullable=True),
                  sa.Column('main', sa.Boolean(), nullable=False),
                  sa.Column('daily', sa.Boolean(), nullable=False),
                  sa.Column('completed', sa.Boolean(), nullable=False),
                  sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                  sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
                  sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                  sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
  op.drop_table('note')
