"""Agregada columna id_evento y relación en asistentes

Revision ID: f2498fb3eed3
Revises: b6089801167e
Create Date: 2025-01-20 16:43:35.974621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2498fb3eed3'
down_revision = 'b6089801167e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evento_asistente',
    sa.Column('id_evento', sa.Integer(), nullable=False),
    sa.Column('id_asistente', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_asistente'], ['asistentes.id_asistente'], ),
    sa.ForeignKeyConstraint(['id_evento'], ['eventos.id_evento'], ),
    sa.PrimaryKeyConstraint('id_evento', 'id_asistente')
    )
    with op.batch_alter_table('asistentes', schema=None) as batch_op:
        batch_op.drop_column('id_evento')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('asistentes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_evento', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))

    op.drop_table('evento_asistente')
    # ### end Alembic commands ###
