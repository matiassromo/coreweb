"""Inicializar tablas de la base de datos

Revision ID: be94da348224
Revises: 
Create Date: 2025-01-20 12:49:51.080020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be94da348224'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eventos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True))

    with op.batch_alter_table('organizadores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_registro', sa.DateTime(), server_default=sa.text('now()'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organizadores', schema=None) as batch_op:
        batch_op.drop_column('fecha_registro')

    with op.batch_alter_table('eventos', schema=None) as batch_op:
        batch_op.drop_column('fecha_creacion')

    # ### end Alembic commands ###
