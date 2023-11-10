"""Initial revision

Revision ID: 9c55c882b3ab
Revises: 
Create Date: 2023-09-02 17:07:33.408735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = '9c55c882b3ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('postponed_films', ARRAY(sa.JSON(), dimensions=2), nullable=False),
        sa.Column('planned_films', ARRAY(sa.JSON(), dimensions=2), nullable=False),
        sa.Column('abandoned_films', ARRAY(sa.JSON(), dimensions=2), nullable=False),
        sa.Column('finished_films', ARRAY(sa.JSON(), dimensions=2), nullable=False),
        sa.Column('favorite_films', ARRAY(sa.JSON(), dimensions=2), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('refresh_token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(op.f('ix_refresh_tokens_id'), 'refresh_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_refresh_tokens_refresh_token'), 'refresh_tokens', ['refresh_token'], unique=False)
    op.create_table('films',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False, unique=True),
        sa.Column('poster', sa.String(), nullable=False, unique=True),
        sa.Column('trailer', sa.String(), nullable=True, unique=True),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('genres', sa.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('director', sa.String(), nullable=True),
        sa.Column('writers', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('producers', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('cinematographers', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('composers', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('art_directors', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('editor', sa.ARRAY(sa.String()), server_default='{}'),
        sa.Column('budget', sa.String(), nullable=True),
        sa.Column('box_office_world', sa.String(), nullable=True),
        sa.Column('premiere_russia', sa.String()),
        sa.Column('premiere_world', sa.String(), nullable=False),
        sa.Column('age_rating', sa.String(), nullable=True),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('local_rating', sa.Float(), nullable=False, server_default='0'),
        sa.Column('is_planned', sa.Boolean(), server_default="False"),
        sa.Column('is_abandoned', sa.Boolean(), server_default="False"),
        sa.Column('is_favorite', sa.Boolean(), server_default="False"),
        sa.Column('is_postponed', sa.Boolean(), server_default="False"),
        sa.Column('is_finished', sa.Boolean(), server_default="False"),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('film_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('attitude', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('liked_by_users', ARRAY(sa.String()), nullable=False),
        sa.Column('disliked_by_users', ARRAY(sa.String()), nullable=False),
        sa.Column('review_rating', sa.Integer(), nullable=False, server_default='0'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('comments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('film_id', sa.Integer(), nullable=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    )
    
    op.create_table('user_film_ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('film_id', sa.Integer(), nullable=False),   
        sa.Column('rating', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ondelete='CASCADE'),        
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('reply_comments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('comment_id', sa.String(), nullable=False),
        sa.Column('parent_comment_id', sa.String(), nullable=True),
        sa.Column('parent_review_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_review_id'], ['reviews.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_refresh_tokens_refresh_token'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_id'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('reply_comments')
    op.drop_table('reviews')
    op.drop_table('comments')
    op.drop_table('user_film_ratings')
    op.drop_table('users')
    op.drop_table('films')
    # ### end Alembic commands ###
