"""Add Course populerl

Revision ID: c8e14fd58627
Revises: 0197e2bd66f1
Create Date: 2024-11-23 12:02:08.340240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e14fd58627'
down_revision = '0197e2bd66f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses_populer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.String(length=50), nullable=False),
    sa.Column('price', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses_populer')
    # ### end Alembic commands ###
