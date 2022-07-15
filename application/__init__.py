from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pandas as pd
import os
from application.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# Start Loging manager
login_manager = LoginManager(app)
login_manager.login_view = 'pilot.login'
login_manager.login_message_category = 'info'

# Import Users to be able to create database
from application.pilot.models import User
from application.ai_advice.models import AIUser




# Load in CSV file from relative source
def load_data(file="data.csv"):
    # source location of current file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    df = pd.read_csv(os.path.join(STATICFILES_DIRS, file),)
    return df


# Create database when non existent with startupp
if __name__ == '__main__':
    data = load_data()
    db.create_all()

from application.pilot.routes import pilot
from application.main.routes import main
from application.ai_advice.routes import ai_advice


app.register_blueprint(pilot)
app.register_blueprint(main)
app.register_blueprint(ai_advice)