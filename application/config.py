import os
import psycopg2

class Config:
    SECRET_KEY = '.'
    # Configure database

    SQLALCHEMY_DATABASE_URI = 'heroku pg:psql postgresql-globular-41149 --app lucie-thesis-pilot'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
