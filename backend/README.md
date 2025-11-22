# Stellar AI Mentor - Backend

Gold-standard pedagogical AI mentoring platform built with FastAPI.

---

## 🌟 Features

- **8 Specialized AI Mentors**: Stella (Math), Max (Physics), Nova (Chemistry), Darwin (Biology), Lexis (English), Neo (AI/Tech), Luna (Arts), Atlas (History)
- **Supervisor Agent**: Intelligent routing to the right mentor
- **Gold-Standard Pedagogy**: Research-backed teaching principles (growth mindset, scaffolding, differentiation, SEL)
- **Socratic Method**: Question-first, guided discovery approach
- **LVO Framework**: Learn-Verify-Own pedagogical phases
- **H-PEM Integration**: History-Practice-Evaluation-Metacognition
- **Multi-LLM Support**: OpenAI, Anthropic Claude, Google Gemini, LucidAI (stub)
- **Gamification**: XP, achievements, levels, streaks
- **Multi-Language Ready**: English default, prepared for localization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or uv package manager
- (Optional) PostgreSQL for database

### Installation

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Edit .env and add your API keys
# Required: At least one LLM provider API key (OpenAI, Anthropic, or Gemini)
nano .env  # or use your preferred editor
```

### Configuration

Edit `.env` file:

```bash
# Required: Add at least one LLM provider API key
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
# OR
GOOGLE_API_KEY=your-google-api-key-here

# Set default provider
DEFAULT_LLM_PROVIDER=openai  # or anthropic, gemini

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite+aiosqlite:///./stellar.db

# CORS (adjust for your frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Run the Server

```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the convenience script
python -m app.main
```

Server will start at: **http://localhost:8000**

API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 API Documentation

### Endpoints

#### 1. Get All Mentors
```http
GET /api/chat/mentors
```

Returns list of all 8 mentors with metadata.

**Response**:
```json
[
  {
    "id": "stella",
    "display_name": "Stella",
    "emoji": "📐",
    "subjects": ["Mathematics", "Algebra", "Geometry", "Calculus"],
    "age_range": "12-18",
    "personality_traits": ["Analytical", "Patient", "Encouraging"],
    "teaching_style": "socratic",
    "description": "Your mathematical guide..."
  },
  ...
]
```

#### 2. Get Mentor Details
```http
GET /api/chat/mentors/{mentor_id}
```

Get detailed information about a specific mentor.

#### 3. Send Message (with Supervisor Routing)
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "What is photosynthesis?",
  "student_context": {
    "age": 14,
    "skill_level": "beginner",
    "language": "English"
  }
}
```

**Response**:
```json
{
  "mentor_id": "darwin",
  "mentor_name": "Darwin",
  "message": "Great question! Before I explain, what do you already know about how plants get their energy?",
  "provider_used": "openai",
  "model_used": "gpt-4-turbo-preview",
  "lvo_phase_detected": "learn"
}
```

#### 4. Send Message to Specific Mentor
```http
POST /api/chat/message
Content-Type: application/json

{
  "mentor_id": "stella",
  "message": "Help me solve 2x + 5 = 13",
  "student_context": {
    "age": 13
  },
  "conversation_history": [
    {"role": "user", "content": "I'm learning algebra"},
    {"role": "assistant", "content": "Algebra is so useful! Let's start."}
  ]
}
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_agents.py -v

# Run specific test
pytest tests/unit/test_agents.py::TestMentorPersonas::test_all_mentors_exist -v
```

Test coverage includes:
- ✅ Mentor persona loading
- ✅ System prompt rendering
- ✅ Socratic principle verification
- ✅ Pedagogical keyword checks
- ✅ LVO phase detection
- ✅ Safety boundary validation

---

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Settings & environment
│   ├── agents/                 # 🎓 Agent instruction layer
│   │   ├── personas.py         # Gold-standard prompts (8 mentors + Supervisor)
│   │   ├── mentor_engine.py    # Prompt assembly & LLM orchestration
│   │   ├── supervisor.py       # Intelligent routing
│   │   └── schemas.py          # Pydantic models
│   ├── llm/                    # 🤖 Multi-LLM abstraction
│   │   ├── router.py           # Vendor-agnostic LLM router
│   │   └── providers/          # OpenAI, Anthropic, Gemini, LucidAI
│   ├── lvo/                    # 📖 Learn-Verify-Own framework
│   ├── hpem/                   # 🧠 History-Practice-Eval-Meta
│   ├── gamification/           # 🎮 XP, achievements, rewards
│   ├── database/               # 🗄️ SQLAlchemy models
│   ├── api/                    # 🌐 REST endpoints
│   │   └── chat.py             # Chat API
│   └── utils/                  # 🛠️ Utilities
├── tests/
│   └── unit/
│       └── test_agents.py      # Agent system tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎓 Pedagogical Framework

All 8 mentors are built on **gold-standard pedagogical principles**:

### Core Principles

1. **Growth Mindset** (Dweck, 2006)
   - Normalize mistakes as learning opportunities
   - Praise effort, not just results
   - Use "yet" language

2. **Scaffolding** (Vygotsky's ZPD)
   - Break complexity into manageable steps
   - Concrete → Abstract progression
   - Just-in-time support

3. **Differentiation** (Tomlinson, 2014)
   - Age-appropriate language
   - Skill-level adaptation
   - Multiple representations

4. **Formative Assessment** (Black & Wiliam, 1998)
   - Frequent comprehension checks
   - Early misconception detection
   - Real-time adjustments

5. **Metacognition** (Flavell, 1979)
   - Self-awareness prompts
   - Reflection after problem-solving
   - Strategy evaluation

6. **Social-Emotional Learning (SEL)** (CASEL)
   - Validate feelings
   - Build self-efficacy
   - Psychological safety

### Socratic Communication

All mentors use a **three-tier question-first approach**:

1. **Probe** prior knowledge
2. **Guide** with strategic hints
3. **Explain** only after student attempts

See full framework: [`docs/agent-instruction-design.md`](../docs/agent-instruction-design.md)

---

## 🔧 Development

### Adding a New Mentor

1. **Define Persona** in `app/agents/personas.py`:
```python
NEW_MENTOR_PROMPT = """You are **NewMentor**, an AI [subject] mentor...
# Include all pedagogical principles
# Follow Socratic pattern
# Reference LVO phases
# Include safety boundaries
"""

