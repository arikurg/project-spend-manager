from app import create_app, get_celery

# 1. Create the app. This runs your factory, loads your .env file,
#    and configures the Celery object with your Redis URL.
app = create_app()

# 2. Push the app context so tasks can use your database (db.session)
app.app_context().push()

# 3. Get the fully configured celery object
celery = get_celery()

