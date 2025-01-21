"""Eliminar relación con Asistente

Revision ID: 6477f136ecfd
Revises: c434aae6e18c
Create Date: 2025-01-21 15:01:57.010722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6477f136ecfd'
down_revision = 'c434aae6e18c'
branch_labels = None
depends_on = None


def upgrade():
    # Eliminar primero la tabla dependiente (evento_asistente)
    op.drop_table('evento_asistente')

    # Luego eliminar la tabla principal (asistentes)
    op.drop_table('asistentes')


def downgrade():
    # Restaurar primero la tabla principal (asistentes)
    op.create_table(
        'asistentes',
        sa.Column('id_asistente', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id_asistente', name='asistentes_pkey'),
        sa.UniqueConstraint('email', name='asistentes_email_key')
    )

    # Luego restaurar la tabla dependiente (evento_asistente)
    op.create_table(
        'evento_asistente',
        sa.Column('id_evento', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('id_asistente', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id_asistente'], ['asistentes.id_asistente'], name='evento_asistente_id_asistente_fkey'),
        sa.ForeignKeyConstraint(['id_evento'], ['eventos.id_evento'], name='evento_asistente_id_evento_fkey'),
        sa.PrimaryKeyConstraint('id_evento', 'id_asistente', name='evento_asistente_pkey')
    )
