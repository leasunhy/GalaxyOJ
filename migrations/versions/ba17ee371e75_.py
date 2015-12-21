"""add PostTag model.

Revision ID: ba17ee371e75
Revises: f1ae4fab020a
Create Date: 2015-12-21 17:46:00.574194

"""

# revision identifiers, used by Alembic.
revision = 'ba17ee371e75'
down_revision = 'f1ae4fab020a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_tag_rel',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['post_tag.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tag_rel')
    op.drop_table('post_tag')
    ### end Alembic commands ###