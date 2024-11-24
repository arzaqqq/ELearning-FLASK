""" for UserModel

Revision ID: 3874f9eb57f0
Revises: 468d6fc5948e
Create Date: 2024-11-22 19:48:06.455157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3874f9eb57f0'
down_revision = '468d6fc5948e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
