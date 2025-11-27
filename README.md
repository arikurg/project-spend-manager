# 💰 Spend Manager - B2B FinTech SaaS Expense Tracker

A business-to-business expense management application designed to help small businesses track, analyze, and optimize their recurring SaaS subscriptions and expenses. Built with Flask, PostgreSQL, and Celery—the exact tech stack Ramp uses.

## 🎯 Project Overview

**Mission:** Help businesses "spend less" by providing visibility into recurring expenses and automated renewal alerts.

**The Problem:** Small businesses often forget about active subscriptions, leading to unnecessary recurring charges and wasted budget.

**The Solution:** Spend Manager provides:
- 📊 Real-time analytics on subscription spending
- 🔔 Smart email alerts 7 days before renewal dates
- 💾 Secure PostgreSQL database for expense tracking
- ⚡ Fast, intuitive UI for quick expense management

## 🏗️ Architecture

### Backend Stack
- **Framework:** Flask (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** Flask-Login with Werkzeug password hashing
- **Task Queue:** Celery for async renewal reminders
- **Message Broker:** Redis for Celery task management
- **API:** RESTful JSON API with CORS support

### Frontend Stack
- **HTML/CSS/JavaScript:** Vanilla (no framework bloat)
- **Styling:** Custom CSS with modern design system
- **API Communication:** Fetch API with error handling

### Key Feature: Celery Email Alerts
When a user adds an expense, the system automatically schedules a Celery task to send an email reminder 7 days before the subscription renews, enabling users to make informed cancellation decisions and save money.

## 📋 Database Schema

```sql
-- Users table
users:
  - id (PK)
  - email (unique)
  - username (unique)
  - password_hash
  - company_name
  - created_at, updated_at

-- Expenses table
expenses:
  - id (PK)
  - user_id (FK → users.id)
  - name (service name)
  - category (Design, Development, etc.)
  - amount (monthly cost)
  - renewal_date
  - description
  - reminder_sent (boolean)
  - created_at, updated_at
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis 5+

### Installation

1. **Clone and Navigate**
   ```bash
   cd spend-manager
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   # Create PostgreSQL database
   createdb spend_manager_dev
   
   # Initialize tables (done automatically on app start)
   ```

5. **Configure Environment**
   - Edit `.env` file with your settings
   - Update `DATABASE_URL` if needed
   - Set `SECRET_KEY` for production

6. **Start Redis**
   ```bash
   redis-server
   ```

7. **Start Celery Worker** (in separate terminal)
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

8. **Run Flask App**
   ```bash
   python run.py
   ```

9. **Access Application**
   - Open http://localhost:5000
   - Register a new account
   - Start adding expenses!

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Expenses
- `POST /api/expenses` - Create new expense
- `GET /api/expenses` - Get all user expenses
- `GET /api/expenses/<id>` - Get specific expense
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense

### Dashboard Analytics
- `GET /api/dashboard/stats` - Comprehensive dashboard stats
- `GET /api/dashboard/summary` - Quick summary metrics

## 📄 License

MIT License - feel free to use for portfolio or learning purposes.

---

**Built with ❤️ for Ramp**

*Stack: Flask • PostgreSQL • SQLAlchemy • Celery • Redis • Python*

