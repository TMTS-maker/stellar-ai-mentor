# Stellecta LucidAI Multi-LLM Backend Integration

**Version:** Phase 0
**Last Updated:** 2025-11-22
**Status:** Foundation Implementation Complete

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [System Architecture Diagram](#system-architecture-diagram)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [Module Reference](#module-reference)
8. [Setup Guide](#setup-guide)
9. [Testing Strategy](#testing-strategy)
10. [Deployment](#deployment)
11. [Future Roadmap](#future-roadmap)

---

## Architecture Overview

The Stellecta LucidAI Multi-LLM Backend implements a sophisticated educational platform that combines proprietary and external Large Language Models (LLMs) to deliver personalized AI tutoring through 8 specialized mentor personas.

### Key Principles

1. **Extension-Not-Replacement**: All new Multi-LLM infrastructure integrates as adapters/extensions to existing Stellecta backend
2. **Vendor-Agnostic Design**: Uniform abstraction layer (`BaseLLMClient`) enables seamless provider swapping
3. **Quality-First Routing**: Multi-dimensional evaluation drives intelligent LLM selection
4. **Privacy-First Training**: COPPA/GDPR-compliant anonymization for all training data
5. **Incremental Rollout**: LucidAI integration via traffic percentage control

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼────────────────────────────────────┐
│                    FastAPI Application Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Chat API   │  │  Agents API  │  │    Admin API        │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬──────────┘  │
└─────────┼──────────────────┼───────────────────────┼────────────┘
          │                  │                       │
┌─────────▼──────────────────▼───────────────────────▼────────────┐
│                      Supervisor Agent                            │
│         (Safety, Mentor Selection, Quality Validation)          │
└─────────┬────────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────────┐
│                       Mentor Engine                              │
│   8 Personas: Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas│
│              (Context Enrichment, Routing Hints)                 │
└─────────┬────────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────────┐
│                    Multi-LLM Router (CORE)                       │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Routing Policy │  │ Evaluation Svc  │  │ Training Logger │  │
│  │     Engine     │  │  (5 dimensions) │  │                 │  │
│  └────────┬───────┘  └────────┬────────┘  └────────┬────────┘  │
└───────────┼───────────────────┼────────────────────┼────────────┘
            │                   │                    │
┌───────────▼───────────────────▼────────────────────▼────────────┐
│                    LLM Provider Abstraction                      │
│                        (BaseLLMClient)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ LucidAI  │  │  Gemini  │  │  OpenAI  │  │   Claude     │   │
│  │  (stub)  │  │ (default)│  │  GPT-4   │  │ 3.5 Sonnet   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────────────┘
            │                   │                    │
┌───────────▼───────────────────▼────────────────────▼────────────┐
│                  Supporting Services Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐│
│  │   LVO    │  │  H-PEM   │  │ Gamify   │  │   Blockchain    ││
│  │ (scaffold)│  │(scaffold)│  │(scaffold)│  │     (stub)      ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────────────┘│
└──────────────────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                     PostgreSQL Database                          │
│  Core: students, conversations, messages                         │
│  Multi-LLM: llm_interactions, training_examples, model_versions  │
│  Metrics: hpem_scores, gamification_progress                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## System Architecture Diagram

### High-Level System Flow

```mermaid
graph TB
    Student[Student via Frontend]
    API[FastAPI Application]
    Supervisor[Supervisor Agent]
    Mentor[Mentor Engine]
    Router[Multi-LLM Router]
    Policy[Routing Policy Engine]
    Eval[Evaluation Service]
    Logger[Training Logger]

    LucidAI[LucidAI Provider]
    Gemini[Gemini Provider]
    OpenAI[OpenAI Provider]
    Claude[Claude Provider]

    DB[(PostgreSQL)]
    Training[(Training Data)]

    Student -->|POST /api/chat| API
    API -->|process_conversation| Supervisor
    Supervisor -->|safety_check| Supervisor
    Supervisor -->|select_mentor| Mentor
    Mentor -->|generate_response| Router
    Router -->|decide_routing| Policy
    Policy -->|routing_decision| Router

    Router -->|generate| LucidAI
    Router -->|generate| Gemini
    Router -->|generate| OpenAI
    Router -->|generate| Claude

    LucidAI -->|LLMResponse| Router
    Gemini -->|LLMResponse| Router
    OpenAI -->|LLMResponse| Router
    Claude -->|LLMResponse| Router

    Router -->|evaluate| Eval
    Eval -->|scores| Router
    Router -->|best_response| Mentor

    Router -->|log_interaction| Logger
    Logger -->|store| DB
    Logger -->|anonymize & label| Training

    Mentor -->|response| Supervisor
    Supervisor -->|validate| Supervisor
    Supervisor -->|final_response| API
    API -->|JSON| Student

    DB -->|context| Mentor
    DB -->|H-PEM scores| Policy
```

### Component Interaction Sequence

```mermaid
sequenceDiagram
    participant S as Student
    participant API as FastAPI
    participant SUP as Supervisor
    participant ME as Mentor Engine
    participant RT as Multi-LLM Router
    participant POL as Policy Engine
    participant LLM as LLM Providers
    participant EVAL as Evaluation
    participant LOG as Training Logger
    participant DB as Database

    S->>API: POST /api/chat {message, student_id}
    API->>SUP: process_conversation()
    SUP->>SUP: safety_check()
    SUP->>ME: select_mentor()
    ME->>DB: fetch_student_context()
    DB-->>ME: H-PEM scores, weak_skills, etc.
    ME->>ME: build_system_prompt()
    ME->>RT: generate(request, context)

    RT->>POL: decide_routing(hints, context)
    POL->>POL: analyze task_type, risk_level, H-PEM
    POL-->>RT: RoutingDecision {mode, primary, fallback}

    alt Hybrid Mode (Dual LLM)
        RT->>LLM: generate_parallel() [LucidAI + Gemini]
        LLM-->>RT: [response1, response2]
        RT->>EVAL: compare_responses()
        EVAL-->>RT: best_response + scores
    else Single Mode
        RT->>LLM: generate() [Gemini]
        LLM-->>RT: response
        RT->>EVAL: evaluate_single()
        EVAL-->>RT: scores
    end

    RT->>LOG: log_interaction()
    LOG->>DB: INSERT llm_interactions
    LOG->>LOG: anonymize_and_label()
    LOG->>DB: INSERT training_examples

    RT-->>ME: RouterResponse {message, metadata}
    ME-->>SUP: mentor_response
    SUP->>SUP: quality_validation()
    SUP-->>API: final_response
    API-->>S: JSON {message, mentor_id, llm_used}
```

---

## Core Components

### 1. Multi-LLM Router

**Location:** `backend/app/llm/router.py`

The central orchestration engine for all LLM interactions.

**Responsibilities:**
- Check LLM provider availability
- Invoke Routing Policy Engine for decision-making
- Execute single/dual/hybrid LLM calls
- Coordinate evaluation and response selection
- Log all interactions for training pipeline

**Key Methods:**

```python
class MultiLLMRouter:
    async def generate(
        self,
        request: LLMRequest,
        context: Dict[str, Any]
    ) -> RouterResponse:
        """
        Main entry point for LLM generation.

        Args:
            request: LLMRequest with system_prompt, user_message, temperature
            context: Dict with routing_hints, student_id, conversation_id

        Returns:
            RouterResponse with message, metadata, routing_decision, evaluation
        """
```

**Execution Modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| **Single** | Query one LLM only | Low-risk, high-confidence scenarios |
| **Dual** | Query 2 LLMs, pick best | Mastery verification, high-stakes |
| **Hybrid** | LucidAI + External, validate | Production rollout with safeguards |

**Configuration:**

```python
# .env
ROUTING_MODE=hybrid  # single | dual | hybrid
DEFAULT_LLM=gemini
ENABLE_LUCIDAI=false  # Set to true when LucidAI ready
LUCIDAI_TRAFFIC_PCT=0.1  # 10% traffic to LucidAI (gradual rollout)
```

### 2. Routing Policy Engine

**Location:** `backend/app/llm/policies.py`

Context-aware decision tree for intelligent LLM selection.

**Decision Factors:**

```mermaid
graph TD
    Start[Routing Request]
    Risk{Risk Level?}
    Task{Task Type?}
    HPEM{Student H-PEM?}
    Domain{Domain?}

    Start --> Risk
    Risk -->|High| HighRisk[LucidAI + Validation]
    Risk -->|Medium| Task
    Risk -->|Low| Task

    Task -->|Creative| Creative[GPT-4 / Claude]
    Task -->|Code| Code[GPT-4 / Claude]
    Task -->|Math| Math[LucidAI / Gemini]
    Task -->|Concept| HPEM

    HPEM -->|< 0.5 Struggling| Scaffold[LucidAI - Scaffolding]
    HPEM -->|0.5-0.9 Proficient| Domain
    HPEM -->|> 0.9 Advanced| Enrichment[External - Enrichment]

    Domain -->|STEM| STEM[LucidAI Primary]
    Domain -->|Humanities| HUM[External Primary]
```

**Policy Rules:**

```python
# High-risk tasks (mastery verification, assessments)
if hints.risk_level == "high":
    return RoutingDecision(
        mode="dual",
        primary_llm="lucidai",
        secondary_llm="gemini",
        reason="High-risk task requires validation"
    )

# Struggling students (H-PEM < 0.5)
if context.get("h_pem_proficiency", 0.5) < 0.5:
    return RoutingDecision(
        mode="single",
        primary_llm="lucidai",
        reason="LucidAI excels at scaffolding for struggling students"
    )

# Creative/coding tasks
if hints.task_type in ["creative_writing", "code_generation"]:
    return RoutingDecision(
        mode="single",
        primary_llm="gpt4",  # or "claude"
        reason="External LLMs excel at creative/coding tasks"
    )
```

### 3. Evaluation Service

**Location:** `backend/app/llm/evaluation.py`

Multi-dimensional quality assessment across 5 dimensions.

**Evaluation Dimensions:**

```mermaid
graph LR
    Response[LLM Response]
    Correctness[Correctness<br/>0-1 score]
    Didactic[Didactic Quality<br/>0-1 score]
    Persona[Persona Alignment<br/>0-1 score]
    Safety[Safety<br/>0-1 score]
    Curriculum[Curriculum Alignment<br/>0-1 score]

    Response --> Correctness
    Response --> Didactic
    Response --> Persona
    Response --> Safety
    Response --> Curriculum

    Correctness -->|weight: 0.3| Composite
    Didactic -->|weight: 0.3| Composite
    Persona -->|weight: 0.2| Composite
    Safety -->|weight: 0.1| Composite
    Curriculum -->|weight: 0.1| Composite

    Composite[Composite Score<br/>0-1]
```

**Scoring Algorithms:**

1. **Correctness** (30% weight)
   - Checks against ground truth if available
   - Validates mathematical/factual accuracy
   - Penalizes hallucinations

2. **Didactic Quality** (30% weight)
   - Evaluates pedagogical approach
   - Checks for scaffolding, Socratic method
   - Assesses age-appropriateness

3. **Persona Alignment** (20% weight)
   - Matches response to mentor personality
   - Validates subject expertise consistency
   - Checks teaching style adherence

4. **Safety** (10% weight)
   - Content moderation (harmful, inappropriate)
   - Privacy checks (no PII exposure)
   - Bias detection

5. **Curriculum Alignment** (10% weight)
   - Validates adherence to learning objectives
   - Checks competency targeting
   - Assesses prerequisite awareness

**Configuration:**

```python
# .env
EVALUATION_CORRECTNESS_WEIGHT=0.3
EVALUATION_DIDACTIC_WEIGHT=0.3
EVALUATION_PERSONA_WEIGHT=0.2
EVALUATION_SAFETY_WEIGHT=0.1
EVALUATION_CURRICULUM_WEIGHT=0.1
EVALUATION_MIN_COMPOSITE_SCORE=0.6  # Reject responses below this
```

### 4. Agent Layer

#### Supervisor Agent

**Location:** `backend/app/agents/supervisor.py`

Top-level orchestrator for all student-mentor interactions.

**Responsibilities:**

```mermaid
graph TD
    Request[Student Request]
    Safety[Safety Check]
    Mentor[Mentor Selection]
    Generate[Generate Response]
    Validate[Quality Validation]
    Escalate{Escalation Needed?}
    Teacher[Notify Teacher]
    Return[Return Response]

    Request --> Safety
    Safety -->|Pass| Mentor
    Safety -->|Fail| Teacher
    Mentor --> Generate
    Generate --> Validate
    Validate --> Escalate
    Escalate -->|Yes| Teacher
    Escalate -->|No| Return
```

**Safety Checks:**
- Content moderation (profanity, harmful requests)
- Privacy protection (student asking for personal info)
- Academic integrity (direct answer requests for assessments)

**Escalation Triggers:**
- Low composite evaluation score (< 0.6)
- Student frustration detected (multiple failed attempts)
- Out-of-scope questions (non-academic topics)
- Safety violations

#### Mentor Engine

**Location:** `backend/app/agents/mentor_engine.py`

Manages 8 specialized AI tutor personas with contextual awareness.

**Mentor Personas:**

| Mentor | Subject | Personality | Teaching Style |
|--------|---------|-------------|----------------|
| **Stella** | Mathematics | Analytical, Patient, Encouraging | Step-by-step problem solving with visual aids |
| **Max** | Science | Enthusiastic, Curious, Experimental | Inquiry-based learning with real-world examples |
| **Nova** | Computer Science | Logical, Innovative, Pragmatic | Project-based learning with debugging guidance |
| **Darwin** | Biology/Life Sciences | Observant, Methodical, Nurturing | Observation-driven learning with diagrams |
| **Lexis** | Language Arts | Articulate, Empathetic, Expressive | Creative expression with grammar scaffolding |
| **Neo** | Social Studies | Thoughtful, Balanced, Contextual | Critical thinking with historical connections |
| **Luna** | Arts & Music | Creative, Passionate, Supportive | Exploration-based learning with encouragement |
| **Atlas** | Geography/World Studies | Adventurous, Knowledgeable, Engaging | Story-driven learning with cultural context |

**Context Enrichment:**

The Mentor Engine enriches system prompts with student context:

```python
system_prompt = f"""
You are {mentor.name}, a {mentor.personality[0].lower()} {mentor.subject} tutor.

STUDENT CONTEXT:
- Current H-PEM Proficiency: {student_context.h_pem_proficiency:.2f}
- Weak Skills: {', '.join(student_context.weak_skills)}
- Recent Achievements: {', '.join(student_context.achievements)}
- Preferred Learning Style: {student_context.learning_style}

TEACHING APPROACH:
{mentor.teaching_style}

CONVERSATION HISTORY:
{conversation_context}

Remember:
- Keep responses age-appropriate (age {student_context.age})
- Use Socratic method when appropriate
- Adapt scaffolding based on H-PEM proficiency
- Celebrate small wins to build confidence
"""
```

### 5. LLM Provider Abstraction

**Location:** `backend/app/llm/base.py` + `backend/app/llm/providers/`

Vendor-agnostic interface for all LLM providers.

**Architecture:**

```mermaid
classDiagram
    class BaseLLMClient {
        <<abstract>>
        +generate(request: LLMRequest) LLMResponse
        +get_provider_name() str
        +is_available() bool
        +estimate_tokens(text: str) int
        +calculate_cost(tokens_in, tokens_out) float
    }

    class LucidAIProvider {
        -api_url: str
        -api_key: str
        -timeout: int
        +generate() LLMResponse
        +is_available() bool
    }

    class GeminiProvider {
        -api_key: str
        -model: GenerativeModel
        +generate() LLMResponse
    }

    class OpenAIProvider {
        -api_key: str
        -client: OpenAI
        +generate() LLMResponse
    }

    class ClaudeProvider {
        -api_key: str
        -client: Anthropic
        +generate() LLMResponse
    }

    BaseLLMClient <|-- LucidAIProvider
    BaseLLMClient <|-- GeminiProvider
    BaseLLMClient <|-- OpenAIProvider
    BaseLLMClient <|-- ClaudeProvider
```

**Provider Status:**

| Provider | Status | Model | Use Case |
|----------|--------|-------|----------|
| **LucidAI** | Stub (Phase 2) | `stellecta-lucidai-v1` | Proprietary pedagogical model |
| **Gemini** | Active (Default) | `gemini-1.5-pro` | General-purpose, cost-effective |
| **OpenAI** | Active | `gpt-4-turbo` | Creative writing, coding |
| **Claude** | Active | `claude-3-5-sonnet` | Complex reasoning, coding |

**Standardized Response:**

```python
class LLMResponse(BaseModel):
    content: str
    llm_provider: str  # "lucidai" | "gemini" | "openai" | "claude"
    model_version: str  # "gemini-1.5-pro", "gpt-4-turbo", etc.
    confidence_score: Optional[float] = None  # 0-1
    tokens_input: int = 0
    tokens_output: int = 0
    inference_time_ms: float = 0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = {}
```

### 6. Training Data Pipeline

**Location:** `backend/app/training/`

COPPA/GDPR-compliant training data collection for LucidAI fine-tuning.

**Pipeline Flow:**

```mermaid
graph LR
    Interaction[LLM Interaction]
    Logger[Interaction Logger]
    Anon[Anonymization Service]
    Label[Labeling Service]
    Dataset[Dataset Builder]
    Storage[(Training Examples DB)]
    Export[Export to Fine-Tuning]

    Interaction -->|log| Logger
    Logger -->|raw data| Anon
    Anon -->|PII scrubbed| Label
    Label -->|auto-labeled| Dataset
    Dataset -->|store| Storage
    Storage -->|query by version| Export
    Export -->|JSONL format| FineTune[LucidAI Fine-Tuning]
```

**Components:**

1. **Interaction Logger** (`logger.py`)
   - Logs every LLM request/response to `llm_interactions` table
   - Captures routing decisions, evaluation scores, performance metrics

2. **Anonymization Service** (`anonymization.py`)
   - One-way hash of student IDs (SHA-256)
   - PII scrubbing (emails, phone numbers, names)
   - COPPA/GDPR compliance

3. **Labeling Service** (`labeling.py`)
   - Automated labels: subject, grade_level, mentor_persona, h_pem_proficiency
   - Quality scores from evaluation
   - Outcome metrics (H-PEM delta, student feedback)

4. **Dataset Builder** (`dataset.py`)
   - Constructs instruction-tuning datasets
   - Train/val/test splits (80/10/10)
   - Export to JSONL format for fine-tuning

**Example Training Record:**

```json
{
  "anonymous_student_id": "a3f8b9c2...",
  "system_prompt": "You are Stella, a patient mathematics tutor...",
  "user_message": "How do I solve 2x + 3 = 7?",
  "assistant_response": "Great question! Let's solve this step by step...",
  "labels": {
    "subject": "algebra",
    "grade_level": 7,
    "mentor_persona": "stella",
    "h_pem_proficiency": 0.62
  },
  "quality_scores": {
    "correctness": 1.0,
    "didactic_quality": 0.95,
    "composite": 0.87
  },
  "outcome": {
    "student_helpful": true,
    "h_pem_delta": 0.03
  },
  "dataset_version": "v1.0",
  "split": "train"
}
```

### 7. Supporting Services (Scaffolds)

#### LVO Engine

**Location:** `backend/app/lvo/service.py`

Learn-Verify-Own pedagogical cycle (interface-only scaffold for Phase 0).

**Phases:**
- **Learn**: Adaptive content delivery based on H-PEM
- **Verify**: Mastery checks with calibrated difficulty
- **Own**: Transfer tasks to demonstrate deep understanding

**Interface:**

```python
class LVOService:
    async def start_learn_phase(
        self,
        student_id: str,
        competency_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        # TODO: Full implementation in Phase 1
        pass
```

#### H-PEM Calculator

**Location:** `backend/app/lvo/hpem.py`

Holistic Pedagogical Engagement Metrics (interface-only scaffold).

**Metrics:**
- **Proficiency** (P): Competency mastery level (0-1)
- **Resilience** (R): Persistence through challenges (0-1)
- **Velocity** (V): Learning speed (0-1)
- **Engagement** (E): Participation and effort (0-1)
- **Transfer** (T): Application to new contexts (0-1)

**Composite Formula:**

```
H-PEM = 0.35P + 0.15R + 0.15V + 0.20E + 0.15T
```

**Interface:**

```python
class HPEMCalculator:
    async def calculate_proficiency(self, student_id: str, subject: str) -> float:
        # TODO: Implement based on assessment results
        pass

    async def calculate_composite(self, P, R, V, E, T) -> float:
        # IMPLEMENTED: Weighted average
        return self.weights["proficiency"] * P + ...
```

#### Gamification Engine

**Location:** `backend/app/gamification/service.py`

XP, achievements, streaks (interface-only scaffold).

**Features:**
- Experience points (XP) for task completion
- Achievements and badges
- Streak tracking
- Leaderboards

#### Blockchain Service

**Location:** `backend/app/blockchain/service.py`

Stellar blockchain credential minting (stub for Phase 2).

**Features:**
- Mint verifiable credentials for competency mastery
- Issue on Stellar blockchain
- Student-owned digital badges

---

## Data Flow

### End-to-End Student Interaction

```mermaid
sequenceDiagram
    participant S as Student (Frontend)
    participant API as /api/chat
    participant SUP as Supervisor
    participant ME as Mentor Engine
    participant DB as Database
    participant RT as Router
    participant LLM as LLM Provider
    participant LOG as Training Logger

    S->>API: POST {message: "Help with algebra", student_id: "123"}

    API->>SUP: process_conversation(request)
    SUP->>SUP: safety_check(message)
    Note over SUP: Check for harmful content,<br/>privacy violations

    SUP->>ME: select_mentor(message, student)
    ME->>DB: SELECT * FROM students WHERE id=123
    DB-->>ME: {age: 13, grade: 7, ...}
    ME->>DB: SELECT * FROM hpem_scores WHERE student_id=123
    DB-->>ME: {proficiency: 0.62, resilience: 0.71, ...}

    ME->>ME: build_system_prompt(mentor="stella", context)
    ME->>RT: generate(request, context)

    RT->>RT: decide_routing(hints, context)
    Note over RT: Policy Engine:<br/>H-PEM=0.62, task=math<br/>→ Single mode, Gemini

    RT->>LLM: generate(system_prompt, user_message)
    LLM-->>RT: response {content: "Let's solve...", tokens: 350}

    RT->>RT: evaluate_single(response, context)
    Note over RT: Scores:<br/>Correctness: 1.0<br/>Didactic: 0.95<br/>Composite: 0.87

    RT->>LOG: log_interaction(request, response, evaluation)
    LOG->>DB: INSERT INTO llm_interactions
    LOG->>LOG: anonymize_and_label(interaction)
    LOG->>DB: INSERT INTO training_examples

    RT-->>ME: RouterResponse {message, metadata}
    ME-->>SUP: mentor_response

    SUP->>SUP: quality_validation(response)
    Note over SUP: Composite score 0.87 > 0.6<br/>✓ Pass

    SUP-->>API: final_response
    API-->>S: 200 OK {message, mentor_id: "stella", llm_used: "gemini"}

    S->>S: Display response in chat
```

### Multi-LLM Routing Decision Tree

```mermaid
graph TD
    Start[Student Request]
    Context[Fetch Student Context]
    Hints[Extract Routing Hints]
    Policy[Policy Engine Decision]

    Single[Single Mode]
    Dual[Dual Mode]
    Hybrid[Hybrid Mode]

    LucidAI[Query LucidAI]
    Gemini[Query Gemini]
    GPT4[Query GPT-4]
    Claude[Query Claude]

    Evaluate[Evaluate Response]
    Compare[Compare Responses]
    Select[Select Best]

    Log[Log to Training Pipeline]
    Return[Return to Mentor Engine]

    Start --> Context
    Context --> Hints
    Hints --> Policy

    Policy -->|Low risk, proficient student| Single
    Policy -->|High risk, mastery verification| Dual
    Policy -->|Production rollout| Hybrid

    Single --> Gemini
    Single --> GPT4
    Single --> Claude

    Dual --> LucidAI
    Dual --> Gemini

    Hybrid --> LucidAI
    Hybrid --> Gemini

    Gemini --> Evaluate
    GPT4 --> Evaluate
    Claude --> Evaluate
    LucidAI --> Compare

    Evaluate --> Log
    Compare --> Select
    Select --> Log

    Log --> Return
```

---

## Database Schema

### Entity-Relationship Diagram

```mermaid
erDiagram
    STUDENTS ||--o{ CONVERSATIONS : has
    CONVERSATIONS ||--o{ CONVERSATION_MESSAGES : contains
    CONVERSATIONS ||--o{ LLM_INTERACTIONS : generates
    STUDENTS ||--o{ HPEM_SCORES : tracked_by
    STUDENTS ||--o{ GAMIFICATION_PROGRESS : earns
    STUDENTS ||--o{ BLOCKCHAIN_CREDENTIALS : receives

    LLM_INTERACTIONS ||--o{ TRAINING_EXAMPLES : produces
    TRAINING_EXAMPLES }o--|| DATASET_VERSIONS : belongs_to
    MODEL_VERSIONS ||--o{ LLM_INTERACTIONS : served_by

    STUDENTS {
        uuid id PK
        string name
        int age
        int grade_level
        string learning_style
        json preferences
        timestamp created_at
    }

    CONVERSATIONS {
        uuid id PK
        uuid student_id FK
        string mentor_id
        string subject
        string status
        timestamp created_at
    }

    CONVERSATION_MESSAGES {
        uuid id PK
        uuid conversation_id FK
        string role
        text content
        json metadata
        timestamp created_at
    }

    LLM_INTERACTIONS {
        uuid id PK
        uuid conversation_id FK
        uuid message_id FK
        string task_type
        string risk_level
        json routing_decision
        string llm_used
        string model_version
        text response_text
        json evaluation_scores
        float composite_score
        int inference_time_ms
        float cost_usd
        timestamp created_at
    }

    TRAINING_EXAMPLES {
        uuid id PK
        uuid llm_interaction_id FK
        string anonymous_student_id
        text system_prompt
        text user_message
        text assistant_response
        json labels
        json quality_scores
        json outcome
        string dataset_version
        string split
        timestamp created_at
    }

    MODEL_VERSIONS {
        uuid id PK
        string version UK
        string base_model
        string training_type
        string deployment_status
        float traffic_percentage
        json performance_metrics
        timestamp deployed_at
    }

    HPEM_SCORES {
        uuid id PK
        uuid student_id FK
        string subject
        float proficiency
        float resilience
        float velocity
        float engagement
        float transfer
        float composite
        timestamp calculated_at
    }

    GAMIFICATION_PROGRESS {
        uuid id PK
        uuid student_id FK
        int total_xp
        int level
        json achievements
        int current_streak
        timestamp last_activity
    }

    BLOCKCHAIN_CREDENTIALS {
        uuid id PK
        uuid student_id FK
        string credential_type
        string competency_id
        string stellar_transaction_id
        json metadata
        timestamp issued_at
    }
```

### Key Tables

#### `llm_interactions` (NEW - Critical)

Captures every LLM inference for analysis and training.

```sql
CREATE TABLE llm_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    message_id UUID REFERENCES conversation_messages(id),

    -- Request metadata
    task_type VARCHAR(50),  -- 'tutoring', 'mastery_check', 'creative_writing', etc.
    risk_level VARCHAR(20), -- 'low', 'medium', 'high'

    -- Routing
    routing_decision JSONB,  -- Full RoutingDecision object
    llms_queried TEXT[],     -- ['gemini', 'gpt4']

    -- Response
    llm_used VARCHAR(50),    -- Provider that was selected
    model_version VARCHAR(100),
    response_text TEXT,
    confidence_score FLOAT,

    -- Evaluation
    evaluation_scores JSONB, -- {correctness: 0.95, didactic: 0.87, ...}
    composite_score FLOAT,
    flagged_for_review BOOLEAN DEFAULT FALSE,

    -- Performance
    inference_time_ms INTEGER,
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost_usd NUMERIC(10, 6),

    -- Feedback (optional)
    student_helpful BOOLEAN,
    teacher_rating INTEGER,
    outcome_h_pem_delta FLOAT,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_llm_interactions_conversation ON llm_interactions(conversation_id);
CREATE INDEX idx_llm_interactions_llm_used ON llm_interactions(llm_used);
CREATE INDEX idx_llm_interactions_created_at ON llm_interactions(created_at DESC);
```

#### `training_examples` (NEW)

Anonymized, labeled training data for LucidAI fine-tuning.

```sql
CREATE TABLE training_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    llm_interaction_id UUID REFERENCES llm_interactions(id),

    -- Anonymized student
    anonymous_student_id VARCHAR(64), -- SHA-256 hash

    -- Training data (PII scrubbed)
    system_prompt TEXT,
    user_message TEXT,
    assistant_response TEXT,

    -- Labels
    labels JSONB, -- {subject, grade_level, mentor_persona, h_pem_proficiency, ...}

    -- Quality
    quality_scores JSONB,
    teacher_rating INTEGER,
    outcome JSONB, -- {student_helpful, h_pem_delta, ...}

    -- Dataset management
    dataset_version VARCHAR(50),
    split VARCHAR(20), -- 'train', 'val', 'test'

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_training_examples_dataset_version ON training_examples(dataset_version);
CREATE INDEX idx_training_examples_split ON training_examples(split);
```

#### `model_versions` (NEW)

LucidAI model registry and deployment tracking.

```sql
CREATE TABLE model_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(50) UNIQUE NOT NULL, -- 'lucidai-v1.0'
    base_model VARCHAR(100), -- 'meta-llama/Llama-3-70b-hf'
    training_type VARCHAR(50), -- 'sft', 'rlhf', 'dpo'

    -- Deployment
    deployment_status VARCHAR(20), -- 'testing', 'canary', 'production', 'deprecated'
    traffic_percentage FLOAT DEFAULT 0.0,

    -- Performance (aggregated from llm_interactions)
    performance_metrics JSONB,

    deployed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Chat Endpoint

**POST** `/api/chat`

Main endpoint for student-mentor interactions.

**Request:**

```json
{
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "How do I solve 2x + 3 = 7?",
  "mentor_id": "stella",  // Optional, auto-selected if omitted
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000"  // Optional for new conversation
}
```

**Response:**

```json
{
  "message": "Great question! Let's solve this step by step...",
  "mentor_id": "stella",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "llm_used": "gemini"
}
```

**Status Codes:**
- `200 OK`: Successful response
- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: Server error

#### 2. List Mentors

**GET** `/api/agents`

Returns all available mentor personas.

**Response:**

```json
{
  "mentors": [
    {
      "id": "stella",
      "name": "Stella",
      "subject": "Mathematics"
    },
    {
      "id": "max",
      "name": "Max",
      "subject": "Science"
    },
    // ... 6 more mentors
  ]
}
```

#### 3. Admin Metrics

**GET** `/api/admin/llm-metrics`

LLM performance metrics (requires admin authentication in production).

**Response:**

```json
{
  "total_requests": 1523,
  "by_provider": {
    "gemini": {
      "count": 1245,
      "avg_latency_ms": 1523,
      "avg_cost_usd": 0.0012,
      "avg_composite_score": 0.84
    },
    "gpt4": {
      "count": 178,
      "avg_latency_ms": 2341,
      "avg_cost_usd": 0.0089,
      "avg_composite_score": 0.91
    },
    "lucidai": {
      "count": 100,
      "avg_latency_ms": 1876,
      "avg_cost_usd": 0.0,
      "avg_composite_score": 0.88
    }
  },
  "evaluation_summary": {
    "avg_correctness": 0.89,
    "avg_didactic_quality": 0.82,
    "avg_safety": 0.97
  }
}
```

#### 4. Health Check

**GET** `/health`

Service health status.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-11-22T10:30:00Z",
  "version": "0.1.0"
}
```

---

## Module Reference

### Configuration

**`backend/app/config.py`**

Pydantic Settings-based configuration management.

**Key Settings:**

```python
class Settings(BaseSettings):
    # App
    app_name: str = "Stellecta LucidAI Backend"
    app_version: str = "0.1.0"
    app_debug: bool = False

    # Database
    database_url: str = "postgresql://user:pass@localhost/stellecta"

    # LLM Providers
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    lucidai_api_url: Optional[str] = None
    lucidai_api_key: Optional[str] = None

    # Routing
    routing_mode: str = "hybrid"  # single | dual | hybrid
    default_llm: str = "gemini"
    enable_lucidai: bool = False
    lucidai_traffic_pct: float = 0.1

    # Evaluation
    evaluation_correctness_weight: float = 0.3
    evaluation_didactic_weight: float = 0.3
    evaluation_persona_weight: float = 0.2
    evaluation_safety_weight: float = 0.1
    evaluation_curriculum_weight: float = 0.1
    evaluation_min_composite_score: float = 0.6

    # H-PEM
    hpem_proficiency_weight: float = 0.35
    hpem_resilience_weight: float = 0.15
    hpem_velocity_weight: float = 0.15
    hpem_engagement_weight: float = 0.20
    hpem_transfer_weight: float = 0.15
```

**Usage:**

```python
from app.config import get_settings

settings = get_settings()
print(settings.database_url)
```

### Database

**`backend/app/database/engine.py`**

SQLAlchemy engine and session management.

**Usage:**

```python
from app.database.engine import get_db

@router.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter_by(id=request.student_id).first()
    # ...
```

### Models

**`backend/app/database/models/`**

SQLAlchemy ORM models for all tables.

**Example:**

```python
from app.database.models.student import Student
from app.database.models.conversation import Conversation
from app.database.models.llm_interaction import LLMInteraction

# Query
students = db.query(Student).filter(Student.grade_level == 7).all()
```

### LLM Schemas

**`backend/app/llm/schemas.py`**

Pydantic models for LLM interactions.

**Key Schemas:**

```python
class LLMRequest(BaseModel):
    system_prompt: str
    user_message: str
    conversation_context: Optional[List[Dict[str, str]]] = []
    temperature: float = 0.7
    max_tokens: int = 1000

class LLMResponse(BaseModel):
    content: str
    llm_provider: str
    model_version: str
    confidence_score: Optional[float] = None
    tokens_input: int = 0
    tokens_output: int = 0
    inference_time_ms: float = 0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = {}

class RouterResponse(BaseModel):
    message: str
    llm_used: str
    model_version: str
    routing_decision: RoutingDecision
    evaluation: EvaluationResult
    metadata: Dict[str, Any]
```

---

## Setup Guide

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+**
- **Redis** (optional, for caching)

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/your-org/stellar-ai-mentor.git
cd stellar-ai-mentor/backend
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Database
DATABASE_URL=postgresql://stellecta_user:password@localhost:5432/stellecta_db

# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional

# Routing (Phase 0: LucidAI disabled)
ROUTING_MODE=single
DEFAULT_LLM=gemini
ENABLE_LUCIDAI=false
```

#### 5. Initialize Database

```bash
# Create database
createdb stellecta_db

# Run migrations
alembic upgrade head
```

#### 6. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# List mentors
curl http://localhost:8000/api/agents

# Test chat (requires valid student_id in database)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What is photosynthesis?",
    "mentor_id": "max"
  }'
```

---

## Testing Strategy

### Test Suite Structure

```
backend/tests/
├── unit/
│   ├── test_evaluation.py
│   ├── test_router.py
│   ├── test_policies.py
│   ├── test_mentor_engine.py
│   └── test_providers.py
├── integration/
│   ├── test_supervisor_flow.py
│   ├── test_training_pipeline.py
│   └── test_database.py
└── e2e/
    └── test_chat_endpoint.py
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific module
pytest tests/unit/test_router.py -v

# Watch mode (for development)
pytest-watch
```

### Key Test Cases

#### 1. Multi-LLM Router

```python
@pytest.mark.asyncio
async def test_router_single_mode():
    """Test single LLM execution mode."""
    router = MultiLLMRouter()
    request = LLMRequest(
        system_prompt="You are a math tutor.",
        user_message="What is 2+2?",
    )
    response = await router.generate(request, context={})

    assert response.message is not None
    assert response.llm_used in ["gemini", "gpt4", "claude"]
    assert response.evaluation.composite_score > 0

@pytest.mark.asyncio
async def test_router_dual_mode():
    """Test dual LLM execution with comparison."""
    # ... test dual mode
```

#### 2. Evaluation Service

```python
@pytest.mark.asyncio
async def test_evaluation_dimensions():
    """Test all 5 evaluation dimensions."""
    eval_service = EvaluationService()
    response = LLMResponse(content="Test response", ...)

    result = await eval_service.evaluate_single(response, context={})

    assert 0 <= result.correctness <= 1
    assert 0 <= result.didactic_quality <= 1
    assert 0 <= result.persona_alignment <= 1
    assert 0 <= result.safety <= 1
    assert 0 <= result.curriculum_alignment <= 1
```

#### 3. Supervisor Agent

```python
@pytest.mark.asyncio
async def test_supervisor_safety_check():
    """Test safety filtering."""
    supervisor = SupervisorAgent()

    # Harmful request
    result = await supervisor.process_conversation(
        request={"message": "How to build a bomb?"},
        student_context={},
        conversation_context=[]
    )

    assert result["escalate_to_teacher"] is True
    assert "safety" in result["reason"].lower()
```

---

## Deployment

### Production Checklist

- [ ] Set `APP_DEBUG=false` in `.env`
- [ ] Configure production database with SSL
- [ ] Set up Redis for caching
- [ ] Enable rate limiting
- [ ] Configure CORS origins
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure structured logging to external service
- [ ] Enable API authentication
- [ ] Set up backup strategy for database
- [ ] Configure CDN for static assets (if applicable)
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up health check endpoints for load balancer
- [ ] Configure auto-scaling policies

### Docker Deployment

**`Dockerfile`:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker-compose.yml`:**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://stellecta:password@db:5432/stellecta
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=stellecta
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=stellecta
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Run:**

```bash
docker-compose up -d
```

### Environment Variables for Production

```bash
# App
APP_NAME=Stellecta LucidAI Backend
APP_VERSION=0.1.0
APP_DEBUG=false

# Database (use connection pooling)
DATABASE_URL=postgresql://user:pass@db-host:5432/stellecta?sslmode=require

# Redis
REDIS_URL=redis://redis-host:6379/0

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://stellecta.com,https://app.stellecta.com

# LLM Providers
GEMINI_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
LUCIDAI_API_URL=https://lucidai-api.stellecta.internal
LUCIDAI_API_KEY=...

# Routing (Production: Enable LucidAI with gradual rollout)
ROUTING_MODE=hybrid
DEFAULT_LLM=gemini
ENABLE_LUCIDAI=true
LUCIDAI_TRAFFIC_PCT=0.1  # Start with 10%

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

## Future Roadmap

### Phase 1: Full Business Logic (Q1 2026)

- [ ] Complete LVO Engine implementation
  - Adaptive learn phase with spaced repetition
  - Calibrated mastery verification
  - Transfer tasks and authentic assessments

- [ ] Full H-PEM Calculator
  - Real-time proficiency tracking from assessments
  - Resilience scoring from challenge persistence
  - Velocity calculation from learning speed
  - Engagement metrics from session data
  - Transfer scoring from cross-domain application

- [ ] Gamification Mechanics
  - XP formula based on H-PEM gains
  - Achievement badge system
  - Streak tracking with notifications
  - Leaderboards (privacy-preserving)

### Phase 2: LucidAI Production (Q2 2026)

- [ ] LucidAI Provider Implementation
  - HTTP client to LucidAI inference service
  - Model versioning and A/B testing
  - Confidence calibration

- [ ] Fine-Tuning Pipeline
  - Automated dataset curation from training_examples
  - Instruction-tuning with Llama 3 70B base
  - RLHF integration with teacher feedback
  - Model evaluation benchmarks

- [ ] Gradual Rollout
  - 10% → 25% → 50% → 100% traffic migration
  - Monitoring and rollback procedures
  - Performance comparison dashboards

### Phase 3: Advanced Features (Q3 2026)

- [ ] Blockchain Integration
  - Stellar credential minting
  - Verifiable competency badges
  - Decentralized student portfolios

- [ ] Advanced Evaluation
  - External evaluator LLM (GPT-4 as judge)
  - Automated rubric scoring
  - Multi-turn conversation quality

- [ ] Real-Time Adaptation
  - Streaming LLM responses
  - Live proficiency updates
  - Dynamic difficulty adjustment

### Phase 4: Scale & Optimization (Q4 2026)

- [ ] Performance Optimization
  - Response caching (Redis)
  - Prompt caching for LLMs
  - Database query optimization
  - CDN for static content

- [ ] Advanced Monitoring
  - Real-time dashboards (Grafana)
  - Alerting (PagerDuty)
  - Cost tracking per student/subject

- [ ] Multi-Tenancy
  - School district isolation
  - Custom mentor personas per district
  - White-label deployment

---

## Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **H-PEM** | Holistic Pedagogical Engagement Metrics - 5D student progress tracking |
| **LVO** | Learn-Verify-Own - Pedagogical cycle for deep learning |
| **Multi-LLM** | Architecture using multiple LLM providers with intelligent routing |
| **LucidAI** | Stellecta's proprietary fine-tuned LLM for education |
| **Routing Policy** | Decision tree for selecting appropriate LLM(s) based on context |
| **Composite Score** | Weighted average of 5 evaluation dimensions (0-1) |
| **Mentor Persona** | AI tutor character with specific subject expertise and teaching style |
| **Supervisor Agent** | Top-level orchestrator for safety, mentor selection, quality validation |

### B. Configuration Reference

See `.env.example` for full list of environment variables.

### C. API Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Invalid request format | Check request schema |
| 401 | Unauthorized | Provide valid API key |
| 404 | Resource not found | Verify student_id/conversation_id exists |
| 429 | Rate limit exceeded | Reduce request frequency |
| 500 | Internal server error | Check logs, contact support |
| 503 | LLM provider unavailable | Wait and retry, fallback active |

### D. Support

- **Documentation**: https://docs.stellecta.com
- **Issues**: https://github.com/your-org/stellar-ai-mentor/issues
- **Email**: support@stellecta.com

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22
**Maintained By:** Stellecta Engineering Team
