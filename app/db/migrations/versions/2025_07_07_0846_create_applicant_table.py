"""Create applicant table

Revision ID: a3b5d9768ffb
Revises: 9d295ba9ba59
Create Date: 2025-07-07 08:46:50.041025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b5d9768ffb'
down_revision: Union[str, Sequence[str], None] = '9d295ba9ba59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applicants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_applicants_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_applicants'))
    )
    op.create_index(op.f('ix_applicants_id'), 'applicants', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_applicants_id'), table_name='applicants')
    op.drop_table('applicants')
    # ### end Alembic commands ###
