#!/bin/bash

# Stellar AI Demo Data Seeding Script
# This script runs database migrations and seeds demo data

set -e  # Exit on error

echo "=================================="
echo "🌟 Stellar AI - Demo Setup"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to backend directory
cd "$(dirname "$0")/.."

echo ""
echo -e "${BLUE}Step 1: Running database migrations...${NC}"
echo ""

# Run Alembic migrations
alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations completed successfully${NC}"
else
    echo -e "${YELLOW}⚠ Migration failed or database not available${NC}"
    echo -e "${YELLOW}  Make sure PostgreSQL is running and DATABASE_URL is configured${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 2: Seeding demo data...${NC}"
echo ""

# Run the seeding script
python3 -m app.demo.seed_demo_data

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=================================="
    echo -e "✅ Demo setup complete!"
    echo -e "==================================${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Start the backend server:"
    echo "     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "  2. Start the frontend (in frontend directory):"
    echo "     npm run dev"
    echo ""
    echo "  3. Access the application:"
    echo "     Frontend: http://localhost:5173"
    echo "     Backend API: http://localhost:8000"
    echo "     API Docs: http://localhost:8000/docs"
    echo ""
else
    echo -e "${YELLOW}⚠ Seeding failed${NC}"
    exit 1
fi
