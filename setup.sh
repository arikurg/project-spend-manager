#!/bin/bash

echo "🚀 Spend Manager Setup Script"
echo "=============================="

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check PostgreSQL
echo "Checking PostgreSQL..."
which psql > /dev/null || { echo "PostgreSQL client is required"; exit 1; }

# Check Redis
echo "Checking Redis..."
which redis-cli > /dev/null || { echo "Redis is required"; exit 1; }

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create database: createdb spend_manager_dev"
echo "2. Start Redis: redis-server"
echo "3. Start Celery (in separate terminal): celery -A app.celery_app worker --loglevel=info"
echo "4. Start Flask: python run.py"
echo "5. Open http://localhost:5000"

