"""User

Revision ID: 9902d08083dd
Revises: da303251e4e6
Create Date: 2024-03-23 22:41:38.145380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9902d08083dd'
down_revision: Union[str, None] = 'da303251e4e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('user',
                  sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                  sa.Column('mail', sa.String(), nullable=False),
                  sa.Column('name', sa.String(), nullable=False),
                  sa.Column('password', sa.String(), nullable=True),
                  sa.Column('pass_token', sa.String(), nullable=True),
                  sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
                  sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                  sa.PrimaryKeyConstraint('id'))

  op.execute(
    """
    INSERT INTO "user" (mail, name, password, pass_token, created_at, updated_at)
    VALUES ('colasanto.giovanni.inf@gmail.com', 'Vanni', null, null, now(), now())
    """
  )
  op.add_column('note', sa.Column('user_id', sa.Integer(), nullable=True))
  op.execute(
    """
    UPDATE note SET user_id =
    (SELECT id FROM "user" WHERE mail = 'colasanto.giovanni.inf@gmail.com')
    """
  )
  op.alter_column('note', 'user_id', nullable=False)
  op.create_foreign_key(None, 'note', 'user', ['user_id'], ['id'])


def downgrade() -> None:
  op.drop_constraint(None, 'note', type_='foreignkey')
  op.drop_column('note', 'user_id')
  op.drop_table('user')
