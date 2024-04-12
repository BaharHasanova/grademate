"""empty message

Revision ID: d7fa1987c05a
Revises: 0298f5cbf29a
Create Date: 2024-04-11 16:01:47.837326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7fa1987c05a'
down_revision = '0298f5cbf29a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.alter_column('max_grade',
               existing_type=mysql.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.alter_column('max_grade',
               existing_type=sa.Integer(),
               type_=mysql.FLOAT(),
               existing_nullable=True)

    # ### end Alembic commands ###