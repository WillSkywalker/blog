"""empty message

Revision ID: 44e23f9db77f
Revises: None
Create Date: 2016-04-22 13:30:09.617093

"""

# revision identifiers, used by Alembic.
revision = '44e23f9db77f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=64), nullable=True),
    sa.Column('subtitle', sa.Unicode(length=64), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('viewcount', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('content'),
    sa.UniqueConstraint('title')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tagname', sa.Unicode(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('of_article', sa.Integer(), nullable=True),
    sa.Column('name', sa.Unicode(length=32), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('md5', sa.String(length=32), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['of_article'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('content'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('md5')
    )
    op.create_table('tag_table',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_table')
    op.drop_table('comments')
    op.drop_table('tags')
    op.drop_table('articles')
    ### end Alembic commands ###
