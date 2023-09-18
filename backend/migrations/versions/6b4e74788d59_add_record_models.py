"""add record models

Revision ID: 6b4e74788d59
Revises: 
Create Date: 2023-09-06 02:39:52.041410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b4e74788d59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subsystem',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subsystem', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=192), nullable=True),
    sa.Column('subsystem_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('impact', sa.Text(), nullable=True),
    sa.Column('cause', sa.Text(), nullable=True),
    sa.Column('mechanism', sa.Text(), nullable=True),
    sa.Column('corrective_action_plan', sa.Text(), nullable=True),
    sa.Column('time_of_failure', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('car_year', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['subsystem_id'], ['subsystem.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('record')
    op.drop_table('subsystem')
    # ### end Alembic commands ###