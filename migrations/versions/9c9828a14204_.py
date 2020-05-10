"""empty message

Revision ID: 9c9828a14204
Revises: 
Create Date: 2020-05-09 18:01:35.497833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9828a14204'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deviceDB',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deviceNum', sa.String(length=20), nullable=True),
    sa.Column('deviceName', sa.String(length=40), nullable=True),
    sa.Column('OnOff', sa.Integer(), nullable=True),
    sa.Column('last_battVolt', sa.Integer(), nullable=True),
    sa.Column('last_rcPeriod', sa.Integer(), nullable=True),
    sa.Column('last_update', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pourDB',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deviceNum', sa.String(length=20), nullable=True),
    sa.Column('deviceName', sa.String(length=40), nullable=True),
    sa.Column('pourVolume', sa.Integer(), nullable=True),
    sa.Column('approxTime', sa.String(length=20), nullable=True),
    sa.Column('commitTime', sa.String(length=20), nullable=True),
    sa.Column('battVolt', sa.Integer(), nullable=True),
    sa.Column('timerCounter', sa.Integer(), nullable=True),
    sa.Column('pourTime', sa.Integer(), nullable=True),
    sa.Column('pulseCount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timeDB',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mon', sa.Integer(), nullable=True),
    sa.Column('tue', sa.Integer(), nullable=True),
    sa.Column('wed', sa.Integer(), nullable=True),
    sa.Column('thu', sa.Integer(), nullable=True),
    sa.Column('fri', sa.Integer(), nullable=True),
    sa.Column('sat', sa.Integer(), nullable=True),
    sa.Column('sun', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timeDB')
    op.drop_table('pourDB')
    op.drop_table('deviceDB')
    # ### end Alembic commands ###
