class Config:
    SECRET_KEY = '.'
    # Configure database
    # Old SQLlite DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///survey_data.db'
    # New Mysql
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
