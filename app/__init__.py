from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import config
from app.models import db, User
from app.celery_app import celery, make_celery

login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    make_celery(app)
    
    # Register blueprints
    from app.routes import auth_bp, expenses_bp, dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(dashboard_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return {'error': 'Unauthorized'}, 401
    
    return app

def get_celery():
    """Get Celery instance"""
    return celery

