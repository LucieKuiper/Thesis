import os
import psycopg2

class Config:
    SECRET_KEY = '.'
    # Configure database
    # Old SQLlite DB
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://lucie:citroentje@localhost:5432/pilot'
    # New Mysql
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
