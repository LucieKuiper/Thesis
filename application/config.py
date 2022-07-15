import os
import psycopg2

class Config:
    SECRET_KEY = '.'
    # Configure database
    # Old SQLlite DB


    SQLALCHEMY_DATABASE_URI = 'postgres://tsfgtjjijcsztm:7f97dfd9b00178777e07bae53e526254a3c4cfbd050f87824e4ab5b538df122a@ec2-34-247-172-149.eu-west-1.compute.amazonaws.com:5432/d5f5v6npk3mhc8'
    # New Mysql
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
