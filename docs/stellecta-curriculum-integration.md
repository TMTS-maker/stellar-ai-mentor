# Stellecta Curriculum Integration

Complete backend infrastructure for multi-curriculum support, learning competency tracking, and personalized learning pathways.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Supported Curricula](#supported-curricula)
4. [Database Schema](#database-schema)
5. [Curriculum Providers](#curriculum-providers)
6. [LCT (Learning Competency Trajectories)](#lct-learning-competency-trajectories)
7. [API Endpoints](#api-endpoints)
8. [Integration with Agents](#integration-with-agents)
9. [Usage Examples](#usage-examples)
10. [Adding New Curricula](#adding-new-curricula)

---

## Overview

The Stellecta curriculum integration layer provides:

- **Multi-curriculum support**: Indian (CBSE/ICSE), UK (National/IGCSE), US (Common Core)
- **Structured learning**: Hierarchical organization (Curriculum → Subject → Unit → Topic → Learning Objective)
- **LCT tracking**: Student competency progression through curriculum objectives
- **Personalized learning**: Gap analysis, prerequisite checking, smart recommendations
- **H-PEM integration**: Spaced repetition, practice tracking, evaluation scoring
- **LVO mapping**: Learning objectives tagged with LVO phase emphasis
- **Agent integration**: Curriculum context injected into mentor prompts

---

## Architecture

### Component Layers

```
┌─────────────────────────────────────────────────┐
│           FastAPI REST API Layer                │
│    /api/curriculum/* endpoints                  │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Service & Business Logic                │
│  - CurriculumService (CRUD, ingestion)          │
│  - LCTEngine (trajectories, recommendations)    │
│  - Context Builder (agent integration)          │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Provider Abstraction Layer              │
│  - BaseCurriculumProvider                       │
│  - IndianCurriculumProvider (CBSE/ICSE)         │
│  - UKCurriculumProvider (National/IGCSE)        │
│  - USCurriculumProvider (Common Core/NGSS)      │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│           Data Sources                          │
│  - Static JSON files (data/curricula/)          │
│  - Future: REST APIs, MCP servers               │
└─────────────────────────────────────────────────┘
```

### Database Schema Hierarchy

```
Curriculum
    └── CurriculumVersion (e.g., "2023-24")
            └── GradeBand (e.g., "Secondary 9-10")
                    └── Subject (e.g., "Mathematics")
                            └── Unit (e.g., "Polynomials")
                                    └── Topic (e.g., "Factorization")
                                            └── LearningObjective (e.g., "Apply factor theorem")

School → Curriculum + CurriculumVersion
Student → School + Grade + Subjects

CompetencyRecord → Student + LearningObjective
    (tracks mastery_level, status, practice_count, etc.)
```

---

## Supported Curricula

### Indian Curricula

**Provider**: `indian`

| Code | Name | Grades | Description |
|------|------|--------|-------------|
| `CBSE` | Central Board of Secondary Education | 1-12 | National curriculum board, widely adopted across India |
| `ICSE` | Indian Certificate of Secondary Education | 1-12 | Private board emphasizing comprehensive education |

**Grade Bands**:
- Primary (1-5)
- Upper Primary (6-8)
- Secondary (9-10)
- Senior Secondary (11-12)

### UK Curricula

**Provider**: `uk`

| Code | Name | Grades | Description |
|------|------|--------|-------------|
| `UK_NATIONAL` | UK National Curriculum (England) | 1-11 | Statutory curriculum for state schools in England |
| `IGCSE` | International GCSE | 10-11 | International version of GCSE |
| `A_LEVEL` | A-Level | 12-13 | Advanced Level qualifications |

**Grade Bands** (Key Stages):
- KS1 (Grades 1-2, Ages 5-7)
- KS2 (Grades 3-6, Ages 7-11)
- KS3 (Grades 7-9, Ages 11-14)
- KS4 (Grades 10-11, Ages 14-16)
- KS5 (Grades 12-13, Ages 16-18)

### US Curricula

**Provider**: `us`

| Code | Name | Grades | Description |
|------|------|--------|-------------|
| `COMMON_CORE` | Common Core State Standards | 1-12 | National standards for Math and ELA |
| `NGSS` | Next Generation Science Standards | 1-12 | National science education standards |

**Grade Bands**:
- Elementary School (1-5)
- Middle School (6-8)
- High School (9-12)

---

## Database Schema

### Core Models

#### Curriculum
```python
class Curriculum(Base):
    id: int
    code: str  # "CBSE", "UK_NATIONAL", "COMMON_CORE"
    name: str
    country_code: str  # "IND", "GBR", "USA"
    provider_type: str  # "indian", "uk", "us"
    created_at: datetime
    updated_at: datetime
```

#### School
```python
class School(Base):
    id: int
    name: str
    country_code: str
    curriculum_id: int (FK)
    curriculum_version_id: int (FK)
    timezone: str
```

#### Student
```python
class Student(Base):
    id: int
    user_id: int (FK)
    school_id: int (FK)
    grade: int  # 1-12
    section: str  # "A", "B", etc.
    current_subjects: JSON  # [subject_ids]
    mastered_objectives: JSON  # [objective_ids]
    in_progress_objectives: JSON  # [objective_ids]
```

#### LearningObjective
```python
class LearningObjective(Base):
    id: int
    topic_id: int (FK)
    code: str  # "CBSE.G9.MATH.ALG.LO.001"
    description: str
    cognitive_level: str  # Bloom's taxonomy
    lvo_phase_emphasis: str  # "learn", "verify", "own"
```

#### CompetencyRecord (LCT)
```python
class CompetencyRecord(Base):
    id: int
    student_id: int (FK)
    objective_id: int (FK)
    status: str  # "not_started", "in_progress", "mastered", "needs_review"
    mastery_level: int  # 0-100
    practice_count: int
    last_practiced_at: datetime
    evaluation_score: int  # 0-100
    started_at: datetime
    mastered_at: datetime
```

---

## Curriculum Providers

### Provider Interface

All providers implement `BaseCurriculumProvider`:

```python
class BaseCurriculumProvider(ABC):
    async def fetch_curriculum(
        self, curriculum_code: str, version_code: Optional[str]
    ) -> CurriculumData

    async def validate_curriculum_structure(
        self, data: CurriculumData
    ) -> bool

    async def get_available_curricula(
        self
    ) -> List[Dict[str, str]]

    def map_to_mentor(
        self, subject_code: str
    ) -> Optional[str]
```

### Subject-to-Mentor Mapping

| Subject Code | Recommended Mentor |
|--------------|-------------------|
| MATH, MATHEMATICS | Stella 📐 |
| PHYSICS | Max ⚛️ |
| CHEMISTRY, SCIENCE | Nova 🔬 |
| BIOLOGY, LIFE_SCIENCE | Darwin 🧬 |
| ENGLISH, LANGUAGE_ARTS | Lexis 📚 |
| COMPUTER_SCIENCE, COMPUTING | Neo 💻 |
| ART, ARTS, MUSIC | Luna 🎨 |
| GEOGRAPHY, HISTORY, SOCIAL_STUDIES | Atlas 🌍 |

---

## LCT (Learning Competency Trajectories)

### What is LCT?

LCT tracks student progression through curriculum learning objectives, providing:

1. **Competency Status Tracking**: not_started → in_progress → mastered → needs_review
2. **Mastery Level**: 0-100% proficiency score
3. **Learning Gaps**: Objectives with unmastered prerequisites
4. **Smart Recommendations**: Next objectives where prerequisites are met
5. **Spaced Repetition**: Objectives needing review based on practice dates
6. **Progression Analytics**: Objectives mastered per week, trajectory charts

### LCTEngine Methods

```python
from app.lct.trajectories import LCTEngine

engine = LCTEngine(db_session)

# Get student's learning trajectory
trajectory = engine.get_trajectory(
    student_id=123,
    subject_code="MATH",  # Optional filter
    timeframe_days=90
)
# Returns: {
#     "mastered_count": 25,
#     "in_progress_count": 5,
#     "progression_rate": 2.5,  # objectives/week
#     "learning_gaps": [...],
#     "recommended_next": [...],
#     "trajectory_chart": {...}
# }

# Update student competency
record = engine.update_competency(
    student_id=123,
    objective_id=456,
    mastery_level=85,
    status="mastered",
    evaluation_score=90
)

# Check prerequisites
prereq_check = engine.check_prerequisite_mastery(
    student_id=123,
    objective_id=456
)
# Returns: {
#     "prerequisites_met": True,
#     "readiness_score": 100,
#     "missing": []
# }

# Get review suggestions (spaced repetition)
review_objectives = engine.suggest_review_objectives(
    student_id=123,
    days_since_practice=14
)
```

---

## API Endpoints

### Curriculum Management

#### GET `/api/curriculum/curricula`
List all available curricula.

**Response**:
```json
[
    {
        "id": 1,
        "code": "CBSE",
        "name": "Central Board of Secondary Education",
        "country_code": "IND",
        "provider_type": "indian"
    }
]
```

#### POST `/api/curriculum/ingest`
Ingest curriculum from a provider.

**Request**:
```json
{
    "provider_type": "indian",
    "curriculum_code": "CBSE",
    "version_code": "2023-24"
}
```

**Response**: Created curriculum object

#### GET `/api/curriculum/objectives?curriculum_id={id}&grade={grade}&subject_code={code}`
Get learning objectives for a grade and subject.

### LCT Endpoints

#### GET `/api/curriculum/student/{student_id}/trajectory`
Get student's learning trajectory.

**Query Parameters**:
- `subject_code` (optional): Filter by subject
- `timeframe_days` (optional, default 90): Timeframe for analysis

**Response**:
```json
{
    "student_id": 123,
    "timeframe_days": 90,
    "mastered_count": 25,
    "in_progress_count": 5,
    "needs_review_count": 3,
    "progression_rate": 2.5,
    "learning_gaps": [
        {
            "objective_id": 10,
            "objective_code": "CBSE.G9.MATH.U02.T03.LO001",
            "objective_name": "Apply the factor theorem...",
            "missing_prerequisites": [...]
        }
    ],
    "recommended_next": [
        {
            "id": 15,
            "code": "CBSE.G9.MATH.U03.T01.LO001",
            "description": "Understand linear equations...",
            "cognitive_level": "understand",
            "lvo_phase_emphasis": "learn",
            "difficulty": "foundational"
        }
    ]
}
```

#### POST `/api/curriculum/student/{student_id}/competency`
Update student competency for an objective.

**Request**:
```json
{
    "objective_id": 15,
    "mastery_level": 85,
    "status": "mastered",
    "evaluation_score": 90
}
```

#### GET `/api/curriculum/student/{student_id}/recommendations`
Get recommended next objective for student.

#### GET `/api/curriculum/student/{student_id}/review`
Get objectives needing review (spaced repetition).

**Query Parameters**:
- `days_since_practice` (optional, default 14): Review threshold

#### GET `/api/curriculum/student/{student_id}/gaps`
Identify learning gaps (missing prerequisites).

---

## Integration with Agents

### Curriculum Context in Mentor Prompts

The curriculum system integrates with the mentor engine to provide context-aware mentoring:

```python
from app.curriculum.context_builder import build_curriculum_context

# Build curriculum context for a student
curriculum_context = build_curriculum_context(
    db=db_session,
    student_id=123,
    subject_code="MATH"
)

# Use in mentor chat
from app.agents.mentor_engine import get_mentor_engine

engine = get_mentor_engine()
response = await engine.chat(
    mentor_id="stella",
    message="I need help with polynomials",
    student_context=student_context,
    curriculum_context=curriculum_context  # Injected here
)
```

### Context String Example

```
=== CURRICULUM & LEARNING TRAJECTORY ===
Curriculum: Central Board of Secondary Education (CBSE, IND)
Objectives mastered: 25
Objectives in progress: 5
Learning pace: 2.5 objectives/week
⚠️ Learning gaps identified: 1 (prerequisites not mastered)
   - Working on: CBSE.G9.MATH.U02.T03.LO001 but missing prerequisites

Recommended next objectives:
   - CBSE.G9.MATH.U03.T01.LO001: Understand what constitutes a linear equation... [understand, learn phase]
   - CBSE.G9.MATH.U03.T01.LO002: Determine if a given pair of values is a solution... [apply, verify phase]

📚 Objectives needing review (not practiced in 14+ days): 3
   - CBSE.G9.MATH.U01.T01.LO002: Identify rational and irrational numbers...
```

This context helps mentors:
- **Personalize instruction** based on student's current learning state
- **Address gaps** by focusing on missing prerequisites
- **Suggest practice** for objectives needing review
- **Align difficulty** with student's progression rate
- **Map to LVO phases** using objective emphasis tags

---

## Usage Examples

### Example 1: Ingest CBSE Curriculum

```bash
curl -X POST http://localhost:8000/api/curriculum/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "provider_type": "indian",
    "curriculum_code": "CBSE",
    "version_code": "2023-24"
  }'
```

### Example 2: Get Student Trajectory

```bash
curl http://localhost:8000/api/curriculum/student/123/trajectory?subject_code=MATH
```

### Example 3: Update Student Competency

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/curriculum/student/123/competency",
    json={
        "objective_id": 456,
        "mastery_level": 90,
        "status": "mastered",
        "evaluation_score": 95
    }
)
```

### Example 4: Get Learning Gaps

```bash
curl http://localhost:8000/api/curriculum/student/123/gaps?subject_code=MATH
```

### Example 5: Chat with Curriculum Context

```python
from app.database.session import get_db
from app.curriculum.context_builder import build_curriculum_context
from app.agents.mentor_engine import get_mentor_engine
from app.agents.schemas import StudentContext

db = next(get_db())

# Build contexts
student_context = StudentContext(grade=9, age=14)
curriculum_context = build_curriculum_context(db, student_id=123, subject_code="MATH")

# Chat with mentor
engine = get_mentor_engine()
response = await engine.chat(
    mentor_id="stella",
    message="Can you help me with factorization?",
    student_context=student_context,
    curriculum_context=curriculum_context
)

print(response.message)
```

---

## Adding New Curricula

To add a new curriculum:

### 1. Create Curriculum Data File

Create `data/curricula/{provider}/{curriculum_code}.json`:

```json
{
  "name": "New Curriculum Name",
  "current_version": "2024",
  "country_code": "XXX",
  "description": "...",
  "grade_bands": [...],
  "subjects": [...],
  "units": [...],
  "topics": [...],
  "learning_objectives": [...]
}
```

### 2. Create or Update Provider

If using a new provider, create `backend/app/curriculum/providers/new_provider.py`:

```python
from .base import BaseCurriculumProvider, CurriculumData

class NewCurriculumProvider(BaseCurriculumProvider):
    def __init__(self, config):
        super().__init__(config)
        self.provider_type = "new_provider"
        self.supported_curricula = ["NEW_CURRICULUM"]

    async def fetch_curriculum(self, curriculum_code, version_code=None):
        # Implementation
        pass

    # Implement other abstract methods...
```

### 3. Register Provider

In `backend/app/curriculum/service.py`:

```python
def _register_providers(self):
    # ... existing providers
    self.providers["new_provider"] = NewCurriculumProvider(
        {"data_path": "data/curricula/new_provider"}
    )
```

### 4. Ingest Curriculum

```bash
curl -X POST http://localhost:8000/api/curriculum/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "provider_type": "new_provider",
    "curriculum_code": "NEW_CURRICULUM"
  }'
```

---

## Best Practices

1. **LCT Updating**: Update competency records after every practice session, quiz, or assessment
2. **Prerequisite Checks**: Always check prerequisites before starting a new objective
3. **Spaced Repetition**: Use review suggestions to maintain mastery
4. **Gap Analysis**: Address learning gaps before moving to dependent objectives
5. **Curriculum Context**: Always provide curriculum context to mentors for personalized instruction
6. **LVO Mapping**: Use objective's `lvo_phase_emphasis` to align with appropriate learning phase
7. **H-PEM Integration**: Track practice_count and last_practiced_at for spaced repetition

---

## Future Enhancements

- **ML-based Gap Prediction**: Predict future learning gaps before they occur
- **Adaptive Difficulty**: Adjust objective difficulty based on student performance
- **Peer Comparison**: Anonymous benchmarking against grade-level peers
- **Curriculum APIs**: Direct integration with official curriculum APIs (NCERT, DfE, etc.)
- **MCP Server Support**: Fetch curricula from MCP servers
- **Custom Curricula**: Allow schools to define custom curricula
- **Cross-curricular Mapping**: Map objectives across different curriculum families
- **Competency Badges**: Award badges for mastering objective clusters
- **Parent Dashboards**: LCT visualization for parents

---

## Support

For questions or issues with curriculum integration:
- Check API documentation: `http://localhost:8000/docs`
- Review test suite: `backend/tests/unit/test_curriculum.py`
- Examine sample data: `data/curricula/`

**Version**: 1.0.0
**Last Updated**: November 2025
