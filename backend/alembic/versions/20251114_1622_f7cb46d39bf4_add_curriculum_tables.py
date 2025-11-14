"""add_curriculum_tables

Revision ID: f7cb46d39bf4
Revises: 72151ecd05f3
Create Date: 2025-11-14 16:22:00.000000

Adds curriculum and content ingestion tables:
- learning_resources (content from multiple sources)
- resource_skills (many-to-many association with skills)
- ResourceType and SourceType enums
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f7cb46d39bf4'
down_revision: Union[str, None] = '72151ecd05f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types for curriculum resources
    op.execute("""
        CREATE TYPE resourcetype AS ENUM (
            'text', 'video', 'pdf', 'interactive_exercise', 'quiz',
            'external_link', 'audio', 'image', 'worksheet', 'game'
        )
    """)

    op.execute("""
        CREATE TYPE sourcetype AS ENUM (
            'school_internal', 'teacher_uploaded', 'intel_input',
            'public_open_content', 'stellar_ai_generated', 'third_party_api'
        )
    """)

    # Create learning_resources table
    op.create_table(
        'learning_resources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),

        # Basic information
        sa.Column('title', sa.String(500), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),

        # Resource type and location
        sa.Column('resource_type', sa.Enum(
            'text', 'video', 'pdf', 'interactive_exercise', 'quiz',
            'external_link', 'audio', 'image', 'worksheet', 'game',
            name='resourcetype'
        ), nullable=False, index=True),
        sa.Column('url', sa.String(1000), nullable=True),
        sa.Column('file_path', sa.String(1000), nullable=True),

        # Content metadata
        sa.Column('language', sa.String(10), nullable=False, server_default='en', index=True),
        sa.Column('subject', sa.String(100), nullable=True, index=True),

        # Age/grade appropriateness
        sa.Column('grade_min', sa.Integer(), nullable=True),
        sa.Column('grade_max', sa.Integer(), nullable=True),
        sa.Column('age_min', sa.Integer(), nullable=True),
        sa.Column('age_max', sa.Integer(), nullable=True),

        # Time estimate
        sa.Column('estimated_minutes', sa.Integer(), nullable=True),

        # Source information
        sa.Column('source_type', sa.Enum(
            'school_internal', 'teacher_uploaded', 'intel_input',
            'public_open_content', 'stellar_ai_generated', 'third_party_api',
            name='sourcetype'
        ), nullable=False, index=True),
        sa.Column('source_attribution', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(1000), nullable=True),
        sa.Column('license_type', sa.String(100), nullable=True),

        # Who created/uploaded this resource
        sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('school_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('schools.id', ondelete='CASCADE'), nullable=True, index=True),

        # Status and visibility
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true', index=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'),

        # Quality and engagement metrics
        sa.Column('difficulty_level', sa.String(50), nullable=True),
        sa.Column('quality_score', sa.Integer(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completion_count', sa.Integer(), nullable=False, server_default='0'),

        # Additional metadata (flexible JSON for custom fields)
        sa.Column('resource_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )

    # Create resource_skills association table (many-to-many)
    op.create_table(
        'resource_skills',
        sa.Column('resource_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('learning_resources.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
    )

    # Create additional indexes for performance
    op.create_index('ix_learning_resources_created_by_user_id', 'learning_resources', ['created_by_user_id'])
    op.create_index('ix_learning_resources_quality_score', 'learning_resources', ['quality_score'])
    op.create_index('ix_learning_resources_grade_range', 'learning_resources', ['grade_min', 'grade_max'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_learning_resources_grade_range', 'learning_resources')
    op.drop_index('ix_learning_resources_quality_score', 'learning_resources')
    op.drop_index('ix_learning_resources_created_by_user_id', 'learning_resources')

    # Drop tables in reverse order
    op.drop_table('resource_skills')
    op.drop_table('learning_resources')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS sourcetype")
    op.execute("DROP TYPE IF EXISTS resourcetype")
