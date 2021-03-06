"""empty message

Revision ID: 5e37db731212
Revises: 5cca950067f7
Create Date: 2017-11-02 18:59:24.807616

"""

# revision identifiers, used by Alembic.
revision = '5e37db731212'
down_revision = '5cca950067f7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_index(op.f('ix_requests_request_id'), 'requests', ['request_id'], unique=False)
    op.create_index(op.f('ix_requests_role_id'), 'requests', ['role_id'], unique=False)
    op.create_index(op.f('ix_requests_user_id'), 'requests', ['user_id'], unique=False)
    op.add_column(u'roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column(u'roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_index(op.f('ix_roles_permissions'), 'roles', ['permissions'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_permissions'), table_name='roles')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column(u'roles', 'permissions')
    op.drop_column(u'roles', 'default')
    op.drop_index(op.f('ix_requests_user_id'), table_name='requests')
    op.drop_index(op.f('ix_requests_role_id'), table_name='requests')
    op.drop_index(op.f('ix_requests_request_id'), table_name='requests')
    op.drop_table('requests')
    # ### end Alembic commands ###
