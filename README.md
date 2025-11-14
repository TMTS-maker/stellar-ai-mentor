# Stellar AI - Interactive Avatar Learning Platform

> An AI-powered educational platform connecting schools, teachers, students, and parents through personalized, gamified learning experiences with interactive AI avatars.

## 🌟 Project Overview

Stellar AI is a comprehensive learning management system with:

- **AI-Powered Tutoring**: Interactive conversations with AI avatars using GPT-4/Claude
- **Gamification**: XP system, badges, streaks, and plant growth mechanics
- **Multi-Role Support**: School admins, teachers, students, and parents
- **Real-time Progress Tracking**: Comprehensive analytics and reporting
- **Speech Integration**: STT (Whisper), TTS (ElevenLabs), and Avatar Video (HeyGen/D-ID)

## 🏗️ Architecture

### Tech Stack

**Frontend**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- React Query (state management)
- React Router (navigation)

**Backend**
- Python 3.11+
- FastAPI (async API framework)
- SQLAlchemy 2.0 + Alembic (ORM + migrations)
- PostgreSQL (database)
- JWT authentication (python-jose)
- Pydantic v2 (validation)

**AI Services**
- OpenAI (GPT-4, Whisper STT)
- Anthropic Claude (optional LLM)
- ElevenLabs (TTS)
- HeyGen/D-ID (avatar video)

## 📁 Project Structure

```
stellar-ai-mentor/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic
│   │   │   └── ai/         # AI service abstractions
│   │   ├── auth.py         # JWT authentication
│   │   ├── config.py       # Settings
│   │   ├── db.py           # Database setup
│   │   └── main.py         # FastAPI app
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile
│   └── .env.example
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── contexts/           # React contexts (Auth)
│   ├── hooks/              # Custom hooks
│   ├── lib/                # Utilities (API client)
│   ├── pages/              # Page components
│   └── App.tsx
├── docker-compose.yml      # Docker setup
├── package.json            # Node dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+
- **Docker** (optional, recommended)

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd stellar-ai-mentor
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   cp .env.example .env
   ```

3. **Edit `backend/.env`** and add your API keys:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/stellar_ai
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   OPENAI_API_KEY=your-openai-key-here
   ELEVENLABS_API_KEY=your-elevenlabs-key-here
   # ... other keys
   ```

4. **Start services with Docker**
   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

6. **Start frontend**
   ```bash
   npm install
   npm run dev
   ```

7. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development Setup

#### Backend Setup

1. **Create Python virtual environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```bash
   createdb stellar_ai
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and API keys
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will be available at http://localhost:8000

#### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Ensure VITE_API_BASE_URL=http://localhost:8000/api/v1
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at http://localhost:5173

## 🔑 Environment Variables

### Backend (`backend/.env`)

```env
# Application
APP_NAME="Stellar AI Backend"
DEBUG=True
API_V1_PREFIX="/api/v1"

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stellar_ai

# JWT Auth
SECRET_KEY=<generate-with: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# AI Services
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
HEYGEN_API_KEY=...
DID_API_KEY=...
```

### Frontend (`.env`)

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 📊 Database Schema

### Core Entities

- **User**: Base user model (email, password, role)
- **School**: School organization
- **Teacher**: Teacher profile
- **Student**: Student profile
- **Parent**: Parent profile
- **Classroom**: Class management
- **Subject**: Subject/course
- **Task**: Learning tasks/exercises
- **StudentTaskProgress**: Progress tracking
- **ConversationSession**: AI conversation tracking
- **ConversationMessage**: Individual messages
- **XPEvent**: XP tracking
- **Badge**: Achievement definitions
- **StudentBadge**: Earned badges

### Relationships

- School has many Teachers, Students, Classrooms, Subjects
- Teacher manages many Classrooms
- Classroom has many Students (via Enrollment)
- Student has many Tasks (via Progress)
- Parent can link to multiple Students (many-to-many)

## 🎯 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

### Students
- `GET /api/v1/students/me/dashboard` - Student dashboard data
- `GET /api/v1/students/me/xp` - XP and level data
- `GET /api/v1/students/me/badges` - Earned badges
- `GET /api/v1/students/me/rings` - Ring progress
- `GET /api/v1/students/me/plant` - Plant growth
- `GET /api/v1/students/me/streaks` - Streak data
- `POST /api/v1/students/tasks/{id}/start` - Start a task
- `POST /api/v1/students/tasks/{id}/complete` - Complete a task

### Teachers
- `GET /api/v1/teachers/me/classes` - Teacher's classrooms
- `GET /api/v1/teachers/me/classes/{id}/students/progress` - Class progress

### Parents
- `POST /api/v1/parents/link-child` - Link to a student
- `GET /api/v1/parents/me/children` - Get linked children
- `GET /api/v1/parents/me/overview` - Children overview

