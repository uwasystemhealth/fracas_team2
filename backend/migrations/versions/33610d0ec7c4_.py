"""empty message

Revision ID: 33610d0ec7c4
Revises: 
Create Date: 2023-09-18 16:00:12.605516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33610d0ec7c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subsystem',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subsystem', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_subsystem')),
    sa.UniqueConstraint('subsystem', name=op.f('uq_subsystem_subsystem'))
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('name', sa.String(length=128), server_default='?', nullable=False),
    sa.Column('inactive', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.Column('leader_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['leader_id'], ['user.id'], name=op.f('fk_team_leader_id_user'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('registered', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.Column('superuser', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_user_team_id_team'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

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
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], name=op.f('fk_record_creator_id_user'), ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['subsystem_id'], ['subsystem.id'], name=op.f('fk_record_subsystem_id_subsystem'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_record'))
    )
    op.create_table('token_blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_token_blacklist_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_token_blacklist'))
    )
    with op.batch_alter_table('token_blacklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_blacklist_jti'), ['jti'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blacklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blacklist_jti'))

    op.drop_table('token_blacklist')
    op.drop_table('record')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('team')
    op.drop_table('subsystem')
    # ### end Alembic commands ###
