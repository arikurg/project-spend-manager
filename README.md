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

## 🎤 How This Project Demonstrates Ramp Alignment

### 1. **Mission Alignment**
- Directly solves the "help businesses spend less" mission
- Prevents wasted spending on forgotten subscriptions
- Provides actionable insights for cost reduction

### 2. **Tech Stack Alignment**
- ✅ Python & Flask (core backend)
- ✅ PostgreSQL (data persistence)
- ✅ SQLAlchemy ORM (database abstraction)
- ✅ Celery (async task processing)
- ✅ REST API (scalable architecture)

### 3. **Engineering Excellence**
- Clean separation of concerns (models, routes, tasks)
- Proper error handling and validation
- Secure password hashing
- Async processing for background tasks
- SQL injection protection via SQLAlchemy

### 4. **Product Thinking**
- User-centric design (simple but powerful)
- Smart feature: renewal alerts drive immediate value
- Real problem solving: prevents budget waste
- Scalable architecture for growth

## 🌟 Standout Feature: Renewal Reminders

### How It Works
1. User adds an expense with a renewal date
2. System calculates reminder date (7 days before)
3. Celery task scheduled for that date/time
4. On reminder date, automated email sent
5. User can decide to cancel before renewal

### Code Example
```python
# When expense is created
send_renewal_reminder_task.apply_async(
    args=[expense.id],
    eta=datetime.combine(reminder_date, datetime.min.time())
)

# Task executes at scheduled time
def send_renewal_reminder_task(expense_id):
    expense = Expense.query.get(expense_id)
    user = expense.user
    # Send email: "Your {service} renews in 7 days - $XX.XX"
    # Mark reminder_sent to avoid duplicates
```

## 📊 Dashboard Features

- **Monthly Spend:** Total recurring expenses
- **Yearly Projection:** 12x monthly spend
- **Category Breakdown:** Spending by type (Design, Dev, etc.)
- **Upcoming Renewals:** Next 30 days sorted by date
- **Recent Expenses:** Latest additions for quick review
- **Visual Charts:** Category spending distribution

## 🔐 Security Considerations

- Passwords hashed with Werkzeug
- SQLAlchemy prevents SQL injection
- CORS configured for API
- User isolation (expenses only visible to owner)
- Session-based authentication
- Environment variables for sensitive data

## 🚢 Deployment (AWS Example)

### Option 1: Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.9 spend-manager
eb create prod-env
eb deploy
```

### Option 2: EC2 + Nginx + Gunicorn
```bash
# On EC2 instance
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app

# Nginx reverse proxy (listening on port 80/443)
```

### Environment Variables (Production)
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@rds.amazonaws.com/dbname
CELERY_BROKER_URL=redis://elasticache.amazonaws.com:6379
SECRET_KEY=<generate-strong-key>
```

## 📈 Future Enhancements

- [ ] Payment method integration (Stripe for billing)
- [ ] Team/workspace support (multi-user per company)
- [ ] Custom alert timing (not just 7 days)
- [ ] Bulk expense import (CSV)
- [ ] Smart categorization using ML
- [ ] Integration with accounting software (QuickBooks, Xero)
- [ ] Spending trends and forecasting
- [ ] Mobile app (React Native)

## 🎓 Learning Resources

This project demonstrates:
- **REST API Design:** Proper HTTP methods, status codes, error handling
- **Database Design:** Foreign keys, relationships, data integrity
- **Authentication:** Secure password storage, session management
- **Async Processing:** Task scheduling, background jobs
- **Frontend Development:** Vanilla JS, modern CSS, responsive design
- **Security:** Input validation, SQL injection prevention, CORS

## 📝 Interview Talking Points

**"I built Spend Manager to demonstrate understanding of Ramp's mission to help businesses 'spend less.' The app uses your exact stack—Flask, PostgreSQL, SQLAlchemy, and Celery—to track recurring expenses and send smart renewal alerts 7 days before subscriptions charge.**

**The key feature is the Celery-powered email reminder system. When a business adds a $1000/year subscription, the system automatically schedules a task that fires a week before renewal, asking 'Do you still need this?' Many businesses forget they have active subscriptions, so this feature drives real savings.**

**I designed it as a B2B FinTech solution that aligns with Ramp's core value. The backend is production-ready with proper authentication, error handling, and async processing. The frontend is simple but functional, focusing on solving the real problem rather than over-engineering UI."**

## 📄 License

MIT License - feel free to use for portfolio or learning purposes.

---

**Built with ❤️ for Ramp**

*Stack: Flask • PostgreSQL • SQLAlchemy • Celery • Redis • Python*

