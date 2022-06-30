from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pandas as pd
import os
print(os.getcwd())


import pymysql


# Configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = '.'
# Configure database
# Old SQLlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# New Mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Start Loging manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import Users to be able create database
from application.models import User



# Load in CSV file from relative source
def load_data(file= "\static\data.csv"):
    # source location of current file
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    df = pd.read_csv(__location__ + file)
    return df

# Create database when non existent with startupp
if __name__ == '__main__':
    data = load_data()
    db.create_all()

from application import routes
