import os
from app import create_app
from dotenv import load_dotenv
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/login')
def login():
    from flask import render_template
    return render_template('login.html')

@app.route('/register')
def register():
    from flask import render_template
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    from flask import render_template
    from flask_login import login_required
    @login_required
    def _dashboard():
        return render_template('dashboard.html')
    return _dashboard()

@app.route('/expenses')
def expenses():
    from flask import render_template
    from flask_login import login_required
    @login_required
    def _expenses():
        return render_template('expenses.html')
    return _expenses()

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(error):
    return {'error': 'Server error'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

