"""initial

Revision ID: 001
Revises: 
Create Date: 2024-05-06 19:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Создание таблицы пользователей
    op.create_table(
        'tbl_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login')
    )

    # Создание таблицы меток
    op.create_table(
        'tbl_mark',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Создание таблицы тем
    op.create_table(
        'tbl_topic',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['tbl_user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Создание таблицы сообщений
    op.create_table(
        'tbl_message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['topic_id'], ['tbl_topic.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Создание таблицы связи тем и меток
    op.create_table(
        'tbl_topic_mark',
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('mark_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['mark_id'], ['tbl_mark.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['tbl_topic.id'], ),
        sa.PrimaryKeyConstraint('topic_id', 'mark_id')
    )

def downgrade() -> None:
    op.drop_table('tbl_topic_mark')
    op.drop_table('tbl_message')
    op.drop_table('tbl_topic')
    op.drop_table('tbl_mark')
    op.drop_table('tbl_user') 