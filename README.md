# Stellecta - AI-Powered Educational Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

Stellecta is an advanced AI-powered educational platform featuring 8 specialized mentor agents, multi-curriculum support, and blockchain-based credential verification.

## 🌟 Features

### 🤖 8 AI Mentor Agents
- **Stella** - Mathematics Tutor
- **Max** - Physics & Engineering Guide
- **Nova** - Chemistry Expert
- **Darwin** - Biology Specialist
- **Lexis** - Language & Literature Mentor
- **Neo** - Technology & Computer Science
- **Luna** - Arts & Creativity Coach
- **Atlas** - History & Social Studies

### 📚 Multi-Curriculum Support
- **Indian Curricula**: CBSE, ICSE
- **UK Curricula**: National Curriculum, IGCSE
- **US Curricula**: Common Core

### 🎮 Gamification System
- XP & Leveling System
- Badges & Achievements
- Daily Streaks
- Global Leaderboards

### 🔗 Blockchain Integration
- H-PEM Credentials on Stellar Network
- Verifiable Learning Achievements
- Decentralized Credential Storage

### 🧠 Multi-LLM Router
- LucidAI Internal Models
- OpenAI GPT-4
- Anthropic Claude 3

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI 0.104+
- Python 3.11+
- PostgreSQL 15+
- SQLAlchemy 2.0+
- Redis 7.0+
- Celery 5.3+
- Stellar SDK

**Frontend:**
- React 18+
- TypeScript 5+
- Vite 5+
- Zustand (State Management)
- Tailwind CSS + shadcn/ui
- Axios

**DevOps:**
- Docker & Docker Compose
- Railway (Hosting)
- GitHub Actions (CI/CD)

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/stellecta/backend-unified-lucidai.git
cd backend-unified-lucidai
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env if needed
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development Setup

**Backend Development:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

**Frontend Development:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📖 Documentation

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Project Structure
```
stellecta/
├── backend/
│   ├── app/
│   │   ├── agents/          # 8 Mentor Agents
│   │   ├── api/             # API Endpoints
│   │   ├── core/            # Configuration
│   │   ├── database/        # Models & Database
│   │   ├── llm/             # Multi-LLM Router
│   │   ├── curriculum/      # Curriculum Providers
│   │   ├── blockchain/      # Stellar Integration
│   │   └── services/        # Business Logic
│   ├── tests/               # Backend Tests
│   └── alembic/             # Database Migrations
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React Components
│   │   ├── pages/           # Page Components
│   │   ├── stores/          # Zustand Stores
│   │   ├── services/        # API Services
│   │   └── types/           # TypeScript Types
│   └── tests/               # Frontend Tests
│
├── docs/                    # Documentation
├── scripts/                 # Utility Scripts
└── docker-compose.yml       # Docker Configuration
```

## 🧪 Testing

**Backend Tests:**
```bash
cd backend
pytest --cov=app --cov-report=html
# Target: 80% coverage
```

**Frontend Tests:**
```bash
cd frontend
npm run test
npm run test:coverage
# Target: 70% coverage
```

## 🚢 Deployment

### Railway Deployment

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Deploy**
```bash
railway up
```

### Manual Deployment

1. **Build Docker images**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Deploy to your infrastructure**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by the Stellecta Team
- Powered by LucidAI, OpenAI, and Anthropic
- Blockchain infrastructure by Stellar

## 📧 Contact

- Website: https://stellecta.com
- Email: support@stellecta.com
- GitHub: https://github.com/stellecta

---

**Version:** 1.0.0
**Status:** In Active Development
**Last Updated:** November 2025
