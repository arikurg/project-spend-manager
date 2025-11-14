from datetime import datetime, timedelta
from app.models import db, Expense, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from app.celery_app import celery


def send_email(to_email, subject, body_html, body_text):
    """Send email using SMTP (using console fallback for demo)"""
    print(f"\n{'='*60}")
    print(f"EMAIL ALERT")
    print(f"{'='*60}")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body (HTML):\n{body_html}")
    print(f"Body (Text):\n{body_text}")
    print(f"{'='*60}\n")

def schedule_renewal_reminder(celery, app, expense_id):
    """
    Schedule a Celery task to send a reminder 7 days before renewal.
    This is called when an expense is created/updated.
    """
    with app.app_context():
        expense = Expense.query.get(expense_id)
        if not expense:
            return
        
        renewal_date = expense.renewal_date
        reminder_date = renewal_date - timedelta(days=7)
        
        # Schedule the task
        send_renewal_reminder_task.apply_async(
            args=[expense_id],
            eta=reminder_date
        )

@celery.task
def send_renewal_reminder_task(expense_id):
    """
    Celery task: Send renewal reminder email 7 days before subscription renews.
    This runs asynchronously.
    """
    expense = Expense.query.get(expense_id)
    if not expense or expense.reminder_sent:
        return False
    
    user = User.query.get(expense.user_id)
    if not user:
        return False
    
    subject = f"💰 Subscription Renewal Alert: {expense.name}"
    
    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #1a73e8;">Subscription Renewal Alert</h2>
            
            <p>Hi {user.username},</p>
            
            <p>Your subscription <strong>{expense.name}</strong> is renewing in 7 days!</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Subscription Details:</strong></p>
                <ul>
                    <li><strong>Service:</strong> {expense.name}</li>
                    <li><strong>Category:</strong> {expense.category}</li>
                    <li><strong>Amount:</strong> ${expense.amount:.2f}</li>
                    <li><strong>Renewal Date:</strong> {expense.renewal_date.strftime('%B %d, %Y')}</li>
                </ul>
            </div>
            
            <p style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 3px;">
                <strong>⚠️ Action Required:</strong> Do you still need this subscription? If not, this is a great time to cancel before the renewal and save money!
            </p>
            
            <p>At Ramp, we believe every dollar counts. Review your subscriptions regularly to ensure you're only paying for what you use.</p>
            
            <p>Log in to your dashboard to manage your expenses: <a href="http://localhost:5000">Your Spend Manager</a></p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            <p style="color: #666; font-size: 12px;">
                This is an automated reminder from your Small Business Spend Manager. If you have questions, please visit our dashboard.
            </p>
        </body>
    </html>
    """
    
    body_text = f"""
    Subscription Renewal Alert
    
    Hi {user.username},
    
    Your subscription {expense.name} is renewing in 7 days!
    
    Subscription Details:
    - Service: {expense.name}
    - Category: {expense.category}
    - Amount: ${expense.amount:.2f}
    - Renewal Date: {expense.renewal_date.strftime('%B %d, %Y')}
    
    ACTION REQUIRED: Do you still need this subscription? If not, this is a great time to cancel before the renewal and save money!
    
    At Ramp, we believe every dollar counts. Review your subscriptions regularly to ensure you're only paying for what you use.
    
    Log in to your dashboard to manage your expenses: http://localhost:5000
    """
    
    # Send the email
    send_email(user.email, subject, body_html, body_text)
    
    # Mark as reminder sent
    expense.reminder_sent = True
    db.session.commit()
    
    return True

