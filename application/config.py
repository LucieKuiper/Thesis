import os
import psycopg2

class Config:
    SECRET_KEY = '.'
    # Configure database
    # Old SQLlite DB


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
