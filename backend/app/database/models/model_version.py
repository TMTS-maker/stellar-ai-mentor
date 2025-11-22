"""
Stellecta LucidAI Backend - Model Version Model

NEW TABLE: LucidAI model registry and deployment tracking.

Tracks all versions of the Stellecta LucidAI model:
- Training configuration and datasets
- Evaluation metrics
- Deployment status
- Performance in production
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database.engine import Base


class ModelVersion(Base):
    """
    Model Version entity.

    Registry of all LucidAI model versions for:
    - Version control and reproducibility
    - A/B testing
    - Rollback capabilities
    - Performance monitoring
    """

    __tablename__ = "model_versions"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ========================================================================
    # MODEL METADATA
    # ========================================================================
    version = Column(String(50), unique=True, nullable=False, index=True)
    """
    Semantic version string:
    - lucidai-v1.0
    - lucidai-v1.1
    - lucidai-v2.0-beta
    """

    base_model = Column(String(100), nullable=False)
    """
    Base foundation model:
    - meta-llama/Llama-3-70b-hf
    - mistralai/Mistral-Large
    - microsoft/Phi-3-medium
    """

    training_type = Column(String(50), nullable=False)
    """
    Training methodology:
    - sft (supervised fine-tuning)
    - rlhf (reinforcement learning from human feedback)
    - dpo (direct preference optimization)
    """

    # ========================================================================
    # TRAINING DETAILS
    # ========================================================================
    training_dataset_version = Column(String(50), nullable=True)
    """Dataset version used for training (e.g., v1.0, v1.1)"""

    training_examples_count = Column(Integer, nullable=True)
    """Total number of training examples"""

    training_started_at = Column(DateTime(timezone=True), nullable=True)
    """Training job start timestamp"""

    training_completed_at = Column(DateTime(timezone=True), nullable=True)
    """Training job completion timestamp"""

    training_config = Column(JSON, nullable=True)
    """
    Full training configuration:
    {
        "epochs": 3,
        "learning_rate": 2e-5,
        "batch_size": 4,
        "lora_rank": 64,
        "quantization": "4-bit"
    }
    """

    # ========================================================================
    # EVALUATION METRICS (Test Set)
    # ========================================================================
    eval_loss = Column(Float, nullable=True)
    """Evaluation loss on held-out test set"""

    eval_accuracy = Column(Float, nullable=True)
    """Evaluation accuracy"""

    eval_didactic_quality = Column(Float, nullable=True)
    """Average didactic quality score on test set"""

    # ========================================================================
    # DEPLOYMENT
    # ========================================================================
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    """Timestamp of production deployment"""

    deployment_status = Column(String(20), default="testing", nullable=False, index=True)
    """
    Deployment status:
    - testing (A/B test, small %)
    - production (full rollout)
    - deprecated (replaced by newer version)
    - archived (historical record only)
    """

    traffic_percentage = Column(Float, default=0.0, nullable=True)
    """Percentage of traffic routed to this model version (0-100)"""

    # ========================================================================
    # PERFORMANCE (Aggregated from llm_interactions)
    # ========================================================================
    avg_inference_time_ms = Column(Float, nullable=True)
    """Average inference latency in production"""

    avg_confidence_score = Column(Float, nullable=True)
    """Average self-reported confidence"""

    avg_composite_score = Column(Float, nullable=True)
    """Average evaluation composite score"""

    # ========================================================================
    # OUTCOMES (Populated Over Time)
    # ========================================================================
    total_interactions = Column(Integer, default=0, nullable=True)
    """Total interactions served by this model version"""

    student_helpful_rate = Column(Float, nullable=True)
    """Percentage of helpful feedback (thumbs up)"""

    teacher_rating_avg = Column(Float, nullable=True)
    """Average teacher quality rating (1-5)"""

    h_pem_improvement_rate = Column(Float, nullable=True)
    """
    Percentage of interactions that led to H-PEM improvement.
    CRITICAL metric for RLHF effectiveness.
    """

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<ModelVersion(version={self.version}, status={self.deployment_status}, traffic={self.traffic_percentage}%)>"
