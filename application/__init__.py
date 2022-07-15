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
def load_data(file="\static\data.csv"):
    # source location of current file
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    df = pd.read_csv(__location__ + file)
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