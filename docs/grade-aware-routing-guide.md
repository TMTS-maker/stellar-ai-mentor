# Grade-Aware Agent Routing System

## Overview

The Stellecta AI Mentor platform now supports **grade-based routing and instruction** for students from **Grade 1 (age 6) through Grade 12 (age 17-18)**. This extension ensures that all 8 mentors can adapt their teaching to younger learners while maintaining pedagogical rigor.

---

## Grade Band System

The system organizes learning into **four grade bands**, each with distinct pedagogical characteristics:

| Grade Band | Grades | Typical Age | Developmental Stage |
|------------|--------|-------------|---------------------|
| **G1-2** | 1-2 | 6-7 years | Early Elementary |
| **G3-4** | 3-4 | 8-9 years | Upper Elementary |
| **G5-8** | 5-8 | 10-13 years | Middle School |
| **G9-12** | 9-12 | 14-17 years | High School |

---

## Mentor Grade Coverage

Each mentor supports specific grade bands based on when their subject is typically introduced:

| Mentor | Subject | Grade Coverage | Rationale |
|--------|---------|----------------|-----------|
| **Stella** 📐 | Mathematics | G1-12 | Math taught from kindergarten onward |
| **Lexis** 📚 | English & Literature | G1-12 | Reading/writing starts in Grade 1 |
| **Luna** 🎨 | Arts & Music | G1-12 | Creative expression for all ages |
| **Darwin** 🧬 | Biology | G3-12 | Life science introduced in elementary |
| **Atlas** 🗺️ | History & Geography | G3-12 | Social studies starts Grade 3-4 |
| **Max** ⚛️ | Physics | G5-12 | Physics concepts in middle school |
| **Nova** 🧪 | Chemistry | G5-12 | Chemistry in middle school science |
| **Neo** 🤖 | AI & Technology | G5-12 | Coding/tech literacy from upper elementary |

---

## Grade-Specific Topic Scope

Each mentor has detailed topic mappings per grade band. See `backend/app/agents/config/mentor_grade_profiles.py` for the complete configuration.

### Example: Stella (Mathematics)

**G1-2 (Early Elementary)**:
- Counting and number recognition (0-100)
- Basic addition and subtraction (within 20)
- Place value (ones, tens)
- Simple shapes and patterns
- Measuring length and time

**G3-4 (Upper Elementary)**:
- Multiplication and division (basic facts)
- Fractions (halves, thirds, fourths)
- Place value to thousands
- Area and perimeter
- Basic graphs

**G5-8 (Middle School)**:
- Fractions, decimals, percentages
- Ratios and proportions
- Algebra basics (variables, expressions)
- Geometry (angles, area, volume)
- Statistics and probability

**G9-12 (High School)**:
- Algebra (linear, quadratic, exponential)
- Geometry proofs and trigonometry
- Calculus (limits, derivatives, integrals)
- Advanced statistics
- Problem-solving and mathematical communication

---

## How Grade-Aware Routing Works

### 1. Student Context with Grade

When a student provides their grade, the system uses it for routing:

```json
{
  "message": "Help me with addition",
  "student_context": {
    "grade": 1,
    "language": "English"
  }
}
```

### 2. Grade-to-Age Mapping

The system maps grades to ages:
- Grade 1 → Age 6
- Grade 2 → Age 7
- ...
- Grade 12 → Age 17

Function: `grade_to_age()` in `backend/app/agents/schemas.py`

### 3. Mentor Recommendations

The supervisor uses `get_recommended_mentors_for_grade()` to filter appropriate mentors:

```python
# For Grade 1 math question:
recommended = ["luna", "lexis", "stella"]

# For Grade 7 physics:
recommended = ["max", "nova", "darwin"]
```

### 4. Grade-Specific Prompt Adaptation

Each mentor's system prompt includes grade-band-specific guidance:

```
4. **Differentiation by Grade/Age**
   - **Grades 1-2 (ages 6-7)**: Very simple language. Use concrete examples...
   - **Grades 3-4 (ages 8-9)**: Introduce abstract concepts gradually...
   - **Grades 5-8 (ages 10-13)**: Transition to formal reasoning...
   - **Grades 9-12 (ages 14-17)**: Advanced topics, college preparation...
```

The mentor engine injects the student's grade into the context:

```
Student grade: 2 (G1-2)
```

---

## API Changes

### GET /api/chat/mentors

Now returns grade ranges:

