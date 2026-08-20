from flask import Flask

from config import Config
from utils.database import create_tables

from routes.auth import auth
from routes.profile import profile
from routes.interview import interview
from routes.resume import resume
from routes.admin import admin

app = Flask(__name__)
app.config.from_object(Config)

# Create database tables
create_tables()

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(interview)
app.register_blueprint(resume)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)