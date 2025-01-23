from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47f1020b7b6c'
down_revision = '77bc03590930'
branch_labels = None
depends_on = None


def upgrade():
    # Eliminar la columna asistencias de la tabla eventos
    with op.batch_alter_table('eventos', schema=None) as batch_op:
        batch_op.drop_column('asistencias')


def downgrade():
    # Restaurar la columna asistencias en la tabla eventos
    with op.batch_alter_table('eventos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('asistencias', sa.Integer(), nullable=True))