```json
{
  "id": "stella",
  "display_name": "Stella",
  "subjects": ["Mathematics", ...],
  "age_range": "6-18",
  "grade_range": "G1-12",  // NEW
  ...
}
```

### POST /api/chat/message

StudentContext now accepts `grade`:

```json
{
  "mentor_id": "stella",
  "message": "What is 2 + 2?",
  "student_context": {
    "grade": 1,  // NEW - optional field (1-12)
    "age": 6,
    "skill_level": "beginner"
  }
}
```

**Backward Compatibility**:
- `grade` is **optional**
- If only `age` is provided, routing works as before
- If `grade` is provided, it takes priority for pedagogical adaptation

---

## Pedagogical Adaptations by Grade Band

### G1-2 (Early Elementary)

**Language**:
- Very simple, short sentences
- Concrete vocabulary (blocks, counters, pictures)
- Avoid abstract terms

**Methods**:
- Hands-on examples and visual aids
- Short, focused sessions (5-10 min attention span)
- Lots of positive reinforcement

**Safety**:
- Age-appropriate content only
- Extra encouragement and patience

### G3-4 (Upper Elementary)

**Language**:
- Simple but slightly more complex
- Introduce subject-specific terms gradually

**Methods**:
- Visual models and relatable word problems
- More scaffolding, step-by-step guidance
- Encourage self-expression and creativity

### G5-8 (Middle School)

**Language**:
- Academic vocabulary appropriate for age
- Introduce formal notation

**Methods**:
- Transition to abstract thinking
- Connect to real-world applications
- Encourage multiple solution strategies
- Foster independence

### G9-12 (High School)

**Language**:
- Formal academic language
- Subject-specific terminology

**Methods**:
- College-preparatory rigor
- Advanced problem-solving
- Prepare for standardized tests (SAT, ACT, AP exams)
- Critical thinking and analysis

---

## Implementation Files

### Core Files

1. **`backend/app/agents/schemas.py`**
   - `StudentContext.grade` field (1-12)
   - `grade_to_age()` mapping function
   - `MentorPersona.grade_min` and `grade_max` fields

2. **`backend/app/agents/config/mentor_grade_profiles.py`**
   - Complete grade band profiles for all 8 mentors
   - Topic scope per grade band
   - Didactic notes for each band
   - `get_recommended_mentors_for_grade()` function

3. **`backend/app/agents/supervisor.py`**
   - `_get_grade_aware_recommendations()` method
   - Grade information in supervisor prompt
   - Pre-filtering mentors based on grade

4. **`backend/app/agents/mentor_engine.py`**
   - Grade information injected into mentor context
   - Grade band displayed to mentor ("Student grade: 3 (G3-4)")

5. **`backend/app/agents/personas.py`**
   - All 8 mentor prompts updated with grade-band guidance
   - Differentiation sections restructured

---

## Testing Grade-Aware Routing

### Unit Tests

See `backend/tests/unit/test_agents.py` for tests including:

```python
def test_grade_routing_early_elementary():
    """Test that Grade 1 student gets age-appropriate mentors."""
    # Grade 1 math should route to Stella with G1-2 awareness
    pass

def test_grade_to_age_mapping():
    """Test grade-to-age conversion."""
    assert grade_to_age(1) == 6
    assert grade_to_age(12) == 17
```

### Manual Testing

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Test Grade 1 student
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Help me count to 10",
    "student_context": {"grade": 1}
  }'

# Test Grade 9 student
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quadratic equations",
    "student_context": {"grade": 9}
  }'
```

---

## Future Enhancements

1. **ML-Based Grade Detection**
   - Automatically infer grade from question complexity

2. **Adaptive Grade Progression**
   - Track when a student is ready for next-grade content

3. **Cross-Grade Projects**
   - Multi-mentor collaboration for interdisciplinary topics

4. **Parent/Teacher Grade Override**
   - Allow manual adjustment if student is advanced/behind

5. **Localized Grade Systems**
   - Support for non-US grade systems (Year 1-13 in UK, etc.)

---

## Summary

✅ **All 8 mentors now support Grades 1-12**
✅ **Grade-aware routing with subject + grade matching**
✅ **Detailed topic scope per grade band**
✅ **Backward-compatible (age-only routing still works)**
✅ **Pedagogically grounded adaptations for each band**
✅ **Clean API with `grade` field in StudentContext**

The Stellecta platform can now serve **elementary school students (G1-4)** with the same pedagogical rigor as middle and high schoolers!
