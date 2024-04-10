"""empty message

Revision ID: 1db0d28196aa
Revises: e801345e7d96
Create Date: 2024-04-10 15:48:55.329790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1db0d28196aa'
down_revision = 'e801345e7d96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=250), nullable=False))
        batch_op.alter_column('full_name',
               existing_type=mysql.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('advisor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=250), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advisor', schema=None) as batch_op:
        batch_op.drop_column('password')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('full_name',
               existing_type=mysql.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('password')

    # ### end Alembic commands ###