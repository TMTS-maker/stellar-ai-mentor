"""add_lvo_tables

Revision ID: 72151ecd05f3
Revises:
Create Date: 2025-11-14 15:29:05.170280

Adds all Learn-Verify-Own (LVO) architecture tables:
- Skills and SkillScores (LEARN)
- LearningPaths and LearningModules (LEARN)
- Verifications (VERIFY)
- Credentials and OnChainCredentials (OWN)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '72151ecd05f3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE skillcategory AS ENUM ('language', 'math', 'science', 'social_studies', 'art', 'music', 'physical_education', 'life_skills', 'critical_thinking', 'other')")
    op.execute("CREATE TYPE pathstatus AS ENUM ('not_started', 'in_progress', 'completed', 'paused')")
    op.execute("CREATE TYPE modulestatus AS ENUM ('locked', 'unlocked', 'in_progress', 'completed')")
    op.execute("CREATE TYPE verificationsource AS ENUM ('ai_assessment', 'teacher_review', 'system_check', 'peer_review', 'self_assessment')")
    op.execute("CREATE TYPE verificationstatus AS ENUM ('pending', 'verified', 'rejected', 'expired')")
    op.execute("CREATE TYPE credentialtype AS ENUM ('skill_mastery', 'module_completion', 'path_completion', 'badge_achievement', 'milestone', 'certificate')")
    op.execute("CREATE TYPE credentialstatus AS ENUM ('draft', 'issued', 'minted', 'revoked')")

    # 1. Create skills table
    op.create_table(
        'skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('language', 'math', 'science', 'social_studies', 'art', 'music', 'physical_education', 'life_skills', 'critical_thinking', 'other', name='skillcategory'), nullable=False, index=True),
        sa.Column('level', sa.String(50), nullable=True, index=True),
        sa.Column('age_group_min', sa.Integer(), nullable=True),
        sa.Column('age_group_max', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. Create skill_scores table
    op.create_table(
        'skill_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('score', sa.Float(), nullable=False, default=0.0),
        sa.Column('confidence', sa.Float(), nullable=False, default=0.5),
        sa.Column('assessment_count', sa.Integer(), nullable=False, default=0),
        sa.Column('last_practiced_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 3. Create learning_paths table
    op.create_table(
        'learning_paths',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('recommended_age_min', sa.Integer(), nullable=True),
        sa.Column('recommended_age_max', sa.Integer(), nullable=True),
        sa.Column('estimated_hours', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(50), nullable=True, index=True),
        sa.Column('prerequisites', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 4. Create learning_modules table
    op.create_table(
        'learning_modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('learning_path_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_paths.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False, index=True),
        sa.Column('skill_ids', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('task_ids', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('completion_threshold', sa.Integer(), nullable=False, default=70),
        sa.Column('estimated_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 5. Create student_learning_paths table
    op.create_table(
        'student_learning_paths',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('learning_path_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_paths.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.Enum('not_started', 'in_progress', 'completed', 'paused', name='pathstatus'), nullable=False, default='not_started', index=True),
        sa.Column('progress_percentage', sa.Integer(), nullable=False, default=0),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 6. Create student_modules table
    op.create_table(
        'student_modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('module_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_modules.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.Enum('locked', 'unlocked', 'in_progress', 'completed', name='modulestatus'), nullable=False, default='locked', index=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('tasks_completed', sa.Integer(), nullable=False, default=0),
        sa.Column('tasks_total', sa.Integer(), nullable=False, default=0),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 7. Create verifications table
    op.create_table(
        'verifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('module_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_modules.id', ondelete='SET NULL'), nullable=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('source', sa.Enum('ai_assessment', 'teacher_review', 'system_check', 'peer_review', 'self_assessment', name='verificationsource'), nullable=False, index=True),
        sa.Column('status', sa.Enum('pending', 'verified', 'rejected', 'expired', name='verificationstatus'), nullable=False, default='pending', index=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('evidence', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('verified_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 8. Create credentials table
    op.create_table(
        'credentials',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('credential_type', sa.Enum('skill_mastery', 'module_completion', 'path_completion', 'badge_achievement', 'milestone', 'certificate', name='credentialtype'), nullable=False, index=True),
        sa.Column('status', sa.Enum('draft', 'issued', 'minted', 'revoked', name='credentialstatus'), nullable=False, default='draft', index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='SET NULL'), nullable=True),
        sa.Column('module_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_modules.id', ondelete='SET NULL'), nullable=True),
        sa.Column('learning_path_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_paths.id', ondelete='SET NULL'), nullable=True),
        sa.Column('badge_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('badges.id', ondelete='SET NULL'), nullable=True),
        sa.Column('verification_ids', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('credential_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('issuer_name', sa.String(255), nullable=True),
        sa.Column('issuer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('schools.id', ondelete='SET NULL'), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('issued_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 9. Create on_chain_credentials table
    op.create_table(
        'on_chain_credentials',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('credential_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('credentials.id', ondelete='CASCADE'), nullable=False, unique=True, index=True),
        sa.Column('network', sa.String(100), nullable=False, index=True),
        sa.Column('transaction_hash', sa.String(255), nullable=True, unique=True, index=True),
        sa.Column('contract_address', sa.String(255), nullable=True),
        sa.Column('token_id', sa.String(255), nullable=True),
        sa.Column('owner_wallet_address', sa.String(255), nullable=True, index=True),
        sa.Column('metadata_uri', sa.String(512), nullable=True),
        sa.Column('gas_fee', sa.String(100), nullable=True),
        sa.Column('verification_url', sa.String(512), nullable=True),
        sa.Column('is_simulated', sa.Boolean(), nullable=False, default=True),
        sa.Column('minting_successful', sa.Boolean(), nullable=False, default=False),
        sa.Column('minting_error', sa.Text(), nullable=True),
        sa.Column('minted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 10. Create task_skills association table (many-to-many)
    op.create_table(
        'task_skills',
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('task_skills')
    op.drop_table('on_chain_credentials')
    op.drop_table('credentials')
    op.drop_table('verifications')
    op.drop_table('student_modules')
    op.drop_table('student_learning_paths')
    op.drop_table('learning_modules')
    op.drop_table('learning_paths')
    op.drop_table('skill_scores')
    op.drop_table('skills')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS credentialstatus")
    op.execute("DROP TYPE IF EXISTS credentialtype")
    op.execute("DROP TYPE IF EXISTS verificationstatus")
    op.execute("DROP TYPE IF EXISTS verificationsource")
    op.execute("DROP TYPE IF EXISTS modulestatus")
    op.execute("DROP TYPE IF EXISTS pathstatus")
    op.execute("DROP TYPE IF EXISTS skillcategory")
