"""Add rating column to UserFilmLibrary

Revision ID: 42a2ae8ec5b7
Revises: 6524c9c5be60
Create Date: 2025-01-29 16:03:10.869064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42a2ae8ec5b7'
down_revision: Union[str, None] = '6524c9c5be60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_film_library', sa.Column('user_rating', sa.Float(), nullable=True))
    op.drop_index('ix_user_film_library_id', table_name='user_film_library')
    op.drop_column('user_film_library', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_film_library', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_index('ix_user_film_library_id', 'user_film_library', ['id'], unique=False)
    op.drop_column('user_film_library', 'user_rating')
    # ### end Alembic commands ###
