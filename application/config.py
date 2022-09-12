import os
import psycopg2


class Config:
    SECRET_KEY = '.'

    prodURI = os.getenv('DATABASE_URL')
    prodURI = prodURI.replace("postgres://", "postgresql://")
    SQLALCHEMY_DATABASE_URI = prodURI

    SQLALCHEMY_TRACK_MODIFICATIONS = False