"""logistic_mesh_map table

Revision ID: 09daa30de644
Revises: 
Create Date: 2021-04-06 00:05:52.531207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09daa30de644'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logistic_mesh_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mapname', sa.String(length=64), nullable=True),
    sa.Column('routes', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logistic_mesh_map_mapname'), 'logistic_mesh_map', ['mapname'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logistic_mesh_map_mapname'), table_name='logistic_mesh_map')
    op.drop_table('logistic_mesh_map')
    # ### end Alembic commands ###