### Schools
- `POST /api/v1/schools` - Create school
- `POST /api/v1/schools/{id}/teachers` - Add teacher
- `POST /api/v1/schools/{id}/classes` - Create classroom
- `POST /api/v1/schools/{id}/subjects` - Create subject

### Classrooms
- `POST /api/v1/classes/{id}/students/bulk` - Bulk import students

### Tasks
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task details

### AI Conversation
- `POST /api/v1/ai/conversation/text` - Text conversation
- `POST /api/v1/ai/conversation/voice` - Voice conversation
- `POST /api/v1/ai/conversation/{id}/end` - End session

## 🧪 Development Workflow

### Creating Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Running Tests (TODO)

```bash
# Backend tests
cd backend
pytest

# Frontend tests
npm test
```

### Building for Production

```bash
# Backend (Docker)
cd backend
docker build -t stellar-ai-backend .

# Frontend
npm run build
```

## 🎮 Usage Guide

### 1. School Admin Flow

1. Sign up with role `school_admin`
2. Create school (automatically created on signup)
3. Add teachers via `/schools/{id}/teachers`
4. Create classrooms
5. Create subjects

### 2. Teacher Flow

1. Teacher account created by school admin
2. Login and view classes
3. Create tasks for students
4. Bulk import students via CSV/JSON
5. Monitor student progress

### 3. Student Flow

1. Account created via teacher bulk import or signup
2. Login and view dashboard
3. Start and complete tasks
4. Interact with AI avatar
5. Earn XP and badges
6. Track progress (rings, plant, streaks)

### 4. Parent Flow

1. Sign up with role `parent`
2. Link to children via email
3. View children's progress
4. Monitor XP, tasks, and activity

## 🤖 AI Integration

### LLM (GPT-4 / Claude)

The system uses a friendly tutor persona defined in `backend/app/services/ai/llm_service.py`:

```python
SYSTEM_PROMPT = """
You are Stellar AI, an educational tutor for children aged 6–14.
You speak warmly, simply, clearly, and encouragingly.
...
"""
```

To switch between OpenAI and Claude:
```env
LLM_PROVIDER=openai  # or anthropic
```

### STT (Speech-to-Text)

Uses OpenAI Whisper API. Configure:
```env
OPENAI_API_KEY=your-key
```

### TTS (Text-to-Speech)

Uses ElevenLabs. Configure:
```env
ELEVENLABS_API_KEY=your-key
```

### Avatar Video

Supports HeyGen or D-ID:
```env
HEYGEN_API_KEY=your-key
# or
DID_API_KEY=your-key
```

**Note**: Avatar integration is stubbed for MVP. Implement real API calls in:
- `backend/app/services/ai/avatar_service.py`

## 📦 Deployment

### Backend (Railway / Render)

1. Connect your repository
2. Set environment variables (all from `backend/.env.example`)
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Run migrations: `alembic upgrade head`

### Frontend (Vercel / Netlify)

1. Connect repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Set environment variable: `VITE_API_BASE_URL=https://your-backend-url.com/api/v1`

### Database (Supabase / Neon)

1. Create PostgreSQL database
2. Copy connection string to `DATABASE_URL`
3. Ensure it includes `+asyncpg` for async support

## 🔒 Security Considerations

- **JWT Tokens**: Store in httpOnly cookies (production) or localStorage (MVP)
- **Password Hashing**: Uses bcrypt
- **CORS**: Configure allowed origins in `BACKEND_CORS_ORIGINS`
- **API Keys**: Never commit to git, use environment variables
- **SQL Injection**: Protected by SQLAlchemy ORM
- **Input Validation**: Pydantic schemas validate all inputs

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U postgres -l

# Test connection
psql postgresql://postgres:postgres@localhost:5432/stellar_ai
```

### Alembic Migration Errors

```bash
# Reset migrations (development only!)
alembic downgrade base
alembic upgrade head

# Or manually create tables
# In backend/app/main.py, uncomment: await init_db()
```

### CORS Errors

Ensure frontend URL is in `BACKEND_CORS_ORIGINS`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### API Not Responding

Check backend logs:
```bash
docker-compose logs backend
# or
uvicorn app.main:app --reload --log-level debug
```

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛣️ Roadmap

- [ ] Add unit and integration tests
- [ ] Implement real-time WebSocket for live conversations
- [ ] Add file upload for avatar customization
- [ ] Implement learning path system
- [ ] Add analytics dashboard for schools
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Advanced gamification (leaderboards, competitions)
- [ ] Integration with LMS platforms (Canvas, Moodle)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary. All rights reserved.

## 📧 Support

For issues or questions:
- Create an issue in the repository
- Contact: support@stellar-ai.com

---

**Built with ❤️ for transforming education through AI**
