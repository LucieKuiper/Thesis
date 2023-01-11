import os
import psycopg2

class Config:
    SECRET_KEY = '.'

    try:
        prodURI = os.getenv('DATABASE_URL')
        prodURI = prodURI.replace("postgres://", "postgresql://")
        SQLALCHEMY_DATABASE_URI = prodURI
    except:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://lucie:citroentje@localhost:5432/pilot'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
