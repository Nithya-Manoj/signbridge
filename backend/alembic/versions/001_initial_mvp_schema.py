"""initial_mvp_schema

Revision ID: 001_initial_mvp_schema
Revises: 
Create Date: 2026-10-29 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_mvp_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'], unique=False)

    # 2. candidates
    op.create_table(
        'candidates',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('education', sa.String(length=255), nullable=True),
        sa.Column('skills', sa.Text(), nullable=True),
        sa.Column('resume_url', sa.String(length=500), nullable=True),
        sa.Column('preferred_communication_mode', sa.String(length=50), nullable=False, server_default='isl'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_candidates_user_id', 'candidates', ['user_id'], unique=True)

    # 3. interviewers
    op.create_table(
        'interviewers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('designation', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_interviewers_user_id', 'interviewers', ['user_id'], unique=True)

    # 4. sign_classes
    op.create_table(
        'sign_classes',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('label', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='interview'),
        sa.Column('example_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('label')
    )
    op.create_index('ix_sign_classes_label', 'sign_classes', ['label'], unique=True)

    # 5. model_versions
    op.create_table(
        'model_versions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('version_tag', sa.String(length=50), nullable=False),
        sa.Column('model_type', sa.String(length=50), nullable=False),
        sa.Column('weights_path_or_url', sa.String(length=500), nullable=False),
        sa.Column('accuracy_metrics', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('deployed_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('version_tag')
    )
    op.create_index('ix_model_versions_version_tag', 'model_versions', ['version_tag'], unique=True)

    # 6. interviews
    op.create_table(
        'interviews',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('candidate_id', sa.String(length=36), nullable=False),
        sa.Column('interviewer_id', sa.String(length=36), nullable=False),
        sa.Column('scheduled_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='45'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='scheduled'),
        sa.Column('meeting_room_id', sa.String(length=64), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['interviewer_id'], ['interviewers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('meeting_room_id')
    )
    op.create_index('ix_interviews_candidate_id', 'interviews', ['candidate_id'], unique=False)
    op.create_index('ix_interviews_interviewer_id', 'interviews', ['interviewer_id'], unique=False)
    op.create_index('ix_interviews_meeting_room_id', 'interviews', ['meeting_room_id'], unique=True)
    op.create_index('ix_interviews_status', 'interviews', ['status'], unique=False)

    # 7. questions
    op.create_table(
        'questions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('interviewer_id', sa.String(length=36), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='general'),
        sa.Column('difficulty', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['interviewer_id'], ['interviewers.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_questions_interviewer_id', 'questions', ['interviewer_id'], unique=False)

    # 8. interview_questions
    op.create_table(
        'interview_questions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('interview_id', sa.String(length=36), nullable=False),
        sa.Column('question_id', sa.String(length=36), nullable=True),
        sa.Column('question_order', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('custom_prompt', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_interview_questions_interview_id', 'interview_questions', ['interview_id'], unique=False)
    op.create_index('ix_interview_questions_question_id', 'interview_questions', ['question_id'], unique=False)

    # 9. responses
    op.create_table(
        'responses',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('interview_question_id', sa.String(length=36), nullable=False),
        sa.Column('candidate_id', sa.String(length=36), nullable=False),
        sa.Column('raw_sign_data', sa.Text(), nullable=True),
        sa.Column('final_text_response', sa.Text(), nullable=True),
        sa.Column('audio_caption_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['interview_question_id'], ['interview_questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_responses_candidate_id', 'responses', ['candidate_id'], unique=False)
    op.create_index('ix_responses_interview_question_id', 'responses', ['interview_question_id'], unique=False)

    # 10. transcripts
    op.create_table(
        'transcripts',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('interview_id', sa.String(length=36), nullable=False),
        sa.Column('speaker_role', sa.String(length=20), nullable=False),
        sa.Column('speaker_id', sa.String(length=36), nullable=True),
        sa.Column('message_type', sa.String(length=30), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['speaker_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_transcripts_interview_id', 'transcripts', ['interview_id'], unique=False)
    op.create_index('ix_transcripts_message_type', 'transcripts', ['message_type'], unique=False)
    op.create_index('ix_transcripts_speaker_id', 'transcripts', ['speaker_id'], unique=False)
    op.create_index('ix_transcripts_timestamp', 'transcripts', ['timestamp'], unique=False)

    # 11. predictions
    op.create_table(
        'predictions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('interview_id', sa.String(length=36), nullable=False),
        sa.Column('transcript_id', sa.String(length=36), nullable=True),
        sa.Column('sign_class_id', sa.String(length=36), nullable=True),
        sa.Column('predicted_sign', sa.String(length=100), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('is_low_confidence', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('latency_ms', sa.Float(), nullable=True),
        sa.Column('raw_landmark_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sign_class_id'], ['sign_classes.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['transcript_id'], ['transcripts.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_predictions_interview_id', 'predictions', ['interview_id'], unique=False)
    op.create_index('ix_predictions_is_low_confidence', 'predictions', ['is_low_confidence'], unique=False)
    op.create_index('ix_predictions_sign_class_id', 'predictions', ['sign_class_id'], unique=False)
    op.create_index('ix_predictions_transcript_id', 'predictions', ['transcript_id'], unique=False)


def downgrade() -> None:
    op.drop_table('predictions')
    op.drop_table('transcripts')
    op.drop_table('responses')
    op.drop_table('interview_questions')
    op.drop_table('questions')
    op.drop_table('interviews')
    op.drop_table('model_versions')
    op.drop_table('sign_classes')
    op.drop_table('interviewers')
    op.drop_table('candidates')
    op.drop_table('users')
