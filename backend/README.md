# Stellecta LucidAI Multi-LLM Backend

FastAPI backend implementing the Multi-LLM architecture for Stellecta.

## 🏗️ Architecture

This backend implements the **Stellecta LucidAI Multi-LLM Architecture** with:

- **Multi-LLM Router**: Intelligent routing between LucidAI (proprietary) and external LLMs (Gemini, OpenAI, Claude)
- **Evaluation Service**: Multi-dimensional response quality scoring
- **Agent Layer**: Supervisor + 8 Mentor personas (Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas)
- **LVO Engine**: Learn-Verify-Own cycle (scaffold)
- **H-PEM Metrics**: Holistic Pedagogical Engagement Metrics (scaffold)
- **Gamification**: XP, achievements, streaks (scaffold)
- **Blockchain**: Stellar credential minting (stub)
- **Training Pipeline**: Anonymized data collection for LucidAI fine-tuning

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for caching)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Required Configuration:**
- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: Google Gemini API key (default LLM for Phase 0)
- Optional: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `LUCIDAI_API_URL`

### 3. Initialize Database

```bash
# Run Alembic migrations
alembic upgrade head
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000

**API Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/              # Agent Layer
│   │   ├── supervisor.py    # Supervisor Agent (orchestration)
│   │   ├── mentor_engine.py # Mentor Engine (8 personas)
│   │   ├── personas.py      # Mentor definitions
│   │   └── schemas.py       # Agent schemas
│   │
│   ├── llm/                 # Multi-LLM Layer
│   │   ├── router.py        # Multi-LLM Router (CORE)
│   │   ├── evaluation.py    # Evaluation Service
│   │   ├── policies.py      # Routing Policies
│   │   ├── base.py          # BaseLLMClient (abstraction)
│   │   ├── schemas.py       # LLM schemas
│   │   └── providers/       # LLM Providers
│   │       ├── lucidai.py   # LucidAI (stub)
│   │       ├── gemini.py    # Gemini (active)
│   │       ├── openai.py    # OpenAI GPT-4
│   │       └── claude.py    # Claude 3.5
│   │
│   ├── lvo/                 # Learn-Verify-Own Engine (scaffold)
│   │   ├── service.py       # LVO Orchestrator
│   │   └── hpem.py          # H-PEM Calculator
│   │
│   ├── gamification/        # Gamification Engine (scaffold)
│   │   └── service.py       # XP, achievements, streaks
│   │
│   ├── blockchain/          # Stellar Blockchain (stub)
│   │   └── service.py       # Credential minting
│   │
│   ├── training/            # Training Data Pipeline
│   │   ├── logger.py        # LLM Interaction Logger
│   │   ├── anonymization.py # COPPA/GDPR anonymization
│   │   ├── labeling.py      # Automated labeling
│   │   └── dataset.py       # Dataset builder
│   │
│   ├── database/            # Database Layer
│   │   ├── engine.py        # SQLAlchemy engine
│   │   ├── models/          # Database models
│   │   │   ├── student.py
│   │   │   ├── conversation.py
│   │   │   ├── llm_interaction.py      # NEW
│   │   │   ├── training_example.py     # NEW
│   │   │   ├── model_version.py        # NEW
│   │   │   ├── llm_performance_tracking.py  # NEW
│   │   │   ├── hpem.py
│   │   │   ├── gamification.py
│   │   │   └── blockchain.py
│   │   └── repositories/
│   │
│   ├── api/                 # FastAPI Routers
│   │   ├── chat.py          # Chat endpoint
│   │   ├── agents.py        # Agent info
│   │   └── admin.py         # Admin/metrics
│   │
│   ├── config.py            # Configuration (Pydantic Settings)
│   └── main.py              # FastAPI app entry point
│
├── alembic/                 # Database Migrations
├── tests/                   # Tests
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # This file
```

## 🔑 Key Components

### 1. Multi-LLM Router

**File:** `app/llm/router.py`

Central orchestration for all LLM interactions:
- Routes requests to appropriate LLM (LucidAI, Gemini, OpenAI, Claude)
- Handles single/dual/hybrid execution modes
- Evaluates and selects best responses
- Logs all interactions for training

**Usage:**
```python
from app.llm.router import MultiLLMRouter
from app.llm.schemas import LLMRequest

router = MultiLLMRouter()
request = LLMRequest(
    system_prompt="You are a helpful tutor...",
    user_message="How do I solve 2x + 3 = 7?",
    temperature=0.7,
)
response = await router.generate(request, context={})
```

### 2. Evaluation Service

**File:** `app/llm/evaluation.py`

Multi-dimensional quality scoring:
- Correctness (0-1)
- Didactic Quality (0-1)
- Persona Alignment (0-1)
- Safety (0-1)
- Curriculum Alignment (0-1)

### 3. Agent Layer

**Files:** `app/agents/supervisor.py`, `app/agents/mentor_engine.py`

- **Supervisor Agent**: Orchestrates all interactions (safety, mentor selection, quality validation)
- **Mentor Engine**: 8 personas (Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas)

### 4. LLM Providers

All providers implement `BaseLLMClient`:
- **LucidAI** (stub): Proprietary model (Phase 2)
- **Gemini** (active): Default for Phase 0
- **OpenAI**: GPT-4 Turbo
- **Claude**: Claude 3.5 Sonnet

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📊 Database Schema

### New Tables (Multi-LLM Architecture)

- **`llm_interactions`**: All LLM requests/responses with routing metadata
- **`training_examples`**: Anonymized training data for LucidAI
- **`model_versions`**: LucidAI model registry
- **`llm_performance_tracking`**: Confidence calibration data

### Existing Tables

- `students`, `conversations`, `conversation_messages`
- `hpem_scores`, `gamification_progress`, `blockchain_credentials`

## 🔐 Security & Privacy

- **COPPA/GDPR Compliant**: All training data anonymized
- **PII Scrubbing**: Automatic removal of personal information
- **API Key Management**: All secrets in environment variables
- **Rate Limiting**: TODO (Phase 2)

## 📈 Monitoring

**LLM Metrics:**
```bash
curl http://localhost:8000/api/admin/llm-metrics
```

Returns:
- Total requests per LLM
- Average latency
- Cost tracking
- Quality scores

## 🚧 TODO (Future Phases)

- [ ] Full LVO business logic implementation
- [ ] H-PEM calculation algorithms
- [ ] Gamification mechanics
- [ ] Stellar blockchain integration
- [ ] LucidAI model fine-tuning
- [ ] RLHF training pipeline
- [ ] Advanced evaluation models
- [ ] Real-time confidence calibration

## 📚 Documentation

Full architecture documentation: See `stellecta-lucidai-multi-llm-architecture.md`

## 🤝 Contributing

This backend is part of the Stellecta platform. All changes must:
- Follow the **extension-not-replacement** principle
- Maintain vendor-agnostic design
- Include tests
- Update documentation

## 📄 License

Proprietary - Stellecta Platform
