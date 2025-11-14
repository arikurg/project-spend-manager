from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models import db, User, Expense
from app.tasks import send_renewal_reminder_task

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
expenses_bp = Blueprint('expenses', __name__, url_prefix='/api/expenses')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


# ==================== AUTH ROUTES ====================

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('username') or not data.get('password'):
        return {'error': 'Missing required fields'}, 400
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already registered'}, 409
    
    if User.query.filter_by(username=data['username']).first():
        return {'error': 'Username already taken'}, 409
    
    user = User(
        email=data['email'],
        username=data['username'],
        company_name=data.get('company_name', '')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    return {'message': 'User created successfully', 'user': user.to_dict()}, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Missing email or password'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': 'Invalid email or password'}, 401
    
    login_user(user)
    return {'message': 'Logged in successfully', 'user': user.to_dict()}, 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return {'message': 'Logged out successfully'}, 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user info"""
    return {'user': current_user.to_dict()}, 200


# ==================== EXPENSE ROUTES ====================

@expenses_bp.route('', methods=['POST'])
@login_required
def create_expense():
    """Create a new expense"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'category', 'amount', 'renewal_date']):
        return {'error': 'Missing required fields: name, category, amount, renewal_date'}, 400
    
    try:
        renewal_date = datetime.strptime(data['renewal_date'], '%Y-%m-%d').date()
    except ValueError:
        return {'error': 'Invalid renewal_date format (use YYYY-MM-DD)'}, 400
    
    expense = Expense(
        user_id=current_user.id,
        name=data['name'],
        category=data['category'],
        amount=float(data['amount']),
        renewal_date=renewal_date,
        description=data.get('description', '')
    )
    
    db.session.add(expense)
    db.session.commit()
    
    # Schedule renewal reminder (7 days before renewal)
    reminder_date = renewal_date - timedelta(days=7)
    if reminder_date > datetime.utcnow().date():
        send_renewal_reminder_task.apply_async(
            args=[expense.id],
            eta=datetime.combine(reminder_date, datetime.min.time())
        )
    
    return {'message': 'Expense created', 'expense': expense.to_dict()}, 201


@expenses_bp.route('', methods=['GET'])
@login_required
def get_expenses():
    """Get all expenses for current user"""
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return {'expenses': [e.to_dict() for e in expenses]}, 200


@expenses_bp.route('/<int:expense_id>', methods=['GET'])
@login_required
def get_expense(expense_id):
    """Get a specific expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return {'error': 'Expense not found'}, 404
    
    return {'expense': expense.to_dict()}, 200


@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    """Update an expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return {'error': 'Expense not found'}, 404
    
    data = request.get_json()
    
    expense.name = data.get('name', expense.name)
    expense.category = data.get('category', expense.category)
    expense.amount = float(data.get('amount', expense.amount))
    expense.description = data.get('description', expense.description)
    
    if 'renewal_date' in data:
        try:
            expense.renewal_date = datetime.strptime(data['renewal_date'], '%Y-%m-%d').date()
            expense.reminder_sent = False  # Reset reminder flag
        except ValueError:
            return {'error': 'Invalid renewal_date format (use YYYY-MM-DD)'}, 400
    
    db.session.commit()
    
    return {'message': 'Expense updated', 'expense': expense.to_dict()}, 200


@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return {'error': 'Expense not found'}, 404
    
    db.session.delete(expense)
    db.session.commit()
    
    return {'message': 'Expense deleted'}, 200


# ==================== DASHBOARD ROUTES ====================

@dashboard_bp.route('/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get dashboard analytics"""
    today = datetime.utcnow().date()
    
    # Get all expenses for user
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Calculate metrics
    total_monthly_spend = sum(e.amount for e in expenses)
    
    # Spend by category
    category_spend = {}
    for expense in expenses:
        category_spend[expense.category] = category_spend.get(expense.category, 0) + expense.amount
    
    # Upcoming renewals (next 30 days)
    upcoming_date = today + timedelta(days=30)
    upcoming = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.renewal_date.between(today, upcoming_date)
    ).order_by(Expense.renewal_date).all()
    
    # Recently added
    recent = Expense.query.filter_by(user_id=current_user.id).order_by(
        Expense.created_at.desc()
    ).limit(5).all()
    
    return {
        'total_monthly_spend': total_monthly_spend,
        'expense_count': len(expenses),
        'category_spend': category_spend,
        'upcoming_renewals': [e.to_dict() for e in upcoming],
        'recently_added': [e.to_dict() for e in recent],
        'currency': 'USD'
    }, 200


@dashboard_bp.route('/summary', methods=['GET'])
@login_required
def get_summary():
    """Get quick summary for dashboard"""
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    total = sum(e.amount for e in expenses)
    yearly_spend = total * 12
    
    # Count expenses by category
    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + 1
    
    # Highest spend category
    category_totals = {}
    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount
    
    highest_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else None
    
    return {
        'total_monthly_spend': total,
        'total_yearly_spend': yearly_spend,
        'total_subscriptions': len(expenses),
        'categories': categories,
        'highest_spend_category': highest_category
    }, 200

