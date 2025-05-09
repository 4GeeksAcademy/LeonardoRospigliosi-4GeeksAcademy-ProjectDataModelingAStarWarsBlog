"""empty message

Revision ID: 2eb55236364d
Revises: 12709427f471
Create Date: 2025-04-02 13:10:20.772600

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2eb55236364d'
down_revision = '12709427f471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('edited',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###