MENTOR_PERSONAS["newmentor"] = MentorPersona(
    id="newmentor",
    display_name="NewMentor",
    emoji="🔬",
    subjects=["Subject Area"],
    age_min=10,
    age_max=18,
    # ... other fields
    system_prompt_template=NEW_MENTOR_PROMPT
)
```

2. **Test** in `tests/unit/test_agents.py`:
```python
def test_new_mentor_exists():
    mentor = get_mentor_by_id("newmentor")
    assert mentor is not None
```

3. **Run tests**: `pytest tests/unit/test_agents.py -v`

### Extending LLM Providers

1. Create provider in `app/llm/providers/`:
```python
class NewProviderClient(BaseLLMClient):
    async def complete(self, messages, ...):
        # Implementation
```

2. Register in `app/llm/router.py`:
```python
if settings.newprovider_api_key:
    self.providers["newprovider"] = NewProviderClient(...)
```

---

## 🔐 Security & Safety

### API Key Management
- **Never commit** `.env` files
- Use environment variables for all secrets
- Rotate keys regularly

### Safety Boundaries

All mentors are instructed to:
- ❌ Not provide medical, legal, or harmful advice
- ❌ Not request personal information
- ✅ Redirect distressed students to trusted adults
- ✅ Focus on learning and support

### Rate Limiting (TODO)
- Implement rate limiting for production
- Use Redis or similar for distributed rate limiting

---

## 📊 Performance

### Optimization Tips

1. **Use faster models for simple interactions**:
   - `gpt-3.5-turbo` for quick Q&A
   - `gpt-4-turbo` for complex reasoning

2. **Enable caching** (provider-specific):
   - OpenAI: Use logit_bias for common responses
   - Anthropic: Leverage prompt caching (beta)

3. **Async everywhere**:
   - All LLM calls are async
   - Use `asyncio.gather()` for parallel requests

4. **Database connection pooling**:
   - SQLAlchemy session management
   - Use async drivers (asyncpg, aiosqlite)

---

## 🐛 Troubleshooting

### "Provider 'openai' not available"
**Solution**: Add API key to `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### "ModuleNotFoundError: No module named 'app'"
**Solution**: Run from backend directory:
```bash
cd backend
python -m app.main
```

### Tests failing with "ANTHROPIC_API_KEY not found"
**Solution**: Tests don't require real API keys. Check test imports.

### CORS errors from frontend
**Solution**: Add frontend URL to `.env`:
```bash
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 📖 Documentation

- **Pedagogical Framework**: [`docs/agent-instruction-design.md`](../docs/agent-instruction-design.md)
- **Gold-Standard Implementation**: [`docs/agent-instructions-gold-standard.md`](../docs/agent-instructions-gold-standard.md)
- **API Docs**: http://localhost:8000/docs (when server running)

---

## 🤝 Contributing

1. Follow the existing code style (Black, Ruff)
2. Add tests for new features
3. Update documentation
4. Ensure pedagogical principles are maintained

### Code Quality

```bash
# Format code
black app/ tests/

# Lint
ruff check app/ tests/

# Type check
mypy app/
```

---

## 📜 License

Educational demonstration project for Stellecta AI Mentor platform.

---

## 🙏 Acknowledgments

Built on research-backed pedagogical principles:
- Carol Dweck (Growth Mindset)
- Lev Vygotsky (Scaffolding)
- Carol Ann Tomlinson (Differentiation)
- Paul Black & Dylan Wiliam (Formative Assessment)
- John Flavell (Metacognition)
- CASEL (Social-Emotional Learning)

---

## 📞 Support

For questions about the gold-standard agent instruction layer:
- Review: `docs/agent-instruction-design.md`
- Check: `docs/agent-instructions-gold-standard.md`
- Test: `pytest tests/unit/test_agents.py -v`

---

**Built with ❤️ for effective, research-backed AI mentoring**
