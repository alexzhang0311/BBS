"""empty message

Revision ID: 89332c5b82d2
Revises: 0733090335db
Create Date: 2020-09-06 21:43:54.953102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89332c5b82d2'
down_revision = '0733090335db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.String(length=100), nullable=False))
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###
