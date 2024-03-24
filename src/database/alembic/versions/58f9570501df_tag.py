"""Tag

Revision ID: 58f9570501df
Revises: 9902d08083dd
Create Date: 2024-03-24 16:10:54.648624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '58f9570501df'
down_revision: Union[str, None] = '9902d08083dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('tag',
                  sa.Column('name', sa.String(), nullable=False),
                  sa.Column('user_id', sa.Integer(), nullable=False),
                  sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                  sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
                  sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                  sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                  sa.PrimaryKeyConstraint('id'))
  op.create_table('note_tag',
                  sa.Column('tag_id', sa.Integer(), nullable=False),
                  sa.Column('note_id', sa.Integer(), nullable=False),
                  sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                  sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
                  sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                  sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
                  sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
                  sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
  op.drop_table('note_tag')
  op.drop_table('tag')
