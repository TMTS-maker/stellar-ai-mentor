# Stellecta Platform - Deployment Guide

## Overview

Complete deployment guide for the Stellecta AI-powered educational platform.

---

## Prerequisites

### System Requirements
- **OS:** Linux (Ubuntu 20.04+ recommended) or macOS
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 20GB minimum
- **CPU:** 2 cores minimum, 4 cores recommended

### Software Requirements
- **Docker:** 20.10+ and Docker Compose 2.0+
- **Python:** 3.11+
- **Node.js:** 20.x LTS
- **PostgreSQL:** 15+
- **Redis:** 7.0+
- **Git:** 2.30+

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/TMTS-maker/stellar-ai-mentor.git
cd stellar-ai-mentor
```

### 2. Backend Environment Variables

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/stellecta

# Security
SECRET_KEY=your_super_secret_key_min_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","https://yourdomain.com"]

# LLM API Keys (optional - fallback mode works without)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-your-anthropic-key
LUCIDAI_API_KEY=your-lucidai-key

# Gamification
XP_PER_MESSAGE=10
```

### 3. Frontend Environment Variables

Create `frontend/.env`:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
# For production:
# VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

---

## Deployment Options

### Option 1: Docker Compose (Recommended)

#### Development
```bash
docker-compose up -d
```

Access:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

#### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Manual Deployment

#### Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Initialize badges
python -c "from app.services.badge_initializer import initialize_badges; from app.database.session import SessionLocal; db = SessionLocal(); initialize_badges(db); print('Badges initialized!')"

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Development mode
npm run dev

# Production build
npm run build

# Serve production build (using serve)
npm install -g serve
serve -s dist -p 3000
```

---

## Database Setup

### 1. Create Database

```bash
# Using psql
createdb stellecta

# Or using SQL
psql -U postgres
CREATE DATABASE stellecta;
```

### 2. Run Migrations

```bash
cd backend
alembic upgrade head
```

### 3. Initialize Data

```bash
# Initialize default badges
python scripts/init_badges.py

# Optional: Seed sample data
python scripts/seed_data.py
```

---

## Production Deployment

### Railway (Recommended)

#### Backend Deployment

1. **Create Railway Project**
```bash
railway init
```

2. **Add PostgreSQL**
```bash
railway add postgresql
```

3. **Set Environment Variables**
```bash
railway variables set SECRET_KEY=your_secret_key
railway variables set OPENAI_API_KEY=your_key
# ... other env vars
```

4. **Deploy**
```bash
railway up
```

#### Frontend Deployment (Vercel)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel --prod
```

3. **Set Environment Variable**
```bash
vercel env add VITE_API_BASE_URL production
# Enter your Railway backend URL
```

### Alternative: AWS EC2

#### Backend on EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql nginx -y

# Clone repository
git clone https://github.com/TMTS-maker/stellar-ai-mentor.git
cd stellar-ai-mentor/backend

# Set up virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Gunicorn for production
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### Frontend on S3 + CloudFront

```bash
# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## SSL/TLS Configuration

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal (cron job)
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## Monitoring & Logging

### Application Logging

Backend uses Python's logging module. Configure in `backend/app/core/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

Recommended tools:
- **Sentry** - Error tracking
- **Datadog** - APM and logs
- **Prometheus + Grafana** - Metrics
- **Uptime Robot** - Uptime monitoring

---

## Backup & Recovery

### Database Backups

```bash
# Manual backup
pg_dump stellecta > backup_$(date +%Y%m%d).sql

# Automated daily backups (cron)
0 2 * * * pg_dump stellecta > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Restore from Backup

```bash
psql stellecta < backup_20250115.sql
```

---

## Scaling

### Horizontal Scaling

#### Backend

- Run multiple Gunicorn workers
- Use load balancer (Nginx, HAProxy, AWS ALB)
- Redis for session storage

#### Database

- PostgreSQL read replicas
- Connection pooling (PgBouncer)
- Database sharding for large scale

### Vertical Scaling

- Increase EC2 instance size
- Upgrade RAM for caching
- SSD storage for database

---

## Health Checks

### Backend Health Endpoint

```python
# GET /health
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "version": "1.0.0"
}
```

### Frontend Health Check

```bash
curl https://yourdomain.com
# Should return 200 OK
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

**2. CORS Errors**
```bash
# Update CORS_ORIGINS in backend/.env
CORS_ORIGINS=["https://yourdomain.com"]
```

**3. Build Failures**
```bash
# Clear node_modules and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

**4. 502 Bad Gateway**
```bash
# Check backend is running
ps aux | grep uvicorn

# Check logs
tail -f /var/log/nginx/error.log
```

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS (SSL/TLS)
- [ ] Set secure CORS origins
- [ ] Enable rate limiting
- [ ] Use strong database passwords
- [ ] Enable firewall (UFW, Security Groups)
- [ ] Regular security updates
- [ ] Environment variables not in code
- [ ] Database backups enabled
- [ ] Monitoring and alerts set up

---

## Performance Optimization

### Backend

- Use Redis for caching
- Database query optimization (indexes)
- Enable gzip compression
- CDN for static assets

### Frontend

- Code splitting
- Lazy loading components
- Image optimization
- Bundle size analysis

---

## CI/CD Pipeline

GitHub Actions workflow automatically:
- ✅ Runs backend tests
- ✅ Runs frontend build
- ✅ Security scanning
- ✅ Code quality checks

Deploy on merge to main:
```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]

jobs:
  deploy:
    # Your deployment steps
```

---

## Rollback Procedure

### Quick Rollback

```bash
# Backend
git checkout <previous-commit>
docker-compose restart backend

# Frontend (Vercel)
vercel rollback
```

### Database Rollback

```bash
# Downgrade migrations
cd backend
alembic downgrade -1
```

---

## Support & Maintenance

### Regular Maintenance Tasks

**Daily:**
- Monitor error logs
- Check system resources

**Weekly:**
- Review database performance
- Update dependencies (security patches)

**Monthly:**
- Full backup verification
- Performance optimization review
- Security audit

---

## Additional Resources

- **API Documentation:** http://localhost:8000/docs
- **Repository:** https://github.com/TMTS-maker/stellar-ai-mentor
- **Issues:** https://github.com/TMTS-maker/stellar-ai-mentor/issues

---

## Quick Start Commands

```bash
# Local Development
docker-compose up -d

# Production Deployment (Railway)
railway up

# Check Status
docker-compose ps
curl http://localhost:8000/health

# View Logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop Services
docker-compose down
```

---

**Deployment Status:** ✅ Ready for production
**Documentation:** Complete
**Support:** Available via GitHub Issues